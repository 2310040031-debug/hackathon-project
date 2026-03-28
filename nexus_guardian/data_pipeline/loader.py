"""
CSV loader with strict schema validation.
Falls back to building a fresh dataset if the CSV is missing,
empty, or has wrong/missing columns. Never raises a KeyError.
"""
import os
import streamlit as st
import pandas as pd
from data_pipeline.dataset_builder import build_dataset
from constants import REQUIRED_COLS


def _csv_is_valid(path: str) -> bool:
    """Read only the header row — fast even on large files."""
    if not os.path.exists(path):
        return False
    try:
        header = pd.read_csv(path, nrows=0)
        header.columns = header.columns.str.strip()
        return REQUIRED_COLS.issubset(set(header.columns))
    except Exception:
        return False


@st.cache_data(show_spinner="Loading sensor dataset…")
def load_dataset(csv_path: str) -> pd.DataFrame:
    """
    Load and validate the sensor dataset.
    Order of priority:
      1. Valid cached CSV at csv_path  →  read and return
      2. Any failure                   →  build fresh, attempt to persist
    """
    if _csv_is_valid(csv_path):
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        return df

    df = build_dataset()
    try:
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
    except OSError:
        pass  # read-only filesystem — silently continue
    return df


def validate_or_stop(df: pd.DataFrame) -> None:
    """
    Call after load_dataset(). If required columns are missing,
    show a human-readable Streamlit error and halt the app cleanly.
    """
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        st.error(
            f"**Dataset schema error — missing columns:** `{missing}`\n\n"
            "**Fix:** Delete `data/sensor_data.csv` and restart the app. "
            "A clean dataset will be regenerated automatically."
        )
        st.stop()


def get_sensor_row(df: pd.DataFrame, tick: int, facility: str) -> dict:
    """Return a single sensor reading dict for the given facility and tick."""
    sub = df[df["facility"] == facility].reset_index(drop=True)
    row = sub.iloc[tick % len(sub)]
    return {col: float(row[col])
            for col in ["temperature", "gas_ppm", "noise_db",
                        "radiation", "heart_rate", "fatigue", "hour"]}
