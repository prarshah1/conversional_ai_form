from pydantic import BaseModel, Field


class DashboardInfo(BaseModel):
    persona: str = Field(
        None,
        description="Persona & User Goal",
    )
    metrics: str = Field(
        None,
        description="Dimensions & Metrics needed for dahsboard",
    )
    sample_values: str = Field(
        None,
        description="sample values of data",
    )
