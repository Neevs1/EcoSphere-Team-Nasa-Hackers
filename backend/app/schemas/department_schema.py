from datetime import datetime

from pydantic import Field, field_validator

from app.schemas.base import ORMBaseModel


class DepartmentCreate(ORMBaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    code: str = Field(
        min_length=2,
        max_length=20,
    )

    head: str | None = Field(
        default=None,
        max_length=100,
    )

    parent_department_id: int | None = Field(
        default=None,
        gt=0,
    )

    employee_count: int = Field(
        default=0,
        ge=0,
    )

    status: bool = True

    @field_validator("name", "code", "head")
    @classmethod
    def remove_extra_spaces(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return value.strip()

    @field_validator("code")
    @classmethod
    def uppercase_code(
        cls,
        value: str,
    ) -> str:
        return value.upper()


class DepartmentUpdate(ORMBaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )

    head: str | None = Field(
        default=None,
        max_length=100,
    )

    parent_department_id: int | None = Field(
        default=None,
        gt=0,
    )

    employee_count: int | None = Field(
        default=None,
        ge=0,
    )

    status: bool | None = None

    @field_validator("name", "code", "head")
    @classmethod
    def remove_extra_spaces(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return value.strip()

    @field_validator("code")
    @classmethod
    def uppercase_code(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return value.upper()


class DepartmentResponse(ORMBaseModel):
    id: int
    name: str
    code: str
    head: str | None = None
    parent_department_id: int | None = None
    employee_count: int
    status: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
