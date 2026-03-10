import streamlit as st
from streamlit_calendar import calendar
import time
st.set_page_config(page_title="Streamlit Calendar", layout="wide")

if "events" not in st.session_state:
    st.session_state.all_events = []

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Add New Event")
    with st.form("event_form",clear_on_submit=True):
        title = st.text_input("Event Title")
        date = st.date_input("Event Date")
        event_time = st.time_input("Event Time")
        submit = st.form_submit_button("Add Event")
        if submit:
            if not title:
                st.error("Please enter an event title.")        
            else:
                new_event = {
                    "title": title,
                    "start": event_time.strftime("%H:%M"),
                    'allDay': False
                }
                st.session_state.all_events.append(new_event)
                st.success(f"Event '{title}' added for {date} at {event_time}.")
with col2:
    st.subheader("Event Calendar")
    st.write("Add your events!")
    calendar(events=st.session_state.all_events,key="event_calendar")

    