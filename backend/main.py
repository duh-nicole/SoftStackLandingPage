import os
import secrets
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import models
from database import engine, get_db
security = HTTPBasic()

# Read credentials from environment variables (defaults for local dev)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "softstack2026!")


def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoftStack Onboarding API")

## --- CORS Middleware --- ##
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",  # Local development
        "http://localhost:3000",
        "https://softstack.studio",  # Production domain
        "https://www.softstack.studio",  # Subdomain
        "https://duh-nicole.github.io",  # GitHub Pages domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


## --- Inbound Request Schemas --- ##
class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    company: Optional[str] = Field(None, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    preferred_contact_method: str = Field("Email", max_length=50)


class BriefCreate(BaseModel):
    business_summary: str = Field(..., max_length=4000, description="Overview of business model.")
    target_audience: str = Field(..., max_length=1500, description="Description of ideal users.")
    competitors: Optional[str] = Field(None, max_length=1500)
    discovery_source: Optional[str] = Field(None, max_length=100)
    primary_goal: str = Field(..., max_length=1000)
    required_features: List[str] = Field(default_factory=list)
    anti_features: Optional[List[str]] = Field(default_factory=list)
    creative_energy: int = Field(3, ge=1, le=5)
    accessibility_requirements: Optional[str] = Field(None, max_length=1500)
    has_accessibility_priority: bool = Field(False)
    existing_assets: Optional[str] = Field(None, max_length=1500)
    technical_contact: Optional[str] = Field(None, max_length=100)
    timeline: str = Field(..., max_length=200)
    budget_range: str = Field(..., max_length=100)
    decision_makers: Optional[str] = Field(None, max_length=500)
    success_kpis: Optional[str] = Field(None, max_length=1500)
    brand_asset_status: Optional[str] = Field(None, max_length=1000)
    maintenance_preference: Optional[str] = Field(None, max_length=500)


class FullOnboardingSubmission(BaseModel):
    client: ClientCreate
    brief: BriefCreate


## --- Outbound Response Schemas --- ##
class ClientResponse(BaseModel):
    name: str
    company: Optional[str] = None
    preferred_contact_method: str

    class Config:
        from_attributes = True


class BriefDashboardResponse(BaseModel):
    id: int
    primary_goal: str
    budget_range: str
    timeline: str
    status: Optional[str] = "Received"
    creative_energy: int
    has_accessibility_priority: bool
    required_features: Optional[List[str]] = None
    client: ClientResponse
    business_summary: str
    anti_features: Optional[List[str]] = None
    accessibility_requirements: Optional[str] = None
    discovery_source: Optional[str] = None
    decision_makers: Optional[str] = None
    success_kpis: Optional[str] = None
    brand_asset_status: Optional[str] = None
    maintenance_preference: Optional[str] = None

    class Config:
        from_attributes = True


## --- Endpoints --- ##

@app.post("/api/v1/onboarding", status_code=status.HTTP_201_CREATED)
def submit_onboarding_form(payload: FullOnboardingSubmission, db: Session = Depends(get_db)):
    try:
        # 1. Fetch or initialize Client profile
        existing_client = db.query(models.Client).filter(
            models.Client.email == payload.client.email
        ).first()

        if not existing_client:
            client = models.Client(
                name=payload.client.name,
                company=payload.client.company,
                email=payload.client.email,
                phone=payload.client.phone,
                preferred_contact_method=payload.client.preferred_contact_method
            )
            db.add(client)
            db.flush()  # Populates client.id without ending transaction
        else:
            client = existing_client
            if payload.client.company:
                client.company = payload.client.company
            if payload.client.phone:
                client.phone = payload.client.phone
            client.preferred_contact_method = payload.client.preferred_contact_method

        # 2. Attach Project Brief
        new_brief = models.ProjectBrief(
            client_id=client.id,
            business_summary=payload.brief.business_summary,
            target_audience=payload.brief.target_audience,
            competitors=payload.brief.competitors,
            discovery_source=payload.brief.discovery_source or "",
            primary_goal=payload.brief.primary_goal,
            required_features=payload.brief.required_features,
            anti_features=payload.brief.anti_features,
            creative_energy=payload.brief.creative_energy,
            accessibility_requirements=payload.brief.accessibility_requirements,
            has_accessibility_priority=payload.brief.has_accessibility_priority,
            existing_assets=payload.brief.existing_assets,
            technical_contact=payload.brief.technical_contact,
            timeline=payload.brief.timeline,
            budget_range=payload.brief.budget_range,
            decision_makers=payload.brief.decision_makers,
            success_kpis=payload.brief.success_kpis,
            brand_asset_status=payload.brief.brand_asset_status,
            maintenance_preference=payload.brief.maintenance_preference
        )

        db.add(new_brief)
        db.commit()
        db.refresh(new_brief)

        return {
            "status": "success",
            "message": "Onboarding brief processed successfully",
            "brief_id": new_brief.id
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database operational error: {str(e)}"
        )


@app.get(
    "/api/v1/briefs",
    response_model=List[BriefDashboardResponse],
    status_code=status.HTTP_200_OK
)
def get_all_briefs(
        db: Session = Depends(get_db),
        admin: str = Depends(authenticate_admin)  # Protects endpoint
):
    """Fetches all submitted briefs along with their attached client profiles."""
    return db.query(models.ProjectBrief).all()
