from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    company = Column(String(100), nullable=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    preferred_contact_method = Column(String(50), default="Email")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One-to-many relationship linking back to the project briefs
    briefs = relationship("ProjectBrief", back_populates="client", cascade="all, delete-orphan")


class ProjectBrief(Base):
    __tablename__ = "project_briefs"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    # Bucket 1: Business Profile
    business_summary = Column(Text, nullable=False)
    target_audience = Column(Text, nullable=False)
    competitors = Column(Text, nullable=True)
    technical_contact = Column(String(100), nullable=True)
    discovery_source = Column(String(100), nullable=True)

    # Bucket 2 & 3: Tech & Design Features
    primary_goal = Column(String(1000), nullable=False)
    required_features = Column(JSON, nullable=False)
    existing_assets = Column(Text, nullable=True)
    accessibility_requirements = Column(Text, nullable=True)
    has_accessibility_priority = Column(Boolean, default=False)
    creative_energy = Column(Integer, default=3)
    anti_features = Column(JSON, nullable=True)

    # Bucket 3.5: Strategic Evaluation Questions
    decision_makers = Column(String(500), nullable=True)
    success_kpis = Column(Text, nullable=False)
    brand_asset_status = Column(Text, nullable=False)
    maintenance_preference = Column(String(500), nullable=True)

    # Bucket 4: Logistics
    timeline = Column(String(200), nullable=False)
    budget_range = Column(String(100), nullable=False)
    status = Column(String(50), default="Brief Submitted")
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship linking back to the parent client details
    client = relationship("Client", back_populates="briefs")
