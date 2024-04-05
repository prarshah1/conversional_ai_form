from pydantic import BaseModel, Field


class DashboardInfo(BaseModel):
    persona: str = Field(
        None,
        description="Persona & User Goal or Role or Title, of the individual we are creating this dashboard for",
    )
    function: str = Field(
        None,
        enum=["IT", "HR", "Sales", "Data Science"],
        description="Which team is the dashboard for",
    )
    analysis_goal: str = Field(
        None,
        description="Enter the analysis to be done with data to create the dashboard",
    )
    dashboard_outcome: str = Field(
        None,
        description="Target outcome, reason for which we are creating the dashboard",
    )
    performance_metrics: str = Field(
        None,
        description="Array or list of Dimensions or Metrics needed for dashboard acceptance criteria, also can be called performance metrics. It can be list/array of multiple acceptance criteria",
    )
    additional_information: str = Field(
        None,
        description="Optional additional information, or any other information that does not fit other fields goes here ",
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
    due_date: str = Field(
        None,
        description="By what date do you want the dashboard completed or Due date",
    )
