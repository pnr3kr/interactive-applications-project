import streamlit as st

st.title("Interactive Outfit Planner")

st.divider()
st.header('choose the day of the week')

tab_monday, tab_tuesday, tab_wednesday, tab_thursday, tab_friday, tab_saturday, tab_sunday = st.tabs(['Monday', "Tuesday", 
"Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

with tab_monday:
    st.subheader("Monday")
    st.write("Weather: Sunny, 25°C")
    st.write("Occasion: Casual workday")
    st.write("Recommended Outfit: Light blouse, tailored pants, and loafers.")

with tab_tuesday:
    st.subheader("Tuesday")
    st.write("Weather: Cloudy, 18°C")
    st.write("Occasion: Business meeting")
    st.write("Recommended Outfit: Blazer, pencil skirt, and heels.")

with tab_wednesday:
    st.subheader("Wednesday")
    st.write("Weather: Rainy, 15°C")
    st.write("Occasion: Casual day out")
    st.write("Recommended Outfit: Waterproof jacket, jeans, and rain boots.")

with tab_thursday:
    st.subheader("Thursday")
    st.write("Weather: Windy, 20°C")
    st.write("Occasion: Outdoor event")
    st.write("Recommended Outfit: Windbreaker, comfortable pants, and sneakers.")

with tab_friday:
    st.subheader("Friday")
    st.write("Weather: Partly cloudy, 22°C")
    st.write("Occasion: Weekend plans")
    st.write("Recommended Outfit: Denim jacket, shorts, and sandals.")

with tab_saturday:
    st.subheader("Saturday")
    st.write("Weather: Sunny, 26°C")
    st.write("Occasion: Social gathering")
    st.write("Recommended Outfit: Floral dress, sandals, and a straw hat.")

with tab_sunday:
    st.subheader("Sunday")
    st.write("Weather: Clear, 24°C")
    st.write("Occasion: Family outing")
    st.write("Recommended Outfit: Comfortable t-shirt, jeans, and sneakers.")