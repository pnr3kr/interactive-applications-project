import streamlit as st
from time import sleep


st.title("Outfit Builder")
st.header("The clothing items you select will be excluded from your outfit recommendations")

if "step" not in st.session_state:
    st.session_state.step = 1

if "selected_shoes" not in st.session_state:
    st.session_state.selected_shoes = []

if "selected_shirts" not in st.session_state:
    st.session_state.selected_shirts = []

if "selected_pants" not in st.session_state:
    st.session_state.selected_pants = []

# --- Step indicator ---
st.progress(min(st.session_state.step, 3) / 3)
st.caption(f"Step {st.session_state.step} of 3")

st.divider()

# --- Step 1: Shoes ---
if st.session_state.step == 1:
    st.subheader("👟 Step 1: Select Your Shoe to be removed")
    shoe_options = [
        "Sneakers", "Loafers", "Boots", "Sandals",
        "Heels", "Oxfords", "Slip-ons", "Rain Boots"
    ]
    st.session_state.selected_shoes = st.multiselect(
        "Choose your shoes:",
        shoe_options,
        default=st.session_state.selected_shoes
    )
    if not st.session_state.selected_shoes:
        st.warning("Please select at least one shoe type.")

    if st.button("Next → Shirts", disabled=not st.session_state.selected_shoes):
        with st.spinner("Moving to shirts..."):
            sleep(1.5)
        st.session_state.step = 2
        st.rerun()

# --- Step 2: Shirts ---
elif st.session_state.step == 2:
    st.subheader("👕 Step 2: Select Your Shirts to be excluded")
    shirt_options = [
        "T-Shirt", "Button-Up", "Polo", "Hoodie",
        "Tank Top", "Blouse", "Flannel", "Turtleneck"
    ]
    st.session_state.selected_shirts = st.multiselect(
        "Choose your shirts:",
        shirt_options,
        default=st.session_state.selected_shirts
    )
    if not st.session_state.selected_shirts:
        st.warning("Please select at least one shirt type.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Shoes"):
            with st.spinner("Going back to shoes..."):
                sleep(1.5)
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next → Pants", disabled=not st.session_state.selected_shirts):
            with st.spinner("Moving to pants..."):
                sleep(1.5)
            st.session_state.step = 3
            st.rerun()

# --- Step 3: Pants ---
elif st.session_state.step == 3:
    st.subheader("👖 Step 3: Select Your Pants to be excluded")
    pants_options = [
        "Jeans", "Chinos", "Sweatpants", "Shorts",
        "Dress Pants", "Leggings", "Cargo Pants", "Joggers"
    ]
    st.session_state.selected_pants = st.multiselect(
        "Choose your pants:",
        pants_options,
        default=st.session_state.selected_pants
    )
    if not st.session_state.selected_pants:
        st.warning("Please select at least one pants type.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Shirts"):
            with st.spinner("Going back to shirts..."):
                sleep(1.5)
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("✅ Finish", disabled=not st.session_state.selected_pants):
            with st.spinner("Building your outfit..."):
                sleep(1.5)
            st.session_state.step = 4
            st.rerun()

# --- Step 4: Summary ---
elif st.session_state.step == 4:
    st.subheader("✅ Your Outfit Summary")
    st.success("These items will be excluded from your recommendations:")

    st.write("👟 **Shoes:**", ", ".join(st.session_state.selected_shoes))
    st.write("👕 **Shirts:**", ", ".join(st.session_state.selected_shirts))
    st.write("👖 **Pants:**", ", ".join(st.session_state.selected_pants))

    st.divider()

    if st.button("🔄 Start Over"):
        st.session_state.step = 1
        st.session_state.selected_shoes = []
        st.session_state.selected_shirts = []
        st.session_state.selected_pants = []
        st.rerun()