# models/chat_history.py
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    # Primary Key
    chat_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    # Foreign Key
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Chat Content
    message_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_history")
    
    def __repr__(self):
        return f"<ChatHistory(id={self.chat_id}, user={self.user_id}, time={self.timestamp})>"
    
    def to_dict(self):
        return {
            "chat_id": str(self.chat_id),
            "user_id": str(self.user_id),
            "message_text": self.message_text,
            "response_text": self.response_text,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }