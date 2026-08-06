from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Automatically creates tables in onboarding.db on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoftStack Onboarding API")

## --- CORS Middleware --- ##
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


## --- Pydantic Data Validation Schemas --- ##
class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    company: Optional[str] = Field(None, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    preferred_contact_method: str = Field("Email", max_length=50)


class BriefCreate(BaseModel):
    business_summary: str = Field(..., max_length=4000, description="Overview of business model.")
    target_audience: str = Field(..., max_length=1500, description="Description of ideal users/demographics.")
    competitors: Optional[str] = Field(None, max_length=1500, description="Direct/indirect competitors.")
    discovery_source: Optional[str] = Field(None, max_length=100, description="Marketing attribution data.")
    primary_goal: str = Field(..., max_length=1000, description="Primary technical objective.")
    required_features: List[str] = Field(..., description="Mandatory features or integrations requested.")
    anti_features: Optional[List[str]] = Field(None, description="Explicit list of anti-patterns.")
    creative_energy: int = Field(3, ge=1, le=5, description="Stylistic vibe rating from 1 to 5.")
    accessibility_requirements: Optional[str] = Field(None, max_length=1500,
                                                      description="Accessibility accommodations.")
    has_accessibility_priority: bool = Field(False, description="Flag for strict WCAG compliance.")
    existing_assets: Optional[str] = Field(None, max_length=1500, description="Inventory notes on existing assets.")
    technical_contact: Optional[str] = Field(None, max_length=100, description="Internal developer/IT contact.")
    timeline: str = Field(..., max_length=200, description="Desired timeline window.")
    budget_range: str = Field(..., max_length=100, description="Financial tier or pricing bracket.")
    decision_makers: Optional[str] = Field(None, max_length=500, description="Sign-off decision makers.")
    success_kpis: str = Field(..., max_length=1500, description="Metrics defining success.")
    brand_asset_status: str = Field(..., max_length=1000, description="Asset readiness status.")
    maintenance_preference: Optional[str] = Field(None, max_length=500, description="Post-launch support needs.")


class FullOnboardingSubmission(BaseModel):
    client: ClientCreate
    brief: BriefCreate


# --- Outbound Dashboard Response Schemas --- ##
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
    success_kpis: str
    brand_asset_status: str
    maintenance_preference: Optional[str] = None

    class Config:
        from_attributes = True


## --- The Endpoints --- ##

@app.post("/api/v1/onboarding", status_code=status.HTTP_201_CREATED)
def submit_onboarding_form(payload: FullOnboardingSubmission, db: Session = Depends(get_db)):
    # Check if client exists
    existing_client = db.query(models.Client).filter(
        models.Client.email == payload.client.email
    ).first()

    if not existing_client:
        new_client = models.Client(
            name=payload.client.name,
            company=payload.client.company,
            email=payload.client.email,
            phone=payload.client.phone,
            preferred_contact_method=payload.client.preferred_contact_method
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        client_id = new_client.id
    else:
        client_id = existing_client.id
        has_updates = False
        if payload.client.company and payload.client.company != existing_client.company:
            existing_client.company = payload.client.company
            has_updates = True
        if payload.client.phone and payload.client.phone != existing_client.phone:
            existing_client.phone = payload.client.phone
            has_updates = True
        if payload.client.preferred_contact_method != existing_client.preferred_contact_method:
            existing_client.preferred_contact_method = payload.client.preferred_contact_method
            has_updates = True

        if has_updates:
            db.add(existing_client)

    # Create linked project brief
    new_brief = models.ProjectBrief(
        client_id=client_id,
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
    try:
        db.commit()
        db.refresh(new_brief)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database transaction failed: {str(e)}"
        )

    return {
        "message": "Hooray! Onboarding brief processed successfully",
        "brief_id": new_brief.id
    }


@app.get("/api/v1/briefs", response_model=List[BriefDashboardResponse], status_code=status.HTTP_200_OK)
def get_all_briefs(db: Session = Depends(get_db)):
    """Fetches all submitted briefs along with their attached client profiles."""
    return db.query(models.ProjectBrief).all()
