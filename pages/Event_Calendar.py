import streamlit as st
from streamlit_calendar import calendar
import time
import datetime
st.set_page_config(page_title="Streamlit Calendar", layout="wide")

if "events" not in st.session_state:
    st.session_state.events = []

def requests():
    if 'requests_made' not in st.session_state:
        st.session_state.requests_made = 0
    st.session_state.requests_made += 1
    if st.session_state.requests_made > 20:
        return '429'
    if not st.session_state.requests_made:
        return '200'
    return 'success'

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Add New Event")
    tab1,tab2=st.tabs(["Add Event", "Delete Event"])
    with tab1:
        if 'date' not in st.session_state:
            st.session_state.date=datetime.date.today()
        if 'event_title' not in st.session_state:
            st.session_state.event_title=""
        if 'time' not in st.session_state:
            st.session_state.time=None
        if "all_day" not in st.session_state:
            st.session_state.all_day=True
        #all_day key allows users to specify if the event is an all-day event or has a specific time. If all_day is True, the time input will be hidden and the event will be treated as an all-day event. If False, the user can specify a time for the event. This provides flexibility for different types of events in the calendar.
        all_day=st.toggle("All Day", key="all_day")

        with st.form("event_form", clear_on_submit=False):
            #key below allows Streamlit to differentiate between different events
            title = st.text_input("Event Title", key="event_title")
            #key below allows Streamlit to differentiate between different dates for each event
            date = st.date_input("Event Date", key="date")
            if not all_day:
                event_time=st.time_input("Event Time", key="time")
            else:
                event_time=None
            #key allows Streamlit to identify specific submit events
            submit = st.form_submit_button("Add Event",key='add_event_btn')
        if submit:
            if title.strip():
                if all_day:
                    start_time = date.strftime("%Y-%m-%d")
                else:
                    start_time = f"{date}T{event_time}"
                    start_display=f"{date} at {event_time}"
                new_event = {
                    "title": title,
                    "start": start_time,
                    "display": start_display if not all_day else date.strftime("%Y-%m-%d")
                    }
                if new_event not in st.session_state.events:
                    st.session_state.events.append(new_event)
                    st.success(f"Added {title}!")
                    st.rerun()  
                else:
                    st.warning("This event already exists in your calendar.")
            else:
                st.error("Title required.")
    with tab2:
        if st.session_state.events:
            with st.form("delete_form"):
                event_options = [f"{e['title']} ({e['display']})" for e in st.session_state.events]
                #key prevents widget conflicts with the add event form and when there are no events to delete
                event_to_delete = st.multiselect("Select event to remove:", event_options,key="event_to_delete")
                #key allows Streamlit to identify specific delete submitting events
                delete_submit = st.form_submit_button("Delete Selected Event", key="delete_event_btn", type="primary")
                if delete_submit:
                    if event_to_delete:
                        st.session_state.events = [e for e in st.session_state.events if f"{e['title']} ({e['display']})" not in event_to_delete]
                        st.success(f"Removed {', '.join(event_to_delete)}!")
                        st.rerun()
                    else:
                        st.warning("Error 404: Please select at least one event to delete.")
        else:
            st.info("No events to remove.")
        
with col2:
    st.subheader("Event Calendar")
    st.write("Add your events!")
    status=requests()
    options = {
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "" 
        }
    }
    if status == '429':
        st.error("Too many requests. Please wait a moment before trying again.")
    elif status == '200':
        st.info("Your calendar is currently empty (Status 200)")
    elif status == 'success': 
        calendar(events=st.session_state.events, options=options, key="calendar")