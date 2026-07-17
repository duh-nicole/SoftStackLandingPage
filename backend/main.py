from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# This initializes your database and creates the onboarding.db file automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoftStack Onboarding API")

## --- CORS Middleware --- ##
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

## --- Pydantic Data Validation Schemas --- ##
class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    company: Optional[str] = Field(None, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    phone: str = Field(None, max_length=20)
    preferred_contact_method: str = Field("Email", max_length=50)


class BriefCreate(BaseModel):
    business_summary: str = Field(..., max_length = 4000, description = "A high-level overview of the client's business model, values, and core operations.")
    target_audience: str = Field(..., max_length = 1500, description = "Description of the ideal users, target market demographics, or core personas for this product.")
    competitors: Optional[str] = Field(None, max_length = 1500, description = "Direct or indirect market competitors in the client's industry that we should analyze.")
    discovery_source: Optional[str] = Field(None, max_length = 100, description = "Marketing attribution data indicating how the client found SoftStack Studios (e.g., Google, Referral, Twitter).")
    primary_goal: str = Field(..., max_length = 1000, description = "The primary technical or business objective the client expects this project to solve.")
    required_features: List[str] = Field(..., description = "A list of specific mandatory technical features or integrations requested (e.g., Stripe, Auth0, CMS).")
    anti_features: Optional[List[str]] = Field(None, description = "An explicit list of UI elements, design patterns, or technical directions the client strongly dislikes.")
    creative_energy: int = Field(3, ge = 1, le = 5, description = "A stylistic vibe rating from 1 (strictly corporate, safe, and conservative) to 5 (experimental, highly creative, and modern).")
    accessibility_requirements: Optional[str] = Field(None, max_length = 1500, description = "Specific descriptions of user accessibility accommodations needed for the build.")
    has_accessibility_priority: bool = Field(False, description = "A boolean flag indicating if the project requires strict legal WCAG/ADA compliance auditing.")
    existing_assets: Optional[str] = Field(None, max_length = 1500, description = "Inventory notes on what the client already owns (e.g., current domain names, existing Figma files, hosting packages).")
    technical_contact: Optional[str] = Field(None, max_length = 100, description = "Contact information for the client's internal developer or IT administrator, if applicable.")
    timeline: str = Field(..., max_length = 200, description = "The client's desired development timeline window or strict drop-dead launch date.")
    budget_range: str = Field(..., max_length = 100, description = "The financial tier or pricing bracket allocated by the client for the initial build phase.")
    decision_makers: Optional[str] = Field(None, max_length = 500, description = "Who holds final sign-off authority?")
    success_kpis: str = Field(..., max_length = 1500, description = "What metric defines success for this build?")
    brand_asset_status: str = Field(..., max_length = 1000, description = "Are copy/logos ready or do they need production?")
    maintenance_preference: Optional[str] = Field(None, max_length = 500, description = "Do they need post-launch support?")

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
    status: str
    creative_energy: int
    has_accessibility_priority: bool
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
## Endpoint 1 : Submit Onboarding Form ##
@app.post("/api/v1/onboarding", status_code=status.HTTP_201_CREATED)
def submit_onboarding_form(payload: FullOnboardingSubmission, db: Session = Depends(get_db)):
    # Check if the client already exists
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
        # Track and sync any profile updates dynamically
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

    # Create the project brief linked to that client
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
        decision_makers = payload.brief.decision_makers,
        success_kpis = payload.brief.success_kpis,
        brand_asset_status = payload.brief.brand_asset_status,
        maintenance_preference = payload.brief.maintenance_preference
    )

    db.add(new_brief)
    try:
        db.commit()
        db.refresh(new_brief)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Whoops! Database transaction failed: {str(e)}"
        )

    return {
        "message": "Hooray! Onboarding brief processed successfully",
        "brief_id": new_brief.id
    }


## Endpoint 2 : Get All Briefs (Admin Dashboard)
@app.get("/api/v1/briefs", response_model=List[BriefDashboardResponse], status_code=status.HTTP_200_OK)
def get_all_briefs(db: Session = Depends(get_db)):
    """Fetches all submitted briefs along with their attached client profiles."""
    return db.query(models.ProjectBrief).all()
