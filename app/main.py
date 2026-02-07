from fastapi import FastAPI, Query
import os
from os import getcwd
from uvicorn import run
import polars as pl
from duckdb import connect
from gym_membership_churn.app.schemas import MemberData, PaginatedItems

os.environ["POLARS_VERBOSE"] = "1"

#Path to the csv file 
csv_path = getcwd() + "/data/gym_members_dataset.csv"

duckdb_path = getcwd() + "/data/gym_members_dataset.db"

#Loading and Cleaning Data
df = pl.read_csv(source=csv_path)
df=df.with_columns(
    pl.col('Name').fill_null('Test Name'),
    pl.col('Age').fill_null(pl.col('Age').mean()),
        pl.col('Avg_Calories_Burned').fill_null(pl.col('Avg_Calories_Burned').mean()),
        pl.col('Total_Weight_Lifted_kg').fill_null(pl.col('Total_Weight_Lifted_kg').mean()),
        pl.col('Visits_Per_Month').fill_null(pl.col('Visits_Per_Month').mean())
    )

#Drop Null values
df_clean = df.drop_nulls(subset=["Join_Date"])

#Change Datatype to Date
df = df_clean.with_columns([
    pl.col("Join_Date").cast(pl.Date),
    pl.col("Last_Visit_Date").cast(pl.Date),
])

#Serving Raw Data via FastAPI

#Fast API object
app = FastAPI()

#Route
@app.get(path='/serving_raw_dataset')
def get_rawdata_as_json():
    df_as_json = df.to_dicts()
    return df_as_json

#DuckDB Integration

def create_table():
    #Save the dataframe in db 
    cursor=connect(database=duckdb_path)

    #SQL query to create a table
    sql_query = """
    CREATE OR REPLACE TABLE gym_membership_data AS (
        SELECT * 
        FROM df
    );
    """
    #Execute query
    result = cursor.sql(query=sql_query)
    cursor.close()

#Create duckdb table
create_table()

#Serving Aggregated Data

@app.get(path='/churn_by_membership_count')
def get_churn_data():
    cursor=connect(database=duckdb_path)
    churn_count=cursor.sql(query="""
                           
                        SELECT Membership_Type, SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS num_churns
                        FROM gym_membership_data
                        GROUP BY Membership_Type
                        ORDER BY num_churns DESC
                           
                        """)
    result=pl.from_arrow(churn_count).to_dicts() # type: ignore
    # Close your DuckDB connection
    cursor.close()
    return result

#Query Parameters and Validation
@app.get(path='/favorite-exercise-member-count')
def get_member_data(
    exercise: str = Query(
        default="Pull-ups",
        description="Allowed exercises are Pull-ups, Squats, Bench Press, Deadlift, Treadmill, Cycling"
    )
):
    cursor=connect(database=duckdb_path)
    query=("""
            SELECT Favorite_Exercise, COUNT(DISTINCT Member_ID) AS Total_Members
            FROM gym_membership_data
            WHERE Favorite_Exercise = ?
            GROUP BY Favorite_Exercise
        """
    )
    
    members_count=cursor.sql(query, params=[exercise])
    result=pl.from_arrow(members_count).to_dicts() # type: ignore
    # Close your DuckDB connection
    cursor.close()
    return result

#Pagination and Pydantic Response Models
@app.get(path='/data-using-pagination')
def get_paginated_date(
    page: int = Query(description='Exact page number', default=1, ge=1),
    page_size: int = Query(
        description='Exact number of members to be displayed on a page',
        default=10,
        ge=1,
        le=100
    )
):
    offset= (page - 1) * page_size
    cursor=connect(database=duckdb_path)

    #Get Total count
    total = cursor.execute("SELECT COUNT(*) FROM gym_membership_data").fetchone()
    total=total[0] if total else 0

    if total == 0:
        return PaginatedItems(
           MemberData=[],
           total=0,
           page=page,
           page_size=page_size
        )

    page_result=cursor.execute("""
            SELECT *
            FROM gym_membership_data
            LIMIT ? OFFSET ?
    """,
    [page_size,offset],
    ).fetchall()

    paginated_result=[MemberData(
        Member_ID=r[0], 
        Name=r[1], 
        Age=r[2], 
        Gender=r[3], 
        Address=r[4], 
        Phone_Number=r[5], 
        Membership_Type=r[6], 
        Join_Date=r[7], 
        Last_Visit_Date=r[8], 
        Favorite_Exercise=r[9], 
        Avg_Workout_Duration_Min=r[10], 
        Avg_Calories_Burned=r[11], 
        Total_Weight_Lifted_kg=r[12], 
        Visits_Per_Month=r[13], 
        Churn=r[14])
        for r in page_result]

    # pl.from_arrow(page_result).to_dicts() # type: ignore
    cursor.close()
    return PaginatedItems(
        MemberData=paginated_result,
        total=total,
        page=page,
        page_size=page_size,
    )


# Run function
run(app=app, host='0.0.0.0', port=8080)

