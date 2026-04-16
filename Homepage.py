import streamlit as st
import datetime
import requests

st.set_page_config(page_title="App")

# Location and Weather Setup in Sidebar
with st.sidebar:
    st.header("📍 Location Settings")
    city = st.text_input("Enter a city", value="Charlottesville", key="sidebar_city")
    state = st.text_input("Enter a state (e.g. VA or Virginia)", value="VA", key="sidebar_state")
    city_with_state = f"{city}, {state}" if state.strip() else city

    state_abbrevs = {
        "al": "alabama", "ak": "alaska", "az": "arizona", "ar": "arkansas",
        "ca": "california", "co": "colorado", "ct": "connecticut", "de": "delaware",
        "fl": "florida", "ga": "georgia", "hi": "hawaii", "id": "idaho",
        "il": "illinois", "in": "indiana", "ia": "iowa", "ks": "kansas",
        "ky": "kentucky", "la": "louisiana", "me": "maine", "md": "maryland",
        "ma": "massachusetts", "mi": "michigan", "mn": "minnesota", "ms": "mississippi",
        "mo": "missouri", "mt": "montana", "ne": "nebraska", "nv": "nevada",
        "nh": "new hampshire", "nj": "new jersey", "nm": "new mexico", "ny": "new york",
        "nc": "north carolina", "nd": "north dakota", "oh": "ohio", "ok": "oklahoma",
        "or": "oregon", "pa": "pennsylvania", "ri": "rhode island", "sc": "south carolina",
        "sd": "south dakota", "tn": "tennessee", "tx": "texas", "ut": "utah",
        "vt": "vermont", "va": "virginia", "wa": "washington", "wv": "west virginia",
        "wi": "wisconsin", "wy": "wyoming"
    }

    @st.cache_data(ttl=86400)
    def geocode_city(city_name):
        clean_city = city_name.split(",")[0].strip()
        state_hint = city_name.split(",")[1].strip() if "," in city_name else None
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={clean_city}&count=10&language=en&format=json"
        try:
            response = requests.get(url, timeout=10)

            # Error codes
            if response.status_code == 401:
                return None, None, "API key is missing or invalid.", None
            elif response.status_code == 404:
                return None, None, "Geocoding endpoint not found.", None
            elif response.status_code == 429:
                return None, None, "API limit reached. Please wait a minute and try again.", None
            elif response.status_code == 500:
                return None, None, "The geocoding service is temporarily unavailable. Please try again later.", None
            elif response.status_code != 200:
                return None, None, f"Unexpected error (status {response.status_code}).", None

            data = response.json()
            results = data.get("results")

            # Empty results
            if not results:
                return None, None, f"No results found for '{city_name}'. Try a different spelling.", None

            if state_hint:
                state_hint_lower = state_hint.lower()
                # Expand abbreviation to full state name for better matching
                full_state = state_abbrevs.get(state_hint_lower, state_hint_lower)
                for r in results:
                    admin = (r.get("admin1") or "").lower()
                    if full_state in admin or admin.startswith(full_state):
                        return r["latitude"], r["longitude"], None, r.get("name", "")
                # State was provided but no match found
                return None, None, f"Could not find '{clean_city}' in '{state_hint}'. Check spelling or try a different state.", None

            # If no state provided and multiple results exist across different states, ask user to clarify
            if len(results) > 1:
                states_found = list(set(r.get("admin1", "") for r in results if r.get("country_code", "").lower() == "us"))
                if len(states_found) > 1:
                    state_list = ", ".join(sorted(states_found))
                    return None, None, f"'{clean_city}' exists in multiple states: {state_list}. Please enter a state to clarify.", None

            return results[0]["latitude"], results[0]["longitude"], None, results[0].get("name", "")

        except requests.exceptions.Timeout:
            return None, None, "Could not connect. Check your internet connection.", None
        except requests.exceptions.ConnectionError:
            return None, None, "Could not connect. Check your internet connection.", None
        except Exception as e:
            return None, None, f"Unexpected error: {str(e)}", None

    @st.cache_data(ttl=3600)
    
    def fetch_weather(lat, lon):
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,weathercode"
            f"&temperature_unit=fahrenheit"
            f"&forecast_days=7"
            f"&past_days=23"
        )
        try:
            response = requests.get(url, timeout=10)

            # Error codes
            if response.status_code == 401:
                return {"error": "API key is missing or invalid."}
            elif response.status_code == 404:
                return {"error": "No results found for your search."}
            elif response.status_code == 429:
                return {"error": "API limit reached. Please wait a minute and try again."}
            elif response.status_code == 500:
                return {"error": "The service is temporarily unavailable. Please try again later."}
            elif response.status_code != 200:
                return {"error": f"Unexpected error (status {response.status_code})."}

            data = response.json()

            if not data.get("daily"):
                return {"error": "Your search returned no results. Try broader terms."}

            return data

        except requests.exceptions.Timeout:
            return {"error": "Could not connect. Check your internet connection."}
        except requests.exceptions.ConnectionError:
            return {"error": "Could not connect. Check your internet connection."}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        with st.spinner(f"Looking up {city_with_state}..."):
            lat, lon, geo_error, matched_city = geocode_city(city_with_state)

        if geo_error:
            st.error(geo_error)
        elif matched_city and city.strip().lower() not in matched_city.lower() and matched_city.lower() not in city.strip().lower():
            st.error(f"Could not find '{city}'. Did you mean '{matched_city}'?")
        else:
            with st.spinner("Fetching weather..."):
                weather_data = fetch_weather(lat, lon)
            if "error" in weather_data:
                st.error(weather_data["error"])
            else:
                # Save to session state so all pages can access it
                st.session_state.weather_data = weather_data
                st.session_state.city_with_state = city_with_state
                st.session_state.lat = lat
                st.session_state.lon = lon
                st.success(f"📍 {city_with_state}")

# Main Page
st.title("OutfitPlannerz")

# Show current location and instructions
if "city_with_state" in st.session_state:
    st.info(f"📍 Current location: **{st.session_state.city_with_state}**. To change, update the city and state in the left sidebar.")
else:
    st.warning("📍 No location set. Enter your city and state in the left sidebar to get started!")

today_outfit = st.session_state.get("today_outfit", None)
if today_outfit:
    st.subheader(f"Today's Outfit: {today_outfit}")
else:
    st.subheader("Today's Outfit: Visit the Planner to get today's recommendation!")

# Show today's weather from session state if available
if "weather_data" in st.session_state:
    daily = st.session_state.weather_data.get("daily", {})
    today_str = datetime.date.today().isoformat()
    if today_str in daily.get("time", []):
        idx = daily["time"].index(today_str)
        temp = daily["temperature_2m_max"][idx]
        st.write(f"Today's Weather: {temp}°F")
    else:
        st.write("Today's Weather: Sunny, 85°F")
else:
    st.write("Today's Weather: Sunny, 85°F")

st.write("No events scheduled for today. Check your calendar for upcoming events and outfit recommendations!")

st.subheader("Upcoming Events")
if "events" not in st.session_state or not st.session_state.events:
    pass
else:
    today = datetime.date.today()
    upcoming = []

    for e in st.session_state.events:
        try:
            event_date = datetime.date.fromisoformat(e["start"].split("T")[0])
            if event_date >= today:
                upcoming.append((event_date, e))
        except ValueError:
            continue

    upcoming.sort(key=lambda x: x[0])

    if upcoming:
        if "visible_events" not in st.session_state:
            st.session_state.visible_events = {e["title"]: True for _, e in upcoming}
        for _, e in upcoming:
            if e["title"] not in st.session_state.visible_events:
                st.session_state.visible_events[e["title"]] = True

        displayed = [(d, e) for d, e in upcoming if st.session_state.visible_events.get(e["title"], True)]

        if displayed:
            for event_date, e in displayed:
                st.write(f"**{e['title']}** — {e['display']}")
        else:
            st.warning("Pick at least one event to display.")

        st.divider()

        with st.expander("⚙️ Advanced Settings"):
            st.write("Select which events to display:")
            for _, e in upcoming:
                new_value = st.checkbox(
                    e["title"], value=st.session_state.visible_events[e["title"]], key=f"check_{e['title']}"
                )
                if new_value != st.session_state.visible_events[e["title"]]:
                    st.session_state.visible_events[e["title"]] = new_value
                    st.rerun()
    else:
        st.info("No upcoming events. Head to the Calendar to add some!")