import streamlit as st
import requests
import plotly.express as px
import pandas as pd

st.title("Analytics")

st.divider()

# Function to fetch weather data and cache to avoid repeated API calls
@st.cache_data(ttl=3600)
def get_historical_weather(lat=38.0293, lon=-78.4767):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,weathercode"
        f"&temperature_unit=fahrenheit"
        f"&forecast_days=7"
        f"&past_days=23"
    )
    response = requests.get(url)
    return response.json()

weather_data = get_historical_weather()
daily_data = weather_data.get("daily", {})
dates = daily_data.get("time", [])
temperatures = daily_data.get("temperature_2m_max", [])

col1, col2 = st.columns(2)
 
with col1:
    st.subheader("Average Temperature over last 30 days")
 
    if dates and temperatures:
        df_weather = pd.DataFrame({"Date": pd.to_datetime(dates), "Max Temperature (°F)": temperatures})
        fig_line = px.line(df_weather, x="Date", y="Max Temperature (°F)")
        fig_line.update_layout(
            xaxis=dict(
                tickformat="%b %d",
                nticks=6,
                tickangle=-30
            ),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Weather data unavailable.")
 
with col2:
    st.subheader("Outfit Category Percentage Breakdown")
with col2:
    st.subheader("Outfit Category Percentage Breakdown")

    # Sample outfit category data and replace with session state data if tracked
    outfit_data = pd.DataFrame({
        "Category": ["Light", "Medium", "Heavy", "Event"],
        "Percentage": [40, 30, 13, 17]
    })

    fig = px.pie(
        outfit_data,
        names="Category",
        values="Percentage",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(showlegend=True, margin=dict(t=20, b=20, l=20, r=20))

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Outfit Category Counts")

    # Count column from percentages for now (out of 100 sample outfits)
    outfit_data["Count"] = outfit_data["Percentage"].astype(int)
    st.dataframe(
        outfit_data[["Category", "Count", "Percentage"]].rename(columns={"Percentage": "Percentage (%)"}),
        use_container_width=True,
        hide_index=True
    )
