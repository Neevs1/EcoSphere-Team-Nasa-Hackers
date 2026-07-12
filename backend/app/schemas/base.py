from pydantic import BaseModel, ConfigDict


class ORMBaseModel(BaseModel):
    """
    Base class for all Pydantic schemas.

    from_attributes=True allows Pydantic response schemas
    to read values directly from SQLAlchemy model objects.

    extra="forbid" rejects unexpected fields in request data.
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )
