from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.database.db import get_db
from app.models.esg_configuration import (
    EsgConfiguration,
)
from app.models.user import User


settings_router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


class EsgConfigResponse(BaseModel):
    id: int
    auto_emission_calculation: bool
    require_evidence_for_csr: bool
    environmental_weight: float
    social_weight: float
    governance_weight: float

    model_config = {"from_attributes": True}


class EsgConfigUpdate(BaseModel):
    auto_emission_calculation: bool | None = None
    require_evidence_for_csr: bool | None = None
    environmental_weight: float | None = None
    social_weight: float | None = None
    governance_weight: float | None = None


@settings_router.get(
    "/esg-configuration",
    response_model=EsgConfigResponse,
    summary="Get ESG configuration",
)
def get_esg_configuration(
    db: Session = Depends(get_db),
):
    config = db.get(EsgConfiguration, 1)

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ESG configuration not found.",
        )

    return config


@settings_router.patch(
    "/esg-configuration",
    response_model=EsgConfigResponse,
    summary="Update ESG configuration",
)
def update_esg_configuration(
    payload: EsgConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(["system_admin"])
    ),
):
    config = db.get(EsgConfiguration, 1)

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ESG configuration not found.",
        )

    update_data = payload.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(config, field, value)

    # Validate weight sum
    env_w = config.environmental_weight
    soc_w = config.social_weight
    gov_w = config.governance_weight

    if abs((env_w + soc_w + gov_w) - 1.0) > 0.001:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "ESG weights must sum to 1.00. "
                f"Current sum: "
                f"{env_w + soc_w + gov_w:.2f}"
            ),
        )

    db.commit()
    db.refresh(config)

    return config
