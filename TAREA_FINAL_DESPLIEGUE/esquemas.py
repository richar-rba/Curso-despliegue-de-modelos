from typing import Literal
from pydantic import BaseModel, Field

class EstudianteInput(BaseModel):

    Attendance_Rate: float = Field(..., ge=75, le=98)
    Homework_Completion: float = Field(..., ge=60, le=99)
    Quiz_Avg: float = Field(..., ge=40, le=90)
    Midterm_Score: float = Field(..., ge=40, le=80)
    Participation: float = Field(..., ge=4, le=10)
    Study_Hours_Week: float = Field(..., ge=3, le=19)
    Internet_Access: Literal["Yes", "No"]
    Family_Income_Level: Literal["High", "Medium", "Low"]
    Sleep_Hours: float = Field(..., ge=5, le=8)
    Math_Score: float = Field(..., ge=40, le=82)
    Commute_Time_Min: float = Field(..., ge=5, le=60)
    Class_Size: float = Field(..., ge=25, le=45)
    Teacher_Experience_Years: float = Field(..., ge=2, le=25)
    School_Type: Literal["Private", "Public"]
    Stress_Level: float = Field(..., ge=1, le=7)

class EstudianteOutput(BaseModel):
    nota_predicha: float