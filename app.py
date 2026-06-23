import streamlit as st

st.set_page_config(
    page_title="HastaVaani",
    layout="wide"
)

st.title("HastaVaani")
st.subheader("AI-Powered Sign Language Communication Assistant")

# -------------------------
# Session State
# -------------------------
if "gesture_count" not in st.session_state:
    st.session_state.gesture_count = 0

if "sentence_count" not in st.session_state:
    st.session_state.sentence_count = 0

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("Controls")

if st.sidebar.button("Clear History"):
    st.session_state.history = []

# -------------------------
# Metrics
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Gestures Detected",
        st.session_state.gesture_count
    )

with col2:
    st.metric(
        "Sentences Spoken",
        st.session_state.sentence_count
    )

with col3:
    st.metric(
        "System Status",
        "Ready"
    )

# -------------------------
# Layout
# -------------------------
left, right = st.columns([2, 1])

with left:
    st.info(
        "Camera feed currently runs through main.py"
    )

with right:

    st.markdown("### Current Gesture")
    st.success("-")

    st.markdown("### Confidence")
    st.info("0%")

    st.markdown("### Session Analytics")

    st.write(
        f"Gestures: {st.session_state.gesture_count}"
    )

    st.write(
        f"Sentences: {st.session_state.sentence_count}"
    )

# -------------------------
# History
# -------------------------
st.markdown("---")

st.markdown("## Recent Gestures")

if not st.session_state.history:

    st.info(
        "No gestures detected yet."
    )

else:

    for item in reversed(
        st.session_state.history[-10:]
    ):
        st.write("•", item)