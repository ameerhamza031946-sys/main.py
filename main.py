import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('dailyActivity_merged.csv')
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])
    return df

df = load_data()

# Title
st.title('Daily Activity Dashboard')

# Summary Statistics
st.header('Summary Statistics')
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Average Steps', f"{df['TotalSteps'].mean():.0f}")
with col2:
    st.metric('Average Calories', f"{df['Calories'].mean():.0f}")
with col3:
    st.metric('Average Distance (km)', f"{df['TotalDistance'].mean():.2f}")
with col4:
    st.metric('Average Sedentary Minutes', f"{df['SedentaryMinutes'].mean():.0f}")

# Data Overview
st.header('Data Overview')
st.dataframe(df.head())

# Charts
st.header('Activity Trends')

# Line chart for Total Steps over time
fig_steps = px.line(df, x='ActivityDate', y='TotalSteps', title='Total Steps Over Time')
st.plotly_chart(fig_steps)

# Line chart for Calories over time
fig_calories = px.line(df, x='ActivityDate', y='Calories', title='Calories Burned Over Time')
st.plotly_chart(fig_calories)

# Bar chart for Activity Minutes
activity_cols = ['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']
df_activity = df.groupby('ActivityDate')[activity_cols].mean().reset_index()
fig_activity = px.bar(df_activity, x='ActivityDate', y=activity_cols, title='Average Activity Minutes per Day')
st.plotly_chart(fig_activity)

# Scatter plot: Steps vs Calories
fig_scatter = px.scatter(df, x='TotalSteps', y='Calories', title='Steps vs Calories')
st.plotly_chart(fig_scatter)

# Filter by User ID
st.header('Filter by User ID')
user_ids = df['Id'].unique()
selected_id = st.selectbox('Select User ID', user_ids)
df_filtered = df[df['Id'] == selected_id]

st.subheader(f'Activity for User {selected_id}')
fig_user_steps = px.line(df_filtered, x='ActivityDate', y='TotalSteps', title='Total Steps Over Time')
st.plotly_chart(fig_user_steps)
