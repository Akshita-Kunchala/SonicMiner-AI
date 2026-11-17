import streamlit as st

# ------------------------------------------------------------------
# Fix: st.markdown() runs content through a Markdown parser even when
# unsafe_allow_html=True. Any line indented 4+ spaces is interpreted
# as a Markdown code block, which is why the heavily-indented HTML
# blocks (similarity card, credits card, footer, etc.) were being
# rendered as literal text instead of styled HTML. This wrapper
# strips leading/trailing whitespace from every line before it
# reaches the parser, so indentation used for readability in the
# source no longer breaks rendering.
# ------------------------------------------------------------------
_original_markdown = st.markdown


def _safe_markdown(body, *args, **kwargs):
    if kwargs.get("unsafe_allow_html") and isinstance(body, str):
        body = "\n".join(line.strip() for line in body.split("\n"))
    return _original_markdown(body, *args, **kwargs)


st.markdown = _safe_markdown


def landing_page():
    

    # ================= NAVBAR =================

    left, right = st.columns([3, 2])

    with left:
        st.markdown(
            """
            <div class="nav-logo">
                SONICMINER AI
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="nav-links">
                <a href="#vision">Vision</a>
                <a href="#features">Features</a>
                <a href="#workflow">Workflow</a>
                <a href="#credits">Credits</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="glow-divider"></div>',
        unsafe_allow_html=True,
    )

    # ================= HERO =================

    
    st.markdown(
    """
    <div class="hero-title">
        SONICMINER AI
    </div>

    <div class="hero-wave">
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
        <span class="wave-bar"></span>
    </div>

    """,
    unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-tagline">
            Mine Intelligence From Sound
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="feature-pill">
            🎵 Audio Analysis
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            """
            <div class="feature-pill">
            🔍 Similarity Search
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            """
            <div class="feature-pill">
            ✨ AI Insights
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown(
        """
        <div class="hero-desc">
        Transform raw audio into meaningful intelligence through
        advanced machine-learning ready feature extraction, interactive visualization,
        similarity search and AI-powered understanding.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    a, b, c = st.columns([2, 3, 2])

    with b:

        if st.button(
            "🚀 Get Started",
            use_container_width=True,
        ):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown(
        """
        <div class="hero-support">
            Supports WAV • MP3 • M4A • Multi-file Upload • Music • Speech • General Audio
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    # ---------------- VISION ---------------- #

    st.markdown(
        """
        <div class="glow-divider"></div>

        <h5 style="
            text-align:center;
            color:#00F5FF;
            letter-spacing:6px;
            font-size:18px;
            margin-bottom:10px;
        ">
        THE SONICMINER VISION
        </h5>

        <h1 style="
            text-align:center;
            font-size:56px;
            margin-bottom:25px;
        ">
        Mine Intelligence From Sound
        </h1>

        <p style="
            text-align:center;
            max-width:900px;
            margin:auto;
            color:#94A3B8;
            font-size:22px;
            line-height:1.9;
        ">
        Transform raw audio into meaningful intelligence through
        advanced feature extraction, visualization,
        similarity search and AI-powered understanding.
        </p>

        <br><br><br>
        """,
        unsafe_allow_html=True
    )

    
    # ---------------- CORE CAPABILITIES ---------------- #


    st.markdown(
        '<div id="features" class="section-anchor"></div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="glow-divider"></div>
    <h1 class="section-title">               
    Core Capabilities
    <div class="section-subtitle">
    Modern audio mining for machine learning, research and intelligent analysis.

    </div>                 
    </h1>
    """, unsafe_allow_html=True)


    row1 = st.columns(3)

    with row1[0]:
        st.markdown("""
        <div class="glass-card">
        <h2>🎼 Audio Analysis</h2>
        <p>
        Extract MFCC, Chroma, Spectral Contrast, Tempo,
        RMS, Zero Crossing Rate and 30+ acoustic features from music, speech and general audio.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with row1[1]:
        st.markdown("""
        <div class="glass-card">
        <h2>📊 Interactive Visualization</h2>
        <p>
        Generate Waveforms, Spectrograms, MFCC Heatmaps
        and Chroma Maps with export support.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with row1[2]:
        st.markdown("""
        <div class="glass-card">
        <h2>📁 Multi-file Upload</h2>
        <p>
        Upload up to <b>10 audio files</b> simultaneously
        and analyze them together.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    row2 = st.columns(3)

    with row2[0]:
        st.markdown("""
        <div class="glass-card">
        <h2>🔍 Similarity Search</h2>
        <p>
        Compare uploaded audio using feature vectors
        and discover the closest matches instantly.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with row2[1]:
        st.markdown("""
        <div class="glass-card">
        <h2>📦 ML-ready CSV Export</h2>
        <p>
        Download features as
        <b>Single</b>,
        <b>Selected</b>,
        or
        <b>Complete Dataset CSV</b>
        for ML projects.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with row2[2]:
        st.markdown("""
        <div class="glass-card">
        <h2>✨ AI Insights</h2>
        <p>
        Understand similarity results using
        Gemini-powered explanations written
        in natural language.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    # =========================================================
    # SIMILARITY DEMO
    # =========================================================

    st.markdown(
        """
        <div class="glow-divider"></div>

        <h1 class="section-title">

        Similarity Search Preview
    <div class="section-subtitle">
    Compare audio files instantly using extracted
        acoustic representations and acoustic features.
    </div>
        </h1>

        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="similarity-card">

            <div class="similarity-row">

                <span class="song-name">

                music_04.wav

                </span>

                <span class="percent">

                94%

                </span>

            </div>

            <div class="progress">

                <div class="progress-fill p94"></div>

            </div>

            <br>

            <div class="similarity-row">

                <span class="song-name">

                song_01.wav

                </span>

                <span class="percent">

                87%

                </span>

            </div>

            <div class="progress">

                <div class="progress-fill p87"></div>

            </div>

            <br>

            <div class="similarity-row">

                <span class="song-name">

                sample.wav

                </span>

                <span class="percent">

                74%

                </span>

            </div>

            <div class="progress">

                <div class="progress-fill p74"></div>

            </div>

        </div>

        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    # =========================================================
    # WORKFLOW
    # =========================================================

    st.markdown(
        '<div id="workflow" class="section-anchor"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="glow-divider"></div>

        <h1 class="section-title">

        How SonicMiner Works
    <div class="section-subtitle">
    A simple pipeline that transforms raw audio into
        meaningful insights.

    </div>
        </h1>

        <br><br>

        """,
        unsafe_allow_html=True
    )
    step1, step2, step3, step4, step5 = st.columns(5)

    with step1:

        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">
            📂
            </div>
            <h3>
            Upload
            </h3>
            <p>
            Upload one or multiple
            audio files.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with step2:

        st.markdown("""
        <div class="workflow-card">

            <div class="workflow-icon">

            🎼

            </div>

            <h3>
            Extract

            </h3>
            <p>
            Generate audio
            features using
            Librosa.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with step3:

        st.markdown("""
        <div class="workflow-card">

            <div class="workflow-icon">
                📦
            </div>

            <h3>
                Download
            </h3>

            <p>
                Export feature CSVs
                or visualization
                images instantly.
            </p>

        </div>
        """, unsafe_allow_html=True)

    with step4:

        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">
            🔍
            </div>
            <h3>
            Compare
            </h3>
            <p>
            Find the most
            similar audio
            automatically.
            </p>
            </div>
        """, unsafe_allow_html=True)

    with step5:

        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">
            ✨
            </div>
            <h3>
            Understand
            </h3>
            <p>
            Generate AI
            explanations using
            Gemini.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    # =========================================================
    # CREDITS
    # =========================================================

    st.markdown(
        '<div id="credits" class="section-anchor"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="glow-divider"></div>

        <h1 class="section-title">

        Meet the Creator

        </h1>

        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="credits-card">

            <div class="credits-avatar">

            👩‍💻

            </div>

            <div class="credits-name">

            Akshita Kunchala

            </div>

            <div class="credits-role">

            AIML Undergraduate

            </div>

            <div class="credits-desc">    
            Passionate about building AI experiences that are not only intelligent, but also intuitive, interactive, and impactful. 
            I believe great technology should feel simple, meaningful, and accessible.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)

    with g1:

        st.link_button(
            "💻 GitHub",
            "https://github.com/",
            use_container_width=True
        )

    with g2:

        st.link_button(
            "🔗 LinkedIn",
            "https://linkedin.com/",
            use_container_width=True
        )

    with g3:

        st.link_button(
            "🌐 Portfolio",
            "#",
            use_container_width=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =========================================================
    # FOOTER
    # =========================================================

    st.markdown(
        """
        <div class="footer">

            <div class="footer-title">

            SONICMINER AI

            </div>

            <div class="footer-text">

            Mine Intelligence From Sound

            </div>

            <div class="footer-copy">

            © 2026 SonicMiner AI • All Rights Reserved

            </div>

            

        </div>
        """,
        unsafe_allow_html=True
    )