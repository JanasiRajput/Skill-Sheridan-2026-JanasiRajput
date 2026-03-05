from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String)
    robot_name = Column(String)
    category = Column(String)
    student_id = Column(String)
    name = Column(String)
    email = Column(String)
    description = Column(String)
    # members = Column(Integer, nullable=True)  # <-- Add this
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    student_id = Column(String)
    email = Column(String)
    rating = Column(Integer)
    comments = Column(Text)


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    team_name = Column(String)
    robot_name = Column(String)
    category = Column(String)
    position = Column(String)
    remarks = Column(Text)