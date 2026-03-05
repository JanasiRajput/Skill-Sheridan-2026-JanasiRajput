from typing import Optional

from pydantic import BaseModel, EmailStr

class TeamCreate(BaseModel):
    team_name: str
    robot_name: str
    category: str
    student_id: str
    name: str
    email: EmailStr
    description: str
    # members: Optional[int] = None  # <-- Add this


class FeedbackCreate(BaseModel):
    student_id: str
    email: EmailStr
    rating: int
    comments: str


class ResultCreate(BaseModel):
    team_name: str
    robot_name: str
    category: str
    position: str  # Winner, Runner-up, Third Place
    remarks: str