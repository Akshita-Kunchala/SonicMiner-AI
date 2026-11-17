import io
import pandas as pd


def analyses_to_dataframe(analyses, selected_features=None):
    rows = []
    for a in analyses:
        row = {"File Name": a["features"].get("File Name", a.get("file_path", "").split("/")[-1])}
        for k, v in a["features"].items():
            if k in {"Duration", "Sample Rate"} or selected_features is None or k in selected_features:
                row[k] = v
        rows.append(row)
    return pd.DataFrame(rows)


def dataframe_bytes(df):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")
