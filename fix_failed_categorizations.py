"""
Fix Failed Categorizations using Fuzzy Matching

This script reads failed_categorizations.json and:
1. Fuzzy matches invalid categories/sub-categories to valid ones
2. Saves corrected categorization to the database
3. Removes successfully fixed entries from failed_categorizations.json
"""
import asyncio
import json
import logging
import os
from datetime import datetime
from uuid import UUID

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from rapidfuzz import fuzz, process
from sqlalchemy import update

from db.config import async_session
from models.company import Company

load_dotenv(find_dotenv())

# Setup logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = os.path.join(LOG_DIR, f"fix_categorizations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

FAILED_COMPANIES_FILE = "failed_categorizations.json"
FUZZY_THRESHOLD = 70  # Minimum similarity score to accept a match


def clean_categories(d: dict) -> dict:
    """Remove None values and transform to {category: [sub_categories]} format"""
    category_dict = {}
    for category, sub_cats in d.items():
        category_dict[category] = [v for v in sub_cats.values() if v is not None]
    return category_dict


def load_valid_categories() -> dict:
    """Load valid categories from the master Excel file"""
    df = pd.read_excel("Service Master Data .xlsx")
    raw_categories = json.loads(df.to_json())
    return clean_categories(raw_categories)


def fuzzy_match_category(invalid_category: str, valid_categories: list, threshold: int = FUZZY_THRESHOLD) -> str | None:
    """
    Fuzzy match an invalid category to the closest valid category.
    
    Returns:
        Matched category name or None if no good match found
    """
    if not valid_categories:
        return None
    
    # First check for exact match (case-insensitive)
    for valid in valid_categories:
        if invalid_category.lower() == valid.lower():
            return valid
    
    # Fuzzy match
    result = process.extractOne(
        invalid_category,
        valid_categories,
        scorer=fuzz.token_sort_ratio
    )
    
    if result and result[1] >= threshold:
        logger.debug(f"Matched category '{invalid_category}' -> '{result[0]}' (score: {result[1]})")
        return result[0]
    
    return None


def fuzzy_match_subcategory(invalid_sub: str, valid_subs: list, threshold: int = FUZZY_THRESHOLD) -> str | None:
    """
    Fuzzy match an invalid sub-category to the closest valid sub-category.
    
    Returns:
        Matched sub-category name or None if no good match found
    """
    if not valid_subs:
        return None
    
    # First check for exact match (case-insensitive)
    for valid in valid_subs:
        if invalid_sub.lower() == valid.lower():
            return valid
    
    # Fuzzy match
    result = process.extractOne(
        invalid_sub,
        valid_subs,
        scorer=fuzz.token_sort_ratio
    )
    
    if result and result[1] >= threshold:
        logger.debug(f"Matched sub-category '{invalid_sub}' -> '{result[0]}' (score: {result[1]})")
        return result[0]
    
    return None


def fix_categorization(raw_output: dict, valid_categories: dict) -> tuple[list, list, list]:
    """
    Fix invalid categories and sub-categories using fuzzy matching.
    
    Args:
        raw_output: The raw_llm_output from failed_categorizations.json
        valid_categories: Dict of {category: [sub_categories]}
    
    Returns:
        Tuple of (fixed_categories, fixed_summaries, unmatched_items)
    """
    fixed_categories = []
    fixed_summaries = []
    unmatched_items = []
    
    categories_list = raw_output.get('categories', [])
    summaries_list = raw_output.get('summaries', [])
    
    # Build a lookup for summaries by category
    summary_map = {s.get('category'): s.get('summary') for s in summaries_list}
    
    valid_category_names = list(valid_categories.keys())
    
    for cat_mapping in categories_list:
        original_category = cat_mapping.get('category')
        original_subs = cat_mapping.get('sub_categories', [])
        
        # Try to match the category
        if original_category in valid_categories:
            matched_category = original_category
        else:
            matched_category = fuzzy_match_category(original_category, valid_category_names)
            if matched_category:
                logger.info(f"Category fuzzy matched: '{original_category}' -> '{matched_category}'")
            else:
                logger.warning(f"Could not match category: '{original_category}'")
                unmatched_items.append(f"Category: {original_category}")
                continue
        
        # Get valid sub-categories for this category
        valid_subs = valid_categories.get(matched_category, [])
        
        # Match sub-categories
        matched_subs = []
        for sub in original_subs:
            if sub in valid_subs:
                matched_subs.append(sub)
            else:
                matched_sub = fuzzy_match_subcategory(sub, valid_subs)
                if matched_sub:
                    logger.info(f"Sub-category fuzzy matched: '{sub}' -> '{matched_sub}' (under {matched_category})")
                    # Avoid duplicates
                    if matched_sub not in matched_subs:
                        matched_subs.append(matched_sub)
                else:
                    logger.warning(f"Could not match sub-category: '{sub}' under '{matched_category}'")
                    unmatched_items.append(f"Sub-category: {sub} (under {matched_category})")
        
        # Only add if we have valid sub-categories
        if matched_subs:
            fixed_categories.append({
                "category": matched_category,
                "sub_categories": matched_subs
            })
            
            # Get or create summary for this category
            summary = summary_map.get(original_category) or summary_map.get(matched_category)
            if summary:
                fixed_summaries.append({
                    "category": matched_category,
                    "summary": summary
                })
    
    return fixed_categories, fixed_summaries, unmatched_items


async def update_company_categorization(
    company_id: str,
    categories: list,
    summaries: list
) -> bool:
    """
    Update a company's categorization data in the database.
    """
    try:
        async with async_session() as session:
            await session.execute(
                update(Company)
                .where(Company.id == UUID(company_id))
                .values(
                    edverise_categories=categories,
                    edverise_category_summary=summaries,
                    edverise_categorized=True
                )
            )
            await session.commit()
        return True
    except Exception as e:
        logger.error(f"Error updating company {company_id}: {e}")
        return False


def load_failed_companies() -> list:
    """Load failed companies from JSON file"""
    if not os.path.exists(FAILED_COMPANIES_FILE):
        logger.info(f"No failed companies file found at {FAILED_COMPANIES_FILE}")
        return []
    
    with open(FAILED_COMPANIES_FILE, 'r', encoding='utf-8') as f:
        failed = json.load(f)
    
    logger.info(f"Loaded {len(failed)} failed companies from {FAILED_COMPANIES_FILE}")
    return failed


def save_remaining_failures(failures: list):
    """Save remaining failures back to JSON file"""
    with open(FAILED_COMPANIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(failures, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(failures)} remaining failures to {FAILED_COMPANIES_FILE}")


async def main(dry_run: bool = False, threshold: int = FUZZY_THRESHOLD):
    """
    Main function to fix failed categorizations.
    
    Args:
        dry_run: If True, don't update database, just show what would be fixed
        threshold: Minimum fuzzy match score (0-100)
    """
    global FUZZY_THRESHOLD
    FUZZY_THRESHOLD = threshold
    
    logger.info(f"Starting fix_failed_categorizations (dry_run={dry_run}, threshold={threshold})")
    
    # Load valid categories
    valid_categories = load_valid_categories()
    logger.info(f"Loaded {len(valid_categories)} valid categories")
    
    # Load failed companies
    failed_companies = load_failed_companies()
    if not failed_companies:
        return
    
    success_count = 0
    skip_count = 0
    partial_fix_count = 0
    remaining_failures = []
    
    for entry in failed_companies:
        company_id = entry.get('id')
        company_name = entry.get('name', 'Unknown')
        raw_output = entry.get('raw_llm_output')
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {company_name} (ID: {company_id})")
        
        # Skip entries without raw_llm_output (LLM exceptions)
        if not raw_output:
            logger.warning(f"Skipping {company_name} - no raw_llm_output (likely LLM exception)")
            remaining_failures.append(entry)
            skip_count += 1
            continue
        
        # Fix the categorization
        fixed_categories, fixed_summaries, unmatched = fix_categorization(raw_output, valid_categories)
        
        if not fixed_categories:
            logger.warning(f"Could not fix any categories for {company_name}")
            remaining_failures.append(entry)
            skip_count += 1
            continue
        
        # Log the results
        logger.info(f"Fixed categories: {len(fixed_categories)}")
        for fc in fixed_categories:
            logger.info(f"  - {fc['category']}: {fc['sub_categories']}")
        
        if unmatched:
            logger.warning(f"Unmatched items for {company_name}:")
            for item in unmatched:
                logger.warning(f"  - {item}")
            partial_fix_count += 1
        
        if dry_run:
            logger.info(f"[DRY RUN] Would update {company_name}")
            continue
        
        # Update database
        success = await update_company_categorization(
            company_id=company_id,
            categories=fixed_categories,
            summaries=fixed_summaries
        )
        
        if success:
            logger.info(f"Successfully updated {company_name}")
            success_count += 1
        else:
            logger.error(f"Failed to update {company_name}")
            remaining_failures.append(entry)
    
    # Save remaining failures
    if not dry_run:
        save_remaining_failures(remaining_failures)
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total processed: {len(failed_companies)}")
    logger.info(f"Successfully fixed: {success_count}")
    logger.info(f"Partially fixed (some unmatched): {partial_fix_count}")
    logger.info(f"Skipped (no raw output / unfixable): {skip_count}")
    logger.info(f"Remaining failures: {len(remaining_failures)}")


async def preview_fixes(limit: int = 10):
    """
    Preview the fixes that would be made without updating the database.
    Useful for checking the fuzzy matching quality.
    """
    valid_categories = load_valid_categories()
    failed_companies = load_failed_companies()
    
    if not failed_companies:
        return
    
    count = 0
    for entry in failed_companies:
        if count >= limit:
            break
            
        company_name = entry.get('name', 'Unknown')
        raw_output = entry.get('raw_llm_output')
        
        if not raw_output:
            continue
        
        print(f"\n{'='*60}")
        print(f"Company: {company_name}")
        print(f"Original errors: {entry.get('errors', [])}")
        print("-" * 40)
        
        fixed_categories, fixed_summaries, unmatched = fix_categorization(raw_output, valid_categories)
        
        print("Fixed categories:")
        for fc in fixed_categories:
            print(f"  - {fc['category']}: {fc['sub_categories']}")
        
        if fixed_summaries:
            print("\nFixed summaries:")
            for fs in fixed_summaries:
                print(f"  - {fs['category']}: {fs['summary'][:80]}...")
        
        if unmatched:
            print(f"\nUnmatched items:")
            for item in unmatched:
                print(f"  - {item}")
        
        count += 1


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--dry-run":
            # Dry run - show what would be fixed without updating DB
            asyncio.run(main(dry_run=True))
        elif sys.argv[1] == "--preview":
            # Preview fixes for first N companies
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            asyncio.run(preview_fixes(limit=limit))
        elif sys.argv[1] == "--threshold":
            # Set custom threshold
            threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 70
            asyncio.run(main(dry_run=False, threshold=threshold))
    else:
        # Default: run with database updates
        asyncio.run(main(dry_run=False))
