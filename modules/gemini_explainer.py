import os
from dotenv import load_dotenv

load_dotenv()
def generate_insight(analysis, comparison=None):
    """Generate an optional LLM explanation without making the core pipeline depend on it."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, "GEMINI_API_KEY is not configured."
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        f = analysis["features"]
        prompt = f"""You are SonicMiner AI's audio interpretation engine.
Interpret these measured audio characteristics accurately. Do not invent facts that are not supported by the measurements.

Duration: {f.get('Duration', 0):.2f} seconds
Tempo: {f.get('Tempo', 0):.1f} BPM
RMS Energy: {f.get('RMS Energy', 0):.5f}
Zero Crossing Rate: {f.get('Zero Crossing Rate', 0):.5f}
Spectral Centroid: {f.get('Spectral Centroid', 0):.1f} Hz
Spectral Bandwidth: {f.get('Spectral Bandwidth', 0):.1f} Hz
Spectral Rolloff: {f.get('Spectral Rolloff', 0):.1f} Hz
Spectral Flatness: {f.get('Spectral Flatness', 0):.5f}

Explain the measurable acoustic profile in concise sections: Energy, Rhythm, Timbre, and Harmonic/cepstral characteristics. Clearly distinguish measurements from interpretation."""
        response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
        return response.text, None
    except Exception as exc:
        return None, f"AI insight unavailable: {exc}"
