import os
from pathlib import Path
import streamlit as st
import pandas as pd

from modules.audio_loader import save_uploaded_files, get_audio_metadata
from modules.feature_extractor import extract_audio_analysis, DEFAULT_FEATURES
from modules.visualization import waveform_figure, mfcc_figure, chroma_figure, contrast_figure
from modules.csv_export import analyses_to_dataframe, dataframe_bytes
from modules.similarity import hybrid_similarity
from modules.gemini_explainer import generate_insight


def _header():
    st.markdown('<div class="workspace-top"><div><div class="workspace-brand">SONICMINER <span>AI</span></div><div class="workspace-kicker">AUDIO INTELLIGENCE WORKSPACE</div></div><div class="status-orb"><span></span> ENGINE ONLINE</div></div>', unsafe_allow_html=True)


def _card(title, subtitle, icon):
    st.markdown(f'<div class="workspace-card-head"><div class="workspace-icon">{icon}</div><div><div class="workspace-card-title">{title}</div><div class="workspace-card-subtitle">{subtitle}</div></div></div>', unsafe_allow_html=True)


def _store_uploads(files):
    if not files:
        return []
    saved = save_uploaded_files(files)
    analyses = []
    progress = st.progress(0, text="Preparing audio intelligence...")
    for i, path in enumerate(saved, 1):
        try:
            a = extract_audio_analysis(path)
            a["features"]["File Name"] = Path(path).name
            a["metadata"] = get_audio_metadata(path)
            analyses.append(a)
        except Exception as exc:
            st.error(f"Could not analyze {Path(path).name}: {exc}")
        progress.progress(i / max(len(saved), 1), text=f"Analyzing {Path(path).name}")
    progress.empty()
    return analyses


def _feature_lab(analyses):
    _card("Feature Lab", "Select audio files and features, then export exactly the dataset you need.", "◈")
    if not analyses:
        st.info("Upload one or more audio files to begin extracting features.")
        return

    names = [a["features"]["File Name"] for a in analyses]

    song_col, feature_col = st.columns([1, 1])
    with song_col:
        selected_songs = st.multiselect(
            "Audio files to include",
            names,
            default=names,
            key="feature_songs",
        )
    with feature_col:
        selected = st.multiselect(
            "Features to include",
            DEFAULT_FEATURES,
            default=DEFAULT_FEATURES,
            key="feature_select",
        )

    selected_analyses = [
        a for a in analyses
        if a["features"]["File Name"] in selected_songs
    ]

    if not selected_songs:
        st.warning("Select at least one audio file.")
        return
    if not selected:
        st.warning("Select at least one feature.")
        return

    df = analyses_to_dataframe(selected_analyses, selected)
    st.dataframe(df, use_container_width=True, hide_index=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Selected audio", len(selected_analyses))
    with c2:
        st.metric("Selected features", len(selected))
    with c3:
        st.metric("Rows ready", len(df))

    filename = "sonicminer_selected_features.csv"
    st.download_button(
        "⇩ DOWNLOAD SELECTED FEATURES",
        dataframe_bytes(df),
        filename,
        "text/csv",
        use_container_width=True,
        key="download_selected_features",
    )
    st.caption("The CSV contains only the selected audio files and selected feature columns.")


def _visuals(analyses):
    _card("Audio Visuals", "See the signal, timbre and harmonic structure.", "◉")
    if not analyses:
        st.info("Upload audio from the workspace to visualize it.")
        return
    names = [a["features"]["File Name"] for a in analyses]
    idx = st.selectbox("Audio file", range(len(names)), format_func=lambda i: names[i], key="visual_audio")
    a = analyses[idx]
    tabs = st.tabs(["WAVEFORM", "MFCC", "CHROMA", "SPECTRAL CONTRAST"])
    figs = [waveform_figure(a), mfcc_figure(a), chroma_figure(a), contrast_figure(a)]
    for tab, fig in zip(tabs, figs):
        with tab:
            st.pyplot(fig, use_container_width=True)


def _compare(analyses):
    _card("Audio Compare", "Select the audio you want in the comparison set and see pairwise similarity results.", "◎")
    if len(analyses) < 2:
        st.info("Upload at least two audio files to compare them.")
        return

    names = [a["features"]["File Name"] for a in analyses]
    selected_names = st.multiselect(
        "Audio files to compare",
        names,
        default=names,
        key="compare_songs",
    )

    selected_analyses = [
        a for a in analyses
        if a["features"]["File Name"] in selected_names
    ]

    if len(selected_analyses) < 2:
        st.warning("Select at least two audio files.")
        return

    selected_names_ordered = [a["features"]["File Name"] for a in selected_analyses]
    results, pca = hybrid_similarity(selected_analyses)

    if not results:
        st.info("No pairwise similarity results are available for the selected audio.")
        return

    st.markdown(
        f'<div class="dataset-strip"><span>{len(selected_analyses)} SELECTED AUDIO FILES</span>'
        f'<span>•</span><span>{len(results)} PAIRWISE COMPARISONS</span>'
        f'<span>•</span><span>HYBRID SIMILARITY READY</span></div>',
        unsafe_allow_html=True,
    )

    results.sort(key=lambda x: x["overall"], reverse=True)

    for r in results:
        left = selected_names_ordered[r["a"]]
        right = selected_names_ordered[r["b"]]
        st.markdown(
            f'<div class="similarity-result">'
            f'<div><div class="result-name">{left} <span class="pair-arrow">↔</span> {right}</div>'
            f'<div class="result-meta">Acoustic {r["acoustic"]:.1f}% · Learned representation {r["learned"]:.1f}%</div></div>'
            f'<div class="result-score">{r["overall"]:.1f}%</div></div>'
            f'<div class="score-track"><div style="width:{r["overall"]:.1f}%"></div></div>',
            unsafe_allow_html=True,
        )

    st.caption("Results show every pair among the selected audio files. The hybrid score combines the transparent acoustic baseline with the data-driven representation layer.")


def _ai(analyses):
    _card("AI Analysis", "Convert measured audio characteristics into an interpretable AI report.", "✦")
    if not analyses:
        st.info("Upload audio to generate AI analysis.")
        return
    names = [a["features"]["File Name"] for a in analyses]
    idx = st.selectbox("Audio file", range(len(names)), format_func=lambda i: names[i], key="ai_audio")
    a = analyses[idx]
    f = a["features"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TEMPO", f"{f.get('Tempo', 0):.1f} BPM")
    c2.metric("RMS", f"{f.get('RMS Energy', 0):.4f}")
    c3.metric("CENTROID", f"{f.get('Spectral Centroid', 0):.0f} Hz")
    c4.metric("ZCR", f"{f.get('Zero Crossing Rate', 0):.4f}")
    if st.button("✦ GENERATE AI INSIGHT", use_container_width=True, key="generate_ai"):
        with st.spinner("Sonic intelligence is interpreting the measured profile..."):
            text, error = generate_insight(a)
        if text:
            st.markdown(f'<div class="ai-report">{text.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        else:
            st.warning(error)


def dashboard():
    _header()
    if st.button("← Return to Landing", key="back_landing"):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown('<div class="workspace-hero"><div class="workspace-eyebrow">AUDIO → FEATURES → INTELLIGENCE</div><h1>Your Audio Intelligence Workspace</h1><p>Choose the task you came for. SonicMiner processes only what that workflow needs.</p></div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("DROP AUDIO HERE", type=["mp3", "wav", "flac", "ogg", "m4a"], accept_multiple_files=True, key="workspace_upload")
    if uploaded:
        names = tuple(f.name for f in uploaded)
        if names != st.session_state.get("uploaded_names"):
            st.session_state.uploaded_names = names
            st.session_state.analyses = _store_uploads(uploaded)

    analyses = st.session_state.get("analyses", [])
    if analyses:
        st.markdown(f'<div class="dataset-strip"><span>{len(analyses)} AUDIO FILES READY</span><span>•</span><span>ANALYSIS ENGINE READY</span><span>•</span><span>ML WORKFLOW READY</span></div>', unsafe_allow_html=True)

    mode = st.radio("WORKSPACE", ["Feature Lab", "Audio Compare", "Audio Visuals", "AI Analysis"], horizontal=True, key="workspace_mode")
    if mode == "Feature Lab":
        _feature_lab(analyses)
    elif mode == "Audio Compare":
        _compare(analyses)
    elif mode == "Audio Visuals":
        _visuals(analyses)
    else:
        _ai(analyses)
