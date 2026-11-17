import matplotlib.pyplot as plt
import librosa.display


def waveform_figure(analysis):
    y = analysis["series"]["waveform"]
    sr = analysis["sample_rate"]
    fig, ax = plt.subplots(figsize=(12, 3.5))
    librosa.display.waveshow(y, sr=sr, ax=ax)
    ax.set_title("Waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    fig.tight_layout()
    return fig


def heatmap_figure(matrix, title, x_label="Time", y_label="Feature"):
    fig, ax = plt.subplots(figsize=(12, 4.8))
    img = ax.imshow(matrix, aspect="auto", origin="lower", interpolation="nearest")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.colorbar(img, ax=ax, fraction=0.025, pad=0.02)
    fig.tight_layout()
    return fig


def mfcc_figure(analysis):
    return heatmap_figure(analysis["series"]["mfcc"], "MFCC Heatmap", y_label="MFCC Coefficient")


def chroma_figure(analysis):
    return heatmap_figure(analysis["series"]["chroma"], "Chroma Heatmap", y_label="Pitch Class")


def contrast_figure(analysis):
    return heatmap_figure(analysis["series"]["contrast"], "Spectral Contrast Heatmap", y_label="Frequency Band")
