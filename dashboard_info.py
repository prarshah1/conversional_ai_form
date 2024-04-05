from pydantic import BaseModel, Field


class DashboardInfo(BaseModel):
    persona: str = Field(
        None,
        description="Persona or Role or Title, of the individual we are creating this or designing this dashboard for.",
    )
    team: str = Field(
        None,
        enum=["IT", "HR", "Sales", "Data Science"],
        description="Which team is the dashboard for? like HR or Sales or IT, etc.",
    )
    dashboard_outcome: str = Field(
        None,
        description="Target outcome, reason for which we are creating the dashboard or analysis goal.",
    )
    list_performance_metrics: str = Field(
        None,
        description="Array or list of Dimensions or Metrics needed for dashboard acceptance criteria, also can be called performance metrics. It can be list/array of multiple acceptance criteria.",
    )
    additional_information: str = Field(
        "No",
        description="Optional additional information.",
    )
    requester: str = Field(
        None,
        description="Who is the requester of this dashboard",
    )
    urgency: str = Field(
        None,
        enum=["Medium Priority", "Minor", "High Priority"],
        description="Urgency of the dashboard",
    )
    date: str = Field(
        None,
        description="By what date do you want the dashboard completed",
    )
