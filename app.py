import streamlit as st

from agent.agent import agent


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="UniMind AI",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99,102,241,.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(168,85,247,.14),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #050816,
                #0b1020,
                #111827
            );

        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background:
            rgba(5,8,22,.92) !important;

        border-right:
            1px solid rgba(255,255,255,.08);

        backdrop-filter: blur(18px);
    }

    .hero {
        text-align: center;
        padding: 40px 10px 25px 10px;
    }

    .hero-icon {
        font-size: 50px;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 850;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #a5b4fc,
                #c4b5fd,
                #93c5fd
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-top: 10px;
    }

    .glass {
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,.075),
                rgba(255,255,255,.025)
            );

        border:
            1px solid rgba(255,255,255,.08);

        border-radius: 22px;

        padding: 20px;

        backdrop-filter: blur(20px);

        box-shadow:
            0 20px 60px rgba(0,0,0,.25);
    }

    .metric {
        background:
            rgba(255,255,255,.045);

        border:
            1px solid rgba(255,255,255,.07);

        border-radius: 18px;

        padding: 18px;

        text-align: center;

        min-height: 110px;
    }

    .metric-icon {
        font-size: 25px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 800;
        margin-top: 5px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 12px;
    }

    .source {
        background:
            rgba(255,255,255,.045);

        border:
            1px solid rgba(255,255,255,.07);

        border-radius: 18px;

        padding: 18px;

        min-height: 145px;
    }

    .source-title {
        font-size: 17px;
        font-weight: 750;
    }

    .source-text {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.6;
        margin-top: 9px;
    }

    .online {
        color: #4ade80;
        font-size: 11px;
        font-weight: 700;
        margin-top: 10px;
    }

    .user-message {
        background:
            rgba(99,102,241,.12);

        border:
            1px solid rgba(129,140,248,.12);

        padding: 15px 18px;

        border-radius:
            18px 18px 4px 18px;

        margin: 15px 0;
    }

    .ai-message {
        background:
            rgba(255,255,255,.045);

        border:
            1px solid rgba(255,255,255,.07);

        padding: 18px;

        border-radius:
            18px 18px 18px 4px;

        margin: 15px 0;
    }

    .tool-box {
        background:
            rgba(129,140,248,.08);

        border:
            1px solid rgba(129,140,248,.12);

        border-radius: 14px;

        padding: 12px 15px;

        margin-top: 10px;

        color: #c4b5fd;

        font-size: 13px;
    }

    textarea {
        background:
            rgba(15,23,42,.70) !important;

        color:
            white !important;

        border:
            1px solid rgba(255,255,255,.10) !important;

        border-radius:
            16px !important;
    }

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            ) !important;

        color: white !important;

        border: none !important;

        border-radius:
            14px !important;

        font-weight:
            750 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;padding:12px;">

            <div style="
                font-size:44px;
            ">
                🎓
            </div>

            <div style="
                font-size:23px;
                font-weight:800;
            ">
                UniMind AI
            </div>

            <div style="
                color:#94a3b8;
                font-size:12px;
                margin-top:4px;
            ">
                University Knowledge Intelligence
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✦ Workspace")

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.markdown("### 📊 Knowledge Sources")

    st.success("🟢 MySQL Connected")
    st.success("🟢 ChromaDB Connected")
    st.success("🟢 Neo4j Connected")

    st.markdown("### 🤖 Local AI")

    st.info("Qwen3 4B · Ollama")

    st.markdown("---")

    st.caption(
        "Agentic AI-based University Knowledge System"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-icon">
            ✦
        </div>

        <div class="hero-title">
            UniMind AI
        </div>

        <div class="hero-subtitle">
            Your intelligent university knowledge assistant
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# METRICS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        """
        <div class="metric">
            <div class="metric-icon">👨‍🎓</div>
            <div class="metric-value">15</div>
            <div class="metric-label">Students</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        """
        <div class="metric">
            <div class="metric-icon">📚</div>
            <div class="metric-value">7</div>
            <div class="metric-label">Courses</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        """
        <div class="metric">
            <div class="metric-icon">📄</div>
            <div class="metric-value">5</div>
            <div class="metric-label">Policy Documents</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        """
        <div class="metric">
            <div class="metric-icon">🔗</div>
            <div class="metric-value">50</div>
            <div class="metric-label">Graph Relations</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# DATABASE SOURCES
# ============================================================

s1, s2, s3 = st.columns(3)

with s1:

    st.markdown(
        """
        <div class="source">

            <div class="source-title">
                🗄️ MySQL
            </div>

            <div class="source-text">
                Structured student, department,
                faculty and course information.
            </div>

            <div class="online">
                ● ONLINE
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with s2:

    st.markdown(
        """
        <div class="source">

            <div class="source-title">
                📖 ChromaDB
            </div>

            <div class="source-text">
                Semantic search over university
                policies and textual documents.
            </div>

            <div class="online">
                ● ONLINE
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with s3:

    st.markdown(
        """
        <div class="source">

            <div class="source-title">
                🕸️ Neo4j
            </div>

            <div class="source-text">
                Relationship analysis between
                students, courses and faculty.
            </div>

            <div class="online">
                ● ONLINE
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                <b>🧑 You</b><br><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="ai-message">

                <b>🤖 UniMind AI</b>

                <br><br>

                {message["content"]}

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# QUESTION INPUT
# ============================================================

st.markdown(
    '<div class="glass">',
    unsafe_allow_html=True
)

question = st.text_area(
    "Ask UniMind",
    placeholder=(
        "Ask about GPA, students, courses, "
        "attendance, university rules or faculty..."
    ),
    height=100
)

ask = st.button(
    "✦ Ask UniMind",
    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if ask:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "🧠 UniMind is searching the knowledge sources..."
        ):

            try:

                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": question
                            }
                        ]
                    }
                )

                answer = result[
                    "messages"
                ][-1].content

                # --------------------------------------------
                # Find tools used
                # --------------------------------------------

                tool_names = []

                for message in result["messages"]:

                    # AIMessage tool calls
                    calls = getattr(
                        message,
                        "tool_calls",
                        []
                    )

                    for call in calls:

                        name = call.get(
                            "name"
                        )

                        if name and name not in tool_names:

                            tool_names.append(name)

                    # ToolMessage
                    tool_name = getattr(
                        message,
                        "name",
                        None
                    )

                    if (
                        tool_name
                        and tool_name not in tool_names
                    ):

                        tool_names.append(
                            tool_name
                        )

                # --------------------------------------------
                # Save messages
                # --------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": question
                    }
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                # --------------------------------------------
                # Current response
                # --------------------------------------------

                if tool_names:

                    pretty_names = {
                        "get_student_gpa": "MySQL",
                        "count_students_by_department": "MySQL",
                        "get_students_by_gpa": "MySQL",
                        "get_all_students": "MySQL",

                        "semantic_policy_search": "ChromaDB",

                        "find_course_teacher": "Neo4j",
                        "find_ai_specialized_faculty": "Neo4j",
                        "find_students_in_ai_faculty_courses": "Neo4j",
                        "find_students_in_course": "Neo4j"
                    }

                    sources = []

                    for name in tool_names:

                        display = pretty_names.get(
                            name,
                            name
                        )

                        if display not in sources:

                            sources.append(
                                display
                            )

                    st.markdown(
                        f"""
                        <div class="tool-box">
                            🧠 Knowledge sources used:
                            <b>
                            {" + ".join(sources)}
                            </b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"""
                    <div class="ai-message">

                        <b>🤖 UniMind AI</b>

                        <br><br>

                        {answer}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(
                    f"Agent error: {e}"
                )