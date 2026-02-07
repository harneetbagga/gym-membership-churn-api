from datetime import date
from pydantic import BaseModel
from typing import List

class MemberData(BaseModel):
    Member_ID: int
    Name: str
    Age: float
    Gender: str
    Address: str
    Phone_Number: str
    Membership_Type: str
    Join_Date: date
    Last_Visit_Date: date
    Favorite_Exercise: str
    Avg_Workout_Duration_Min: int
    Avg_Calories_Burned: float
    Total_Weight_Lifted_kg: float
    Visits_Per_Month: float
    Churn: str

class PaginatedItems(BaseModel):
    MemberData: List[MemberData]
    total: int
    page: int
    page_size: int

