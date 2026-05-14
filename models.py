from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
import datetime

class Team(Base):
    __tablename__ = "Teams"
    TeamID = Column(Integer, primary_key=True, autoincrement=True)
    TeamName = Column(String(50), nullable=False, unique=True)

class User(Base):
    __tablename__ = "Users"
    UserID = Column(Integer, primary_key=True)
    FullName = Column(String(100), nullable=False, unique=True)
    Email = Column(String(100))
    Team = Column(String(50), ForeignKey("Teams.TeamName"))

class IncidentTicket(Base):
    __tablename__ = "INCIDENT_TICKETS"

    Ticket_Number = Column(String(20), primary_key=True)
    Status = Column(String(30))
    Priority = Column(String(10))
    Company = Column(String(100))
    Project = Column(String(100))
    Team = Column(String(50), ForeignKey("Teams.TeamName"))
    Assigned_Person = Column(String(100), ForeignKey("Users.FullName"))
    Service = Column(String(100))
    Description = Column(Text)
    Notes = Column(Text)
    Resolution = Column(Text)
    Cat_T1 = Column(String(50))
    Cat_T2 = Column(String(50))
    Cat_T3 = Column(String(50))
    Submit_Datetime = Column(DateTime, default=datetime.datetime.utcnow)
    Resolved_Datetime = Column(DateTime, nullable=True)
    Closed_Datetime = Column(DateTime, nullable=True)
    Last_Modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    Estimated_Resolution = Column(DateTime, nullable=True)
    Resolution_Category = Column(String(50))
    Pending_Duration = Column(Integer)