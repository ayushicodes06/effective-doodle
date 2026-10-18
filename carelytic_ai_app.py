import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="CARELYTIC AI",
    page_icon="🌿",
    layout="wide",
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# Navigation pages
PAGES = [
    "Home",
    "Well-being Check-in",
    "My Dashboard",
    "Support Assistant",
    "Privacy",
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }

        .hero {
            padding: 35px;
            border-radius: 18px;
            background: linear-gradient(120deg, #e3f6ed, #eef3ff);
            margin-bottom: 25px;
        }

        .hero h1 {
            color: #153b35;
            font-size: 42px;
        }

        .hero p {
            color: #344b48;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("🌿 CARELYTIC AI")
st.sidebar.caption("Your personal well-being companion")

selected_page = st.sidebar.radio(
    "Navigation",
    PAGES,
    index=PAGES.index(st.session_state.page)
    if st.session_state.page in PAGES
    else 0,
)

st.session_state.page = selected_page
page = selected_page

# -----------------------------
# INSIGHT ENGINE
# -----------------------------
def generate_insights(sleep, stress, energy, screen_time):
    insights = []
    suggestions = []

    if sleep < 7:
        insights.append(
            "Your reported sleep duration is below the usual "
            "7–9 hours recommended for most adults."
        )

        suggestions.append(
            "Consider keeping a consistent sleep and wake-up schedule."
        )

    else:
        insights.append(
            "Your reported sleep duration is within the usual "
            "adult sleep-duration recommendation."
        )

    if stress >= 7:
        insights.append(
            "You reported a high stress level today."
        )

        suggestions.append(
            "Try a short breathing exercise or take a break "
            "between study sessions."
        )

    elif stress >= 4:
        insights.append(
            "You reported a moderate stress level."
        )

        suggestions.append(
            "Break larger tasks into smaller, manageable steps."
        )

    else:
        insights.append(
            "You reported a relatively low stress level."
        )

    if energy <= 3:
        insights.append(
            "You reported low energy today."
        )

        suggestions.append(
            "Consider whether rest, hydration, meals, or a change "
            "in routine might help."
        )

    if screen_time >= 6:
        insights.append(
            "Your recreational screen time is relatively high."
        )

        suggestions.append(
            "Try scheduling screen-free breaks during your day."
        )

    if not suggestions:
        suggestions.append(
            "Continue observing your habits and maintaining a "
            "routine that works for you."
        )

    return insights, suggestions


# -----------------------------
# HOME PAGE
# -----------------------------
if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <h1>Understand yourself. Build healthier habits.</h1>
            <p>
                CARELYTIC AI helps students reflect on their sleep,
                stress, energy, and digital habits.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(
        "Welcome to your personal check-in 🌱"
    )

    st.write(
        "Small daily reflections can help you understand your habits "
        "and identify areas where you may want to make changes."
    )

    if st.button("Start My Check-in", type="primary"):
        st.session_state.page = "Well-being Check-in"
        st.rerun()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 😴 Sleep")
        st.write("Reflect on your sleep duration.")

    with col2:
        st.markdown("### 🧠 Stress")
        st.write("Record how stressed you feel.")

    with col3:
        st.markdown("### 📱 Digital habits")
        st.write(
            "Understand your recreational screen time."
        )

    st.info(
        "CARELYTIC AI is a self-reflection tool, "
        "not a medical diagnostic system."
    )


# -----------------------------
# CHECK-IN PAGE
# -----------------------------
elif page == "Well-being Check-in":

    st.title("Your Daily Well-being Check-in")

    st.write(
        "Answer honestly. There are no right or wrong answers."
    )

    with st.form("wellbeing_form"):

        sleep = st.slider(
            "How many hours did you sleep last night?",
            min_value=0.0,
            max_value=14.0,
            value=7.0,
            step=0.5,
        )

        stress = st.slider(
            "How stressed do you feel today?",
            min_value=1,
            max_value=10,
            value=5,
        )

        energy = st.slider(
            "How energetic do you feel today?",
            min_value=1,
            max_value=10,
            value=5,
        )

        screen_time = st.slider(
            "Daily recreational screen time (hours)",
            min_value=0.0,
            max_value=16.0,
            value=3.0,
            step=0.5,
        )

        mood = st.selectbox(
            "How are you feeling?",
            [
                "Calm",
                "Happy",
                "Okay",
                "Tired",
                "Overwhelmed",
                "Sad",
            ],
        )

        submitted = st.form_submit_button(
            "Generate My Insights",
            type="primary",
        )

    if submitted:

        record = {
            "Date": pd.Timestamp.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            "Sleep": sleep,
            "Stress": stress,
            "Energy": energy,
            "Screen Time": screen_time,
            "Mood": mood,
        }

        st.session_state.history.append(record)

        insights, suggestions = generate_insights(
            sleep,
            stress,
            energy,
            screen_time,
        )

        st.success(
            "Your check-in is complete!"
        )

        st.subheader(
            "Your Lifestyle Insights"
        )

        for insight in insights:
            st.write(f"• {insight}")

        st.subheader(
            "Suggested Next Steps"
        )

        for suggestion in suggestions:
            st.write(f"✓ {suggestion}")

        st.caption(
            "These observations are based on your responses and do not "
            "constitute a medical assessment."
        )


# -----------------------------
# DASHBOARD PAGE
# -----------------------------
elif page == "My Dashboard":

    st.title(
        "My Well-being Dashboard"
    )

    if len(st.session_state.history) == 0:

        st.info(
            "You have no check-in history yet. Complete your first "
            "check-in to see your dashboard."
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Average Sleep",
                f"{df['Sleep'].mean():.1f} hrs",
            )

        with col2:
            st.metric(
                "Average Stress",
                f"{df['Stress'].mean():.1f}/10",
            )

        with col3:
            st.metric(
                "Average Energy",
                f"{df['Energy'].mean():.1f}/10",
            )

        with col4:
            st.metric(
                "Average Screen Time",
                f"{df['Screen Time'].mean():.1f} hrs",
            )

        st.divider()

        chart_type = st.selectbox(
            "Choose a metric",
            [
                "Sleep",
                "Stress",
                "Energy",
                "Screen Time",
            ],
        )

        fig = px.line(
            df,
            x="Date",
            y=chart_type,
            markers=True,
            title=f"{chart_type} Over Time",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.subheader(
            "Your Check-in History"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download My Check-in History",
            data=csv_data,
            file_name="my_wellbeing_history.csv",
            mime="text/csv",
        )


# -----------------------------
# SUPPORT ASSISTANT
# -----------------------------
elif page == "Support Assistant":

    st.title(
        "Your Support Assistant 💚"
    )

    st.write(
        "Ask for general suggestions about study routines, relaxation, "
        "breaks, or healthy habits."
    )

    st.info(
        "This initial assistant uses predefined responses. "
        "It is not connected to an AI model yet."
    )

    question = st.text_input(
        "What would you like help with?"
    )

    if st.button("Get Suggestion"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            q = question.lower()

            if any(
                word in q
                for word in (
                    "stress",
                    "overwhelmed",
                    "pressure",
                )
            ):

                answer = (
                    "Try pausing for a moment, taking slow comfortable "
                    "breaths, and identifying one small task you can "
                    "complete next. If stress persists, consider talking "
                    "with someone you trust or a qualified professional."
                )

            elif any(
                word in q
                for word in (
                    "sleep",
                    "tired",
                    "fatigue",
                )
            ):

                answer = (
                    "Consider keeping a consistent sleep schedule, "
                    "allowing enough time for rest, and limiting stimulating "
                    "activities close to bedtime."
                )

            elif any(
                word in q
                for word in (
                    "study",
                    "focus",
                    "distraction",
                )
            ):

                answer = (
                    "Choose one small study goal, silence non-essential "
                    "notifications, and work in a manageable session "
                    "followed by a break."
                )

            elif any(
                word in q
                for word in (
                    "screen",
                    "phone",
                    "mobile",
                )
            ):

                answer = (
                    "Try tracking when you use your phone, turning off "
                    "unnecessary notifications, and scheduling short "
                    "screen-free periods."
                )

            else:

                answer = (
                    "Start by identifying what you need most right now: "
                    "rest, a short break, help with a task, or a conversation "
                    "with someone you trust."
                )

            st.markdown(
                "### A suggestion for you"
            )

            st.write(answer)


# -----------------------------
# PRIVACY PAGE
# -----------------------------
elif page == "Privacy":

    st.title(
        "Privacy & Data Control"
    )

    st.write(
        "This prototype keeps check-in history in your current Streamlit "
        "session. It does not save that history to a permanent database."
    )

    st.write(
        "Avoid entering names, contact details, or other identifying "
        "information into this prototype."
    )

    if st.button(
        "Delete My Current Session History"
    ):

        st.session_state.history = []

        st.success(
            "The check-in history stored in this session was deleted."
        )

        st.rerun()

    st.caption(
        "This prototype does not replace professional medical or "
        "mental-health care."
    )


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "CARELYTIC AI | Student Well-being Prototype | "
    "Built for learning and experimentation"
)