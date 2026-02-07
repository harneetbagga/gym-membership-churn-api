import pandas as pd
import matplotlib.pyplot as plt
from os import getcwd
import datetime

#Path to the csv file 
csv_path = getcwd() + "/data/gym_members_dataset.csv"

df = pd.read_csv(csv_path)

#Drop rows where Member_ID or Age is missing
df_new = df.dropna(subset=['Member_ID','Age'])

#Fill missing Name entries with "Unknown" or "Test Name"
df_new=df_new.fillna({'Name':'Unknown'})

#Standardizing Data Types
df_new['Join_Date']=pd.to_datetime(df_new['Join_Date'], errors='coerce')
df_new['Last_Visit_Date']=pd.to_datetime(df_new['Last_Visit_Date'], errors='coerce')

#Data Consistency
# Loop through columns that are of type 'object'
for col in df_new.select_dtypes(include='object').columns:
    print(f"--- {col} ---")
    print(df_new[col].value_counts())
    print("\n") # Adds a blank line for readability

#New variable Membership Duration
df_new['Membership_Period_Days'] = (df_new['Last_Visit_Date']-df_new['Join_Date']).dt.days
print(df_new['Membership_Period_Days'].dtype)
print(df_new['Membership_Period_Days'])

#New variable Days_Since_Last_Visit Duration
df_new['Days_Since_Last_Visit'] = (pd.Timestamp.now()-df_new['Last_Visit_Date']).dt.days
print(df_new['Days_Since_Last_Visit'].dtype)
print(df_new['Days_Since_Last_Visit'])

#Univariate Analysis
#Plot a Histogram of Age

plt.hist(df_new['Age'],bins=20,color='skyblue', edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Age Distribution')
plt.savefig('Visualizations/age_histogram_plot.png')

#Plot a Pie Chart of Membership_Type
plt.figure(figsize=(8, 6))
labels = ['Quarterly', 'Monthly', 'Yearly']
plt.pie(df_new['Membership_Type'].value_counts(), labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Membership Type Distribution')
plt.savefig('Visualizations/membership_type.png')
plt.close()

#Separate the dataframe into two groups: churned_df and active_df.
churned_df = df_new[df_new['Churn']=='Yes']
active_df = df_new[df_new['Churn']=='No']

#Plot a Bar Chart comparing the Avg_WorkoutDurationMin for Churned vs. Active_members
avg_churned = churned_df['Avg_Workout_Duration_Min'].mean()
avg_active = active_df['Avg_Workout_Duration_Min'].mean()

categories = ['Churned', 'Active']
values = [avg_churned, avg_active]
colors = ['#ff9999', '#66b3ff']

plt.figure(figsize=(8, 6))
plt.bar(categories, values, color=colors, edgecolor='black')
plt.xlabel('Member Status')
plt.ylabel('Average Workout Duration (min)')
plt.title('Avg Workout Duration: Churned vs Active Members')
plt.savefig('Visualizations/workout_duration_comparison.png')
plt.close()

#Plot a Count Plot (stacked bar chart) showing Gender distribution split by Churn
gender_churn = df_new.groupby(['Gender', 'Churn']).size().unstack(fill_value=0)
plt.figure(figsize=(8, 6))
gender_churn.plot(kind='bar', stacked=True, color=['#66b3ff', '#ff9999'], edgecolor='black')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Gender Distribution by Churn Status')
plt.legend(title='Churn', labels=['No', 'Yes'])
plt.xticks(rotation=0)
plt.savefig('Visualizations/gender_churn_distribution.png')
plt.close()