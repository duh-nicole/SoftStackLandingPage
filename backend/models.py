from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_order=True, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    company = Column(String(100), nullable=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    preferred_contact_method = Column(String(50), default="Email", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to ProjectBriefs (One-to-Many)
    briefs = relationship(
        "ProjectBrief",
        back_populates="client",
        cascade="all, delete-orphan"
    )


class ProjectBrief(Base):
    __tablename__ = "project_briefs"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    # Section 01 / Attribution
    discovery_source = Column(String(100), nullable=True, default="")

    # Section 02: Scope & Requirements
    business_summary = Column(Text, nullable=False)
    target_audience = Column(Text, nullable=False)
    competitors = Column(Text, nullable=True)
    primary_goal = Column(Text, nullable=False)

    # Store python lists as native JSON arrays
    required_features = Column(JSON, nullable=False, default=list)
    anti_features = Column(JSON, nullable=True, default=list)

    creative_energy = Column(Integer, default=3, nullable=False)
    has_accessibility_priority = Column(Boolean, default=False, nullable=False)
    accessibility_requirements = Column(Text, nullable=True)
    existing_assets = Column(Text, nullable=True)
    technical_contact = Column(String(100), nullable=True)

    # Section 03: Logistics & Budget
    timeline = Column(String(200), nullable=False)
    budget_range = Column(String(100), nullable=False)
    decision_makers = Column(String(500), nullable=True)
    success_kpis = Column(Text, nullable=True)
    brand_asset_status = Column(String(1000), nullable=True)

    # Section 04: Maintenance & Metadata
    maintenance_preference = Column(String(500), nullable=True)
    status = Column(String(50), default="Received", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Reverse relationship back to Client
    client = relationship("Client", back_populates="briefs")
