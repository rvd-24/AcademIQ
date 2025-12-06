# 📋 Pending Tasks & Incomplete Features

**Last Updated:** 2024  
**Project:** AcademIQ - Academic Performance Management System

---

## 🔴 **CRITICAL BUGS & ISSUES**

### 1. **File Upload Service Bug**
- **Location:** `src/services/admin_service.py:13`
- **Issue:** Function signature expects `file: str` but receives `UploadFile` object
- **Problem:** Uses undefined `file_path` variable instead of handling `UploadFile`
- **Impact:** Upload endpoint will crash
- **Fix Needed:** Handle `UploadFile` properly (read bytes, save temporarily, or process in-memory)

### 2. **Upload Endpoint Incomplete**
- **Location:** `src/routers/admin_router.py:15-32`
- **Issue:** Marksheet insertion is commented out, returns undefined `marksheet_id`
- **Problem:** Data extraction works but doesn't save to database
- **Fix Needed:** Uncomment and fix `insert_marksheet_data()` call

### 3. **Missing Import in query_crud.py**
- **Location:** `src/crud/query_crud.py:40`
- **Issue:** Uses `Integer` without importing it
- **Fix Needed:** Add `from sqlalchemy import Integer`

### 4. **Missing Import in student_crud.py**
- **Location:** `src/crud/student_crud.py:52`
- **Issue:** Uses `Marksheet` without importing it
- **Fix Needed:** Add `from models.marksheet import Marksheet`

### 5. **Database Connection Mismatch**
- **Issue:** Two database setups exist:
  - Async: `src/config/database.py` (asyncpg)
  - Sync: `src/db/db.py` (psycopg2)
- **Problem:** Routes use sync `get_db()` but async setup exists
- **Fix Needed:** Consolidate to one approach (prefer async) or update all routes

---

## 🔐 **AUTHENTICATION & AUTHORIZATION**

### 6. **Authentication System Missing**
- **Location:** `src/routers/auth.py` (empty)
- **Missing:**
  - Login endpoint
  - JWT token generation
  - Password verification
  - Token refresh
  - Logout

### 7. **Authorization Middleware Missing**
- **Missing:**
  - Role-based access control (RBAC)
  - JWT token validation middleware
  - Student vs Teacher permission checks
  - Protected route decorators

### 8. **Session Management**
- **Missing:**
  - User session tracking
  - Token blacklisting (logout)
  - Session timeout handling

---

## 📤 **FILE UPLOAD & INGESTION PIPELINE**

### 9. **Complete Marksheet Ingestion Flow**
- **Location:** `src/routers/admin_router.py:15`
- **Missing:**
  - Parse extracted JSON from OpenAI
  - Map to database schema
  - Create/update subjects
  - Insert marksheet record
  - Insert student marks
  - Handle errors and retries
  - Update processing status

### 10. **Data Validation & Normalization**
- **Missing:**
  - Validate extracted data structure
  - Normalize subject codes/names
  - Handle duplicate marksheets
  - Validate student registration number match
  - Confidence score tracking

### 11. **Error Handling**
- **Missing:**
  - Failed extraction handling
  - Partial data insertion handling
  - Retry mechanism for failed uploads
  - Error logging and notification

---

## 📊 **ANALYTICS & RANKING**

### 12. **Analytics Queries Module Empty**
- **Location:** `src/queries/analytics.py` (empty file)
- **Missing:**
  - Student rank calculation (overall, semester, subject)
  - Percentile calculation
  - Performance band assignment (Top 5%, Top 25%, etc.)
  - Cohort grouping logic
  - Aggregate statistics

### 13. **Ranking System**
- **Missing:**
  - Rank calculation per exam/semester
  - Percentile calculation
  - Performance bands
  - Comparison with cohort (without exposing individual marks)

### 14. **Materialized Views**
- **Missing:**
  - `mv_student_totals` materialized view creation
  - Refresh mechanism (after ingestion)
  - Scheduled refresh (cron/background job)

### 15. **Database Views**
- **Missing:**
  - `vw_student_analytics_raw` view
  - `vw_student_chat` view (safe for students)
  - `vw_teacher_results` view (full access)
  - SQL view definitions

---

## 🤖 **CHATBOT IMPLEMENTATION**

### 16. **Chatbot Queries Module Empty**
- **Location:** `src/queries/chatbot.py` (empty file)
- **Missing:**
  - SQL query generation for student queries
  - SQL query generation for teacher queries
  - Query validation
  - Safe query templates

### 17. **QnA Router Empty**
- **Location:** `src/routers/qna_router.py` (only comment)
- **Missing:**
  - Chat endpoint for students
  - Chat endpoint for teachers
  - Message history retrieval
  - LLM integration (OpenAI/Azure OpenAI)
  - Query processing logic

### 18. **Chatbot Security**
- **Missing:**
  - Student query filtering (no other students' data)
  - Query sanitization
  - PII detection and blocking
  - Rate limiting

### 19. **LLM Integration**
- **Missing:**
  - Chat completion API calls
  - Context building from database
  - Response generation
  - Conversation history management

### 20. **Chat History Storage**
- **Model exists but not used**
- **Missing:**
  - Save chat messages to `ChatHistory` table
  - Retrieve conversation history
  - Context building from history

---

## 👨‍🎓 **STUDENT DASHBOARD & API**

### 21. **Student Router Missing**
- **Missing:**
  - Student routes file
  - Get own marks endpoint
  - Get own rank/percentile endpoint
  - Get performance summary endpoint
  - Compare with cohort (anonymized)

### 22. **Student Access Control**
- **Missing:**
  - RLS policies for students table
  - RLS policies for marksheets table
  - RLS policies for student_marks table
  - Session variable setting (`app.current_user_student_id`)

### 23. **Student Analytics Endpoints**
- **Missing:**
  - `/api/student/my-marks`
  - `/api/student/my-rank`
  - `/api/student/my-percentile`
  - `/api/student/performance-summary`
  - `/api/student/compare-cohort` (anonymized)

---

## 👨‍🏫 **TEACHER/ADMIN DASHBOARD & API**

### 24. **Teacher Dashboard Endpoints**
- **Missing:**
  - Get all students endpoint
  - Get student marks endpoint
  - Get backlog tracking endpoint
  - Get performance graphs data endpoint
  - Subject-wise performance endpoint
  - Semester-wise performance endpoint

### 25. **Analytics Visualization Data**
- **Missing:**
  - Graph data endpoints (performance across subjects)
  - Graph data endpoints (performance across semesters)
  - Backlog tracking endpoints
  - Class statistics endpoints
  - Export functionality (CSV/PDF)

### 26. **Teacher Access Control**
- **Missing:**
  - Teacher role verification
  - Full access RLS policies
  - Teacher-specific endpoints

---

## 🛡️ **SECURITY & PRIVACY**

### 27. **Row-Level Security (RLS)**
- **Missing:**
  - RLS policies on all tables
  - Session variable management
  - Policy creation SQL scripts
  - Testing RLS policies

### 28. **Database Roles**
- **Missing:**
  - `ingest_role` creation
  - `chatbot_student_role` creation
  - `chatbot_teacher_role` creation
  - `analytics_role` creation
  - `admin_role` creation
  - Role-based connection strings

### 29. **Security Definer Function**
- **Missing:**
  - `api.get_student_summary()` function creation
  - Function security checks
  - Function testing

### 30. **Audit Logging**
- **Missing:**
  - Audit log triggers
  - `audit_logs` table (if not exists)
  - Trigger creation SQL
  - Audit log retrieval endpoints

### 31. **Student Aliasing System**
- **Missing:**
  - Alias generation logic
  - Alias assignment on student creation
  - Alias lookup for chatbot
  - Alias-to-student mapping

---

## 🗄️ **DATA MODELS & SCHEMA**

### 32. **Model Inconsistencies**
- **Issue:** `src/db/models.py` has old schema (Branch, ExamResult, etc.)
- **Problem:** Doesn't match actual models in `src/models/`
- **Fix Needed:** Remove or update to match current schema

### 33. **Missing Fields in Models**
- **Check if all required fields from original schema are present:**
  - Confidence scores in marksheet
  - Raw extracted JSON storage
  - Academic year tracking
  - Exam type tracking

---

## 🌐 **API ENDPOINTS**

### 34. **Missing Student Endpoints**
- `/api/student/*` - All student endpoints

### 35. **Missing Teacher Endpoints**
- `/api/teacher/*` - All teacher dashboard endpoints

### 36. **Missing Analytics Endpoints**
- `/api/analytics/*` - Analytics endpoints

### 37. **Missing Chatbot Endpoints**
- `/api/chat/student` - Student chatbot
- `/api/chat/teacher` - Teacher chatbot
- `/api/chat/history` - Chat history

---

## 🧪 **TESTING & VALIDATION**

### 38. **Unit Tests**
- **Missing:** All unit tests

### 39. **Integration Tests**
- **Missing:** All integration tests

### 40. **API Tests**
- **Missing:** All API endpoint tests

### 41. **Data Validation Tests**
- **Missing:** Marksheet extraction validation tests

---

## ⚙️ **CONFIGURATION & DEPLOYMENT**

### 42. **Environment Variables**
- **Missing:**
  - `.env.example` file
  - Documentation for required env vars
  - Azure credentials setup guide

### 43. **Database Migration Scripts**
- **Missing:**
  - Alembic setup
  - Migration scripts for views
  - Migration scripts for RLS policies
  - Migration scripts for functions

### 44. **Requirements.txt Incomplete**
- **Missing Dependencies:**
  - `passlib[bcrypt]` (for password hashing)
  - `python-jose` (for JWT)
  - `PyMuPDF` / `fitz` (for PDF processing)
  - `azure-storage-blob` (for Azure Blob)
  - `openai` (for Azure OpenAI)
  - `pydantic` (for schemas)

---

## 📚 **DOCUMENTATION**

### 45. **API Documentation**
- **Missing:**
  - OpenAPI/Swagger documentation
  - Endpoint descriptions
  - Request/response examples

### 46. **Database Documentation**
- **Missing:**
  - Schema documentation
  - View definitions
  - Function definitions
  - RLS policy documentation

### 47. **Setup Guide**
- **Missing:**
  - Installation instructions
  - Database setup guide
  - Environment configuration guide
  - Deployment guide

---

## ⚡ **PERFORMANCE & OPTIMIZATION**

### 48. **Database Indexes**
- **Missing:**
  - Review and optimize indexes
  - Add missing indexes for common queries

### 49. **Query Optimization**
- **Missing:**
  - Optimize analytics queries
  - Add query caching where appropriate

### 50. **Background Jobs**
- **Missing:**
  - Background job system (Celery/APScheduler)
  - Scheduled materialized view refresh
  - Async file processing queue

---

## 📊 **PRIORITY SUMMARY**

### 🔴 **CRITICAL** (Blocks Core Functionality)
1. Fix file upload service bug
2. Complete marksheet ingestion flow
3. Fix import errors
4. Consolidate database setup

### 🟠 **HIGH PRIORITY** (Core Features)
5. Authentication system
6. Authorization middleware
7. Student router and endpoints
8. Teacher router and endpoints
9. Chatbot implementation
10. Analytics queries

### 🟡 **MEDIUM PRIORITY** (Important Features)
11. RLS implementation
12. Database views creation
13. Materialized views
14. Audit logging
15. Error handling

### 🟢 **LOW PRIORITY** (Nice to Have)
16. Testing suite
17. Documentation
18. Performance optimization
19. Background jobs

---

## 📝 **NOTES**

- **Total Tasks Identified:** 50+
- **Estimated Completion Time:** Varies by task complexity
- **Recommended Order:** Start with Critical → High → Medium → Low priority tasks
- **Dependencies:** Some tasks depend on others (e.g., RLS depends on authentication)

---

## 🔗 **RELATED FILES**

- Database Config: `src/config/database.py`
- Models: `src/models/`
- Routers: `src/routers/`
- Services: `src/services/`
- CRUD: `src/crud/`
- Queries: `src/queries/`

---

**Last Review Date:** 2024  
**Next Review:** After major milestones

