from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base
import uuid
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_hash = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=True)
    role = Column(String, default="CITIZEN")
    is_verified = Column(Boolean, default=False)
    uidai_reference_token = Column(String, nullable=True) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Complaint(Base):
    __tablename__ = 'complaints'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=True)
    tracking_id = Column(String, unique=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    category = Column(String(100))
    status = Column(String(50), default="DRAFT")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    department = Column(String(150), nullable=True)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Evidence(Base):
    __tablename__ = 'evidence'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID, ForeignKey('complaints.id'))
    file_path = Column(String)
    file_type = Column(String(50))
    sha256_hash = Column(String(64))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

class AIAnalysis(Base):
    __tablename__ = 'ai_analysis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID, ForeignKey('complaints.id'), unique=True)
    applicable_laws = Column(JSONB)
    summary = Column(Text)
    missing_info = Column(JSONB)
    fraud_score = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
