import json
import time
from pathlib import Path

import streamlit as st

from document_processor import process_image


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MCQ Document Analyzer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: #f7f7fb;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #24134f 0%,
            #3b2380 100%
        );
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* ---------- Header ---------- */

    .hero {
        padding: 20px 0 10px 0;
    }

    .hero h1 {
        font-size: 38px;
        margin-bottom: 5px;
        font-weight: 750;
        color: #181526;
    }

    .hero p {
        color: #686477;
        font-size: 16px;
    }

    /* ---------- Cards ---------- */

    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #ebe8f3;
        box-shadow: 0 5px 20px rgba(40, 30, 80, 0.06);
    }

    .metric-title {
        color: #777285;
        font-size: 13px;
        margin-bottom: 7px;
    }

    .metric-value {
        color: #24134f;
        font-size: 28px;
        font-weight: 750;
    }

    .upload-card {
        background: white;
        border: 2px dashed #bca8ee;
        border-radius: 22px;
        padding: 40px;
        margin-top: 20px;
        text-align: center;
    }

    .status-card {
        background: white;
        border-radius: 18px;
        padding: 24px;
        border: 1px solid #ebe8f3;
        box-shadow: 0 5px 20px rgba(40, 30, 80, 0.06);
    }

    .question-card {
        background: white;
        border-radius: 16px;
        padding: 22px;
        margin: 12px 0;
        border: 1px solid #ebe8f3;
        box-shadow: 0 4px 16px rgba(40, 30, 80, 0.04);
    }

    .question-title {
        font-size: 18px;
        font-weight: 700;
        color: #23183e;
    }

    .option {
        background: #f8f6fd;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 7px 0;
        color: #3b3547;
    }

    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        background: #eee8ff;
        color: #5b35b4;
        font-size: 12px;
        font-weight: 650;
        margin-right: 6px;
    }

    .success-box {
        padding: 15px 18px;
        background: #edf9f2;
        border: 1px solid #b9e6c8;
        border-radius: 12px;
        color: #1e6b3b;
        font-weight: 600;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 10px;
        font-weight: 650;
        min-height: 42px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:25px;
            font-weight:800;
            padding:10px 0 5px 0;">
            ✦ MCQ
        </div>

        <div style="
            font-size:15px;
            opacity:0.85;
            margin-bottom:35px;">
            Document Analyzer
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Upload Document",
            "Questions",
            "JSON Output",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            background:rgba(255,255,255,0.12);
            border-radius:14px;
            padding:15px;">
            <div style="font-size:12px;opacity:.75;">
                AI EXTRACTION ENGINE
            </div>
            <div style="
                margin-top:7px;
                font-weight:700;">
                ● Ready
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "json_data" not in st.session_state:
    st.session_state.json_data = None

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>Document Intelligence</h1>
            <p>
                Turn question papers into structured,
                searchable knowledge.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.result

    if result:

        summary = result["extraction_summary"]

        questions = summary["questions_detected"]

        layout = result["document"]["layout"]

        st.markdown("### Latest Analysis")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        Questions Extracted
                    </div>
                    <div class="metric-value">
                        {questions}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        Layout
                    </div>
                    <div class="metric-value">
                        {layout.replace("-", " ").title()}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        Options Detected
                    </div>
                    <div class="metric-value">
                        {summary["total_options_detected"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c4:
            complete = summary["questions_with_4_options"]

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        Complete Questions
                    </div>
                    <div class="metric-value">
                        {complete}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("")
        st.success(
            f"Last processed document: "
            f"{result['document']['file_name']}"
        )

    else:

        st.info(
            "No document analyzed yet. "
            "Go to Upload Document to begin."
        )


# ============================================================
# UPLOAD PAGE
# ============================================================

elif page == "Upload Document":

    st.markdown(
        """
        <div class="hero">
            <h1>Upload your question paper</h1>
            <p>
                Extract, organize and analyze MCQs automatically.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="upload-card">
            <h2>Upload a document</h2>
            <p>
                Supported formats: PNG, JPG, JPEG
            </p>
            <p style="color:#777285;">
                Best results with clear printed question papers.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
    )

    if uploaded_file:

        st.markdown("### Selected Document")

        c1, c2 = st.columns([1, 1])

        with c1:

            st.image(
                uploaded_file,
                caption=uploaded_file.name,
                use_container_width=True,
            )

        with c2:

            st.markdown(
                f"""
                <div class="status-card">
                    <h3>{uploaded_file.name}</h3>

                    <p>
                        <span class="badge">
                        {uploaded_file.type}
                        </span>

                        <span class="badge">
                        {round(uploaded_file.size / 1024, 1)} KB
                        </span>
                    </p>

                    <p>
                    The document will be analyzed for:
                    </p>

                    <p>
                    ✓ OCR text extraction<br>
                    ✓ Column detection<br>
                    ✓ Reading order<br>
                    ✓ MCQ extraction<br>
                    ✓ JSON generation
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("")

            analyze = st.button(
                "✦ Analyze Document",
                use_container_width=True,
                type="primary",
            )

            if analyze:

                input_dir = Path("data/input")
                output_dir = Path("data/output")

                input_dir.mkdir(
                    parents=True,
                    exist_ok=True
                )

                output_dir.mkdir(
                    parents=True,
                    exist_ok=True
                )

                input_path = (
                    input_dir /
                    uploaded_file.name
                )

                output_path = (
                    output_dir /
                    f"{Path(uploaded_file.name).stem}.json"
                )

                input_path.write_bytes(
                    uploaded_file.getbuffer()
                )

                progress = st.progress(0)

                status = st.empty()

                try:

                    status.info(
                        "01 · Validating document..."
                    )
                    progress.progress(10)
                    time.sleep(0.3)

                    status.info(
                        "02 · Running OCR..."
                    )
                    progress.progress(30)

                    result = process_image(
                        input_path,
                        output_path
                    )

                    status.info(
                        "03 · Detecting layout and "
                        "reading order..."
                    )
                    progress.progress(65)
                    time.sleep(0.4)

                    status.info(
                        "04 · Extracting MCQs..."
                    )
                    progress.progress(82)
                    time.sleep(0.4)

                    status.info(
                        "05 · Generating JSON..."
                    )
                    progress.progress(95)
                    time.sleep(0.4)

                    progress.progress(100)

                    status.success(
                        "Analysis completed successfully."
                    )

                    st.session_state.result = result
                    st.session_state.processed_file = (
                        uploaded_file.name
                    )

                    with open(
                        output_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        st.session_state.json_data = (
                            f.read()
                        )

                    st.success(
                        "Your structured JSON file is ready."
                    )

                    st.rerun()

                except Exception as exc:

                    progress.empty()

                    st.error(
                        "Document processing failed."
                    )

                    st.exception(exc)


# ============================================================
# QUESTIONS PAGE
# ============================================================

elif page == "Questions":

    st.markdown(
        """
        <div class="hero">
            <h1>Extracted Questions</h1>
            <p>
                Review the questions identified from your document.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.result

    if not result:

        st.info(
            "Analyze a document first."
        )

    else:

        questions = result["questions"]

        st.markdown(
            f"""
            <div class="success-box">
                {len(questions)}
                question blocks detected.
            </div>
            """,
            unsafe_allow_html=True,
        )

        for question in questions:

            st.markdown(
                f"""
                <div class="question-card">

                    <div class="question-title">
                        Q{question["question_number"]}
                    </div>

                    <p>
                        {question["question"]}
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            for option in question["options"]:

                st.markdown(
                    f"""
                    <div class="option">
                        <strong>
                            {option["label"]}.
                        </strong>
                        {option["text"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            validation = question["validation"]

            if validation["complete"]:

                st.success(
                    "✓ 4/4 options detected"
                )

            else:

                st.warning(
                    f"⚠ "
                    f"{validation['options_detected']}/4 "
                    f"options detected"
                )


# ============================================================
# JSON PAGE
# ============================================================

elif page == "JSON Output":

    st.markdown(
        """
        <div class="hero">
            <h1>Structured JSON Output</h1>
            <p>
                Machine-readable output generated from your document.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.result
    json_data = st.session_state.json_data

    if not result or not json_data:

        st.info(
            "Analyze a document first to generate JSON."
        )

    else:

        summary = result["extraction_summary"]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Questions",
                summary["questions_detected"]
            )

        with c2:
            st.metric(
                "Options",
                summary["total_options_detected"]
            )

        with c3:
            st.metric(
                "Layout",
                result["document"]["layout"]
                .replace("-", " ")
                .title()
            )

        st.markdown("### JSON Preview")

        st.code(
            json_data,
            language="json",
            line_numbers=True,
        )

        st.markdown("")

        json_filename = (
            Path(
                result["document"]["file_name"]
            ).stem
            + ".json"
        )

        st.download_button(
            label="⬇ Download JSON File",
            data=json_data,
            file_name=json_filename,
            mime="application/json",
            use_container_width=True,
            type="primary",
        )

        st.success(
            f"Ready to download: {json_filename}"
        )