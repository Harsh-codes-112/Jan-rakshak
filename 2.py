from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_hash = Column(String, unique=True, index=True) # Hashed for privacy
    email = Column(String, unique=True, nullable=True)
    role = Column(String, default="CITIZEN") # CITIZEN, ADMIN, NODAL_OFFICER
    is_verified = Column(Boolean, default=False)
    # External ID integration strictly handled via OAuth/UIDAI tokens, no raw numbers stored
    uidai_reference_token = Column(String, nullable=True) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Complaint(Base):
    __tablename__ = 'complaints'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=True) # Nullable for anonymous
    tracking_id = Column(String, unique=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    category = Column(String(100)) # Bribery, Harassment, etc.
    status = Column(String(50), default="DRAFT") # SUBMITTED, UNDER_REVIEW, REFERRED, FIR_REGISTERED
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    department = Column(String(150), nullable=True)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Evidence(Base):
    __tablename__ = 'evidence'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID, ForeignKey('complaints.id'))
    file_path = Column(String) # Encrypted S3 path
    file_type = Column(String(50))
    sha256_hash = Column(String(64)) # Integrity verification
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

class AIAnalysis(Base):
    __tablename__ = 'ai_analysis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID, ForeignKey('complaints.id'), unique=True)
    applicable_laws = Column(JSONB) # BNS, BNSS sections
    summary = Column(Text)
    missing_info = Column(JSONB)
    fraud_score = Column(Float) # Trust layer flag
    created_at = Column(DateTime, default=datetime.datetime.utcnow)