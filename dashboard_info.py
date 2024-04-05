from pydantic import BaseModel, Field


class DashboardInfo(BaseModel):
    persona_or_role_intended_for: str = Field(
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
    performance_metrics: str = Field(
        None,
        description="Metrics needed for dashboard acceptance criteria, it can also contain values and dimensions.",
    )
    additional_information: str = Field(
        "No",
        description="Optional additional information.",
    )
    requester_full_name: str = Field(
        None,
        description="Name of the requester of this dashboard",
    )
    urgency_or_priority: str = Field(
        None,
        enum=["Medium Priority", "Low Priority", "High Priority"],
        description="Urgency of the dashboard",
    )
    date: str = Field(
        None,
        description="deadline date",
    )
    dashboard_view_dimension: str = Field(
        None,
        description="Scale to be used for the dashboard, eg. date or days or time or values.",
    )
