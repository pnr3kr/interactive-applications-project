import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Analytics")
st.divider()

# Read from session state set in Homepage.py sidebar
weather_data = st.session_state.get("weather_data", None)
city_with_state = st.session_state.get("city_with_state", "Charlottesville, VA")

forecast_days = st.slider("Days of history to show", min_value=7, max_value=30, value=14, key="forecast_slider")

if not weather_data:
    st.warning("No weather data found. Please set your location in the sidebar on the Homepage.")
    st.stop()

if "error" in weather_data:
    st.error(weather_data["error"])
    st.stop()

st.success(f"Weather data loaded for {city_with_state}!")

daily_data = weather_data.get("daily", {})
dates = daily_data.get("time", [])
temperatures = daily_data.get("temperature_2m_max", [])

# Filter dates/temperatures to only show the selected number of past days
if dates and temperatures:
    today_str = pd.Timestamp.today().strftime("%Y-%m-%d")
    filtered = [(d, t) for d, t in zip(dates, temperatures) if d <= today_str]
    filtered = filtered[-forecast_days:]
    dates = [f[0] for f in filtered]
    temperatures = [f[1] for f in filtered]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Max Temperature — Last {forecast_days} Days")

    if dates and temperatures:
        df_weather = pd.DataFrame({
            "Date": pd.to_datetime(dates),
            "Max Temperature (°F)": temperatures
        })
        fig_line = px.line(df_weather, x="Date", y="Max Temperature (°F)")
        fig_line.update_layout(
            xaxis=dict(tickformat="%b %d", nticks=6, tickangle=-30),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Weather data unavailable.")

with col2:
    st.subheader("Outfit Category Percentage Breakdown")

    outfit_log = st.session_state.get("outfit_log", {})

    if outfit_log:
        category_counts = pd.Series(list(outfit_log.values())).value_counts().reset_index()
        category_counts.columns = ["Category", "Count"]
        total = category_counts["Count"].sum()
        category_counts["Percentage"] = (category_counts["Count"] / total * 100).round(1)
        outfit_data = category_counts
    else:
        st.info("No outfit data yet. Visit the Planner to log outfits!")
        outfit_data = None

    if outfit_data is not None:
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
        st.dataframe(
            outfit_data[["Category", "Count", "Percentage"]].rename(columns={"Percentage": "Percentage (%)"}),
            use_container_width=True,
            hide_index=True
        )