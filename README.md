
# 🎵 SonicMiner AI
### AI-Powered Audio Feature Extraction and Analysis Platform

SonicMiner AI is an interactive audio analysis platform that allows users to upload audio files, extract meaningful audio features, visualize acoustic characteristics, and export extracted data for further analysis and machine learning applications.

The primary goal of SonicMiner AI is to make audio feature extraction easier and more accessible by providing users with structured audio data that they can download and use to train their own machine learning models or perform further research.

## 🚀 Key Features

### 1. Audio Upload and Analysis
- Upload multiple audio files.
- Supports audio playback.
- Analyze individual audio files or multiple files together.

### 2. Audio Feature Extraction
Extracts **39 audio features** across five categories:

- **Core Features:** RMS Energy, Zero Crossing Rate, Spectral Centroid, Spectral Bandwidth, Spectral Rolloff and Spectral Flatness.
- **MFCC:** 13 Mel-Frequency Cepstral Coefficients.
- **Chroma:** 12 Chroma features.
- **Spectral Contrast:** 7 Spectral Contrast features.
- **Rhythm:** Tempo.

Additional metadata includes audio duration and sample rate.

### 3. CSV Data Export
Users can export extracted audio features in CSV format.

- Export features of all uploaded audio files.
- Export selected audio files.
- Export selected features from selected audio files.
- Export individual audio analysis results.

The exported datasets can be used for machine learning, data analysis, experimentation and research.

### 4. Audio Visualization
Provides visual representations to help users understand audio characteristics.

- Audio Waveform Visualization
- MFCC Heatmaps
- Chroma Heatmaps
- Spectral Contrast Heatmaps

### 5. Audio Similarity Search
Compare uploaded audio files to understand how similar their extracted feature representations are.

For example, users can compare one song against multiple uploaded songs or compare any two selected audio files.

### 6. Gemini-Powered AI Explanations
Provides optional AI-generated explanations of measured audio characteristics to help users interpret their audio analysis results.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Audio Processing | Librosa, SoundFile |
| Numerical Computing | NumPy |
| Data Processing | Pandas |
| Machine Learning | Scikit-learn |
| Visualization | Matplotlib |
| Generative AI | Google Gemini API |

## 📂 Project Structure

```text
SonicMiner-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── assets/
│   ├── styles.css
│   ├── logo.png
│   ├── hero_bg.png
│   ├── waveform.png
│   ├── mfcc.png
│   ├── chroma.png
│   └── spectral_contrast.png
│
└── modules/
    ├── audio_loader.py
    ├── csv_export.py
    ├── dashboard.py
    ├── feature_extractor.py
    ├── gemini_explainer.py
    ├── landing.py
    ├── similarity.py
    ├── utils.py
    └── visualization.py
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/SonicMiner-AI.git
```

### 2. Navigate to the Project Directory

```bash
cd SonicMiner-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API (Optional)

Create a `.env` file in the project root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Gemini-powered explanations are optional. The core audio analysis functionality does not require an API key.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🎯 Project Objective

The main objective of SonicMiner AI is to provide users with an easy-to-use platform for extracting, understanding and exporting audio features.

Instead of manually processing audio files using programming libraries, users can upload their audio files, obtain structured feature data, visualize audio characteristics and download datasets for their own machine learning experiments.

## 👩‍💻 Developed With

**SonicMiner AI** — Making Audio Feature Extraction and Analysis Accessible.
