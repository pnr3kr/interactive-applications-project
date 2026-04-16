import streamlit as st
from time import sleep
from datetime import datetime

st.title("Interactive Outfit Planner")
st.divider()
st.header('Choose the day of the week')

# --- Read weather data from session state set in Homepage.py sidebar ---
weather_data = st.session_state.get("weather_data", None)
city_with_state = st.session_state.get("city_with_state", "Charlottesville, VA")

# Initialize outfit log in session state for Analytics tracking
if "outfit_log" not in st.session_state:
    st.session_state.outfit_log = {}

def get_weather_description(code):
    if code == 0:
        return "Clear sky ☀️"
    elif code in [1, 2, 3]:
        return "Partly cloudy ⛅"
    elif code in [45, 48]:
        return "Foggy 🌫️"
    elif code in [51, 53, 55, 61, 63, 65]:
        return "Rainy 🌧️"
    elif code in [71, 73, 75]:
        return "Snowy ❄️"
    elif code in [80, 81, 82]:
        return "Showers 🌦️"
    elif code in [95, 96, 99]:
        return "Thunderstorm ⛈️"
    else:
        return "Mixed conditions 🌤️"

def recommend_outfit(temp_max, weather_code):
    """Recommend an outfit based on temperature and weather code."""
    # Rainy or stormy → rain outfit
    if weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]:
        return "Waterproof jacket, jeans, and rain boots"
    # Snowy → warm/heavy outfit
    elif weather_code in [71, 73, 75]:
        return "Heavy coat, scarf, warm boots, and gloves"
    # Hot (80°F+)
    elif temp_max >= 80:
        return "Light t-shirt, shorts, and sandals"
    # Warm (65-79°F)
    elif temp_max >= 65:
        return "Light blouse, tailored pants, and loafers"
    # Mild (50-64°F)
    elif temp_max >= 50:
        return "Denim jacket, jeans, and sneakers"
    # Cold (below 50°F)
    else:
        return "Heavy coat, scarf, warm boots, and gloves"

def get_outfit_category(temp_max, weather_code):
    """Assign a category based on temp and weather for Analytics tracking."""
    # Heavy if rainy, snowy, stormy, or cold
    if weather_code in [51, 53, 55, 61, 63, 65, 71, 73, 75, 80, 81, 82, 95, 96, 99]:
        return "Heavy"
    elif temp_max >= 80:
        return "Light"
    elif temp_max >= 65:
        return "Medium"
    else:
        return "Heavy"

def reset_outfits():
    for d, _ in future:
        st.session_state[f"{d}_use_suggested"] = True
        st.session_state[f"{d}_custom_outfit"] = ""
    st.toast("Filters cleared!")
    sleep(3)

if not weather_data:
    st.warning("No weather data found. Please set your location in the sidebar on the Homepage.")
    st.stop()

daily = weather_data.get("daily", {})
dates = daily.get("time", [])
temp_maxes = daily.get("temperature_2m_max", [])
temp_mins = daily.get("temperature_2m_min", [])
wind_speeds = daily.get("windspeed_10m_max", [])
precips = daily.get("precipitation_sum", [])
weather_codes = daily.get("weathercode", [])

# Get only the next 7 days from today
today_str = datetime.today().strftime("%Y-%m-%d")
future = [(d, i) for i, d in enumerate(dates) if d >= today_str][:7]

if not future:
    st.warning("No upcoming forecast data available.")
    st.stop()

# Build tab labels from real dates
tab_labels = [
    f"{datetime.strptime(d, '%Y-%m-%d').strftime('%A')} {datetime.strptime(d, '%Y-%m-%d').strftime('%-m/%-d')}"
    for d, _ in future
]

st.button("🔄 Reset All Outfits", on_click=reset_outfits)

# Initialize session state for each day
for d, _ in future:
    if f"{d}_use_suggested" not in st.session_state:
        st.session_state[f"{d}_use_suggested"] = True
    if f"{d}_custom_outfit" not in st.session_state:
        st.session_state[f"{d}_custom_outfit"] = ""

tabs = st.tabs(tab_labels)

for tab, (date_str, idx) in zip(tabs, future):
    with tab:
        temp_max = temp_maxes[idx]
        temp_min = temp_mins[idx] if temp_mins else None
        wind = wind_speeds[idx] if wind_speeds else None
        precip = precips[idx] if precips else None
        code = weather_codes[idx]
        description = get_weather_description(code)
        day_name = datetime.strptime(date_str, '%Y-%m-%d').strftime('%A')
        date_display = datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %-d, %Y')

        st.subheader(f"{day_name} — {date_display}")

        col1, col2, col3 = st.columns(3)
        col1.metric("High", f"{temp_max}°F")
        if temp_min:
            col2.metric("Low", f"{temp_min}°F")
        if wind:
            col3.metric("Wind", f"{wind} mph")

        st.write(f"**Weather:** {description}")
        if precip is not None:
            st.write(f"**Precipitation:** {precip} mm")

        # Check for events on this day from the calendar
        events_today = [
            e for e in st.session_state.get("events", [])
            if e.get("start", "").split("T")[0] == date_str
        ]
        if events_today:
            st.write(f"**Occasion:** {events_today[0]['title']}")

        recommended = recommend_outfit(temp_max, code)
        st.write(f"**Recommended Outfit:** {recommended}")

        st.divider()

        # key allows Streamlit to differentiate between checkboxes for each day
        use_suggested = st.checkbox(
            "Use suggested outfit",
            key=f"{date_str}_use_suggested"
        )

        # Determine outfit category for Analytics tracking
        category = get_outfit_category(temp_max, code)

        if not use_suggested:
            custom = st.text_input(
                "Enter your custom outfit:",
                key=f"{date_str}_custom_outfit",
                placeholder="e.g. White t-shirt, cargo pants, and white sneakers"
            )
            if not custom.strip():
                st.warning("Pick at least one outfit — enter a custom outfit above.")
            else:
                st.success(f"Custom outfit set: {custom}")
                # Log the category for this day for Analytics tracking
                st.session_state.outfit_log[date_str] = category
                # Save today's outfit to session state for Homepage
                if date_str == today_str:
                    st.session_state.today_outfit = custom
        else:
            st.info(f"Outfit selected: {recommended}")
            # Log the category for this day for Analytics tracking
            st.session_state.outfit_log[date_str] = category
            # Save today's outfit to session state for Homepage
            if date_str == today_str:
                st.session_state.today_outfit = recommended