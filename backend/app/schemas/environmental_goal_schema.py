from datetime import date

from pydantic import Field, model_validator

from app.schemas.base import ORMBaseModel


class EnvironmentalGoalCreate(ORMBaseModel):
    department_id: int = Field(gt=0)

    goal_name: str = Field(
        min_length=2,
        max_length=200,
    )

    target_value: float = Field(
        ge=0,
    )

    achieved_value: float = Field(
        default=0,
        ge=0,
    )

    target_date: date

    status: bool = True

    @model_validator(mode="after")
    def validate_goal_values(self):
        if self.achieved_value > self.target_value:
            raise ValueError(
                "achieved_value cannot be greater than target_value."
            )

        return self


class EnvironmentalGoalUpdate(ORMBaseModel):
    department_id: int | None = Field(
        default=None,
        gt=0,
    )

    goal_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    target_value: float | None = Field(
        default=None,
        ge=0,
    )

    achieved_value: float | None = Field(
        default=None,
        ge=0,
    )

    target_date: date | None = None

    status: bool | None = None


class EnvironmentalGoalResponse(ORMBaseModel):
    id: int
    department_id: int | None = None
    goal_name: str
    target_value: float | None = None
    achieved_value: float | None = None
    target_date: date | None = None
    status: bool
