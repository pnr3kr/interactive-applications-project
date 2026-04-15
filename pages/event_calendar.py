import streamlit as st
from streamlit_calendar import calendar
import datetime
from time import sleep

st.set_page_config(page_title="Streamlit Calendar", layout="wide")

if "events" not in st.session_state:
    st.session_state.events = []

if "toast_message" not in st.session_state:
    st.session_state.toast_message = None

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Homepage", "App", "Calendar", "Analytics"])

if page == "Homepage":
    st.title("Welcome to the Streamlit Calendar App!")
    st.write("Use the sidebar to navigate to different pages.")

if page == "App":
    st.title("App Page")
    st.write("This is the app page. You can add your events in the calendar section.")

if page == "Analytics":
    st.title("Analytics Page")
    st.write("This is the analytics page. You can analyze your events here.")

if page == "Calendar":
    if st.session_state.toast_message:
        st.toast(st.session_state.toast_message)
        st.session_state.toast_message = None

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Add New Event")
        tab1, tab2 = st.tabs(["Add Event", "Delete Event"])

        with tab1:
            if 'date' not in st.session_state:
                st.session_state.date = datetime.date.today()
            if 'end_date' not in st.session_state:
                st.session_state.end_date = datetime.date.today()
            if 'event_title' not in st.session_state:
                st.session_state.event_title = "new event"
            if 'time' not in st.session_state:
                st.session_state.time = None
            if "all_day" not in st.session_state:
                st.session_state.all_day = True

            all_day = st.toggle("All Day", key="all_day")

            with st.form("event_form", clear_on_submit=False):
                title = st.text_input("Event Title", key="event_title")
                start_date = st.date_input("Start Date", key="date")
                end_date = st.date_input("End Date", key="end_date")
                if not all_day:
                    event_time = st.time_input("Event Time", key="time")
                else:
                    event_time = None

                submit = st.form_submit_button("Add Event")

            if submit:
                if end_date < start_date:
                    st.error("End date cannot be before the start date.")
                elif title.strip():
                    if all_day:
                        start_time = start_date.strftime("%Y-%m-%d")
                        start_display = start_date.strftime("%Y-%m-%d")
                    else:
                        start_time = f"{start_date}T{event_time}"
                        start_display = f"{start_date} at {event_time}"
                    new_event = {
                        "title": title,
                        "start": start_time,
                        "end": end_date.strftime("%Y-%m-%d"),
                        "display": start_display
                    }
                    if new_event not in st.session_state.events:
                        st.session_state.events.append(new_event)
                        st.session_state.toast_message = f"Added '{title}'! 🎉"
                        st.rerun()
                    else:
                        st.warning("This event already exists in your calendar.")
                else:
                    st.error("Title required.")

        with tab2:
            if st.session_state.events:
                with st.form("delete_form"):
                    event_options = [f"{e['title']} ({e['display']})" for e in st.session_state.events]
                    event_to_delete = st.multiselect("Select event to remove:", event_options)
                    delete_submit = st.form_submit_button("Delete Selected Event", type="primary")
                    if delete_submit:
                        if event_to_delete:
                            st.session_state.events = [
                                e for e in st.session_state.events
                                if f"{e['title']} ({e['display']})" not in event_to_delete
                            ]
                            st.session_state.toast_message = f"Removed {', '.join(event_to_delete)}! 🗑️"
                            sleep(1)
                            st.rerun()
                        else:
                            st.warning("Please select at least one event to delete.")
            else:
                st.info("No events to remove.")

    with col2:
        st.subheader("Event Calendar")
        st.write("Add your events!")
        if not st.session_state.events:
            st.info("Your calendar is currently empty.")

        options = {
            "initialView": "dayGridMonth",
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": ""
            }
        }
        calendar(events=st.session_state.events, options=options, key="calendar")