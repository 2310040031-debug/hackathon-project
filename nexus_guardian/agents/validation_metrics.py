"""
Offline validation metrics for rule-based safety agents.

Compares each agent's categorical output to an independent *threshold oracle*
built from ``constants.THRESHOLDS`` (warn / danger / limit). The full historical
CSV is replayed per facility with cumulative exposure, matching live app behavior.

This is a consistency / alignment metric vs. regulatory-style labels — not
supervised ML accuracy on held-out labels.
"""

from __future__ import annotations

import os

import pandas as pd

from . import exposure_system, machine_agent, supervisor_agent, worker_agent
from constants import RISK_WEIGHTS, THRESHOLDS

_MACHINE_MAP = {"OPTIMAL": 0, "ADVISORY": 1, "WARNING": 2, "CRITICAL": 3}
_WORKER_MAP = {"FIT": 0, "CAUTION": 1, "AT RISK": 2, "CRITICAL": 3}

_TIER_PROXY = (18.0, 42.0, 62.0, 92.0)  # score stand-ins for oracle tiers 0–3


def _sev(val: float, key: str) -> int:
    th = THRESHOLDS[key]
    if val >= th["limit"]:
        return 3
    if val >= th["danger"]:
        return 2
    if val >= th["warn"]:
        return 1
    return 0


def machine_oracle_status(temp: float, gas: float, noise: float, rad: float) -> str:
    s = max(
        _sev(temp, "temperature"),
        _sev(gas, "gas_ppm"),
        _sev(noise, "noise_db"),
        _sev(rad, "radiation"),
    )
    if s >= 3:
        return "CRITICAL"
    if s == 2:
        return "WARNING"
    if s == 1:
        return "ADVISORY"
    return "OPTIMAL"


def worker_oracle_status(
    hr: float,
    fatigue: float,
    temp: float,
    gas: float,
    noise: float,
    rad: float,
    exp_score: float,
) -> str:
    sw = max(_sev(hr, "heart_rate"), _sev(fatigue, "fatigue"))
    se = max(
        _sev(temp, "temperature"),
        _sev(gas, "gas_ppm"),
        _sev(noise, "noise_db"),
        _sev(rad, "radiation"),
    )
    sx = 0 if exp_score < 35 else 1 if exp_score < 55 else 2 if exp_score < 78 else 3
    s = max(sw, se, sx)
    if s >= 3:
        return "CRITICAL"
    if s == 2:
        return "AT RISK"
    if s == 1:
        return "CAUTION"
    return "FIT"


def exp_tier_from_score(score: float) -> int:
    if score < 20:
        return 0
    if score < 40:
        return 1
    if score < 65:
        return 2
    return 3


def supervisor_oracle_status(mt: int, wt: int, et: int) -> str:
    w = RISK_WEIGHTS["supervisor"]
    ms, ws, es = _TIER_PROXY[mt], _TIER_PROXY[wt], _TIER_PROXY[et]
    combined = ms * w["machine"] + ws * w["worker"] + es * w["exposure"]
    max_single = max(ms, ws, es)
    if max_single >= 80:
        combined = max(combined, max_single * 0.92)
    combined = round(combined, 1)

    if combined < 28:
        return "ALL SYSTEMS NOMINAL"
    if combined < 48:
        return "ELEVATED ADVISORY"
    if combined < 68:
        return "ROTATION REQUIRED"
    return "EMERGENCY STOP"


def compute_dataset_validation(csv_path: str, _mtime: float | None = None) -> dict:
    """
    Replay every row grouped by facility; return accuracy percentages and counts.

    ``_mtime`` is only used to bust Streamlit's cache when the file changes.
    """
    if not os.path.isfile(csv_path):
        return _empty_metrics()

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    required = {
        "facility",
        "temperature",
        "gas_ppm",
        "noise_db",
        "radiation",
        "heart_rate",
        "fatigue",
    }
    if not required.issubset(df.columns):
        return _empty_metrics()

    machine_ok = worker_ok = sup_ok = 0
    n = 0
    m_abs_err = 0.0
    w_abs_err = 0.0

    for fac in df["facility"].unique():
        sub = df[df["facility"] == fac].reset_index(drop=True)
        exp = 0.0
        for i in range(len(sub)):
            row = sub.iloc[i]
            t = float(row["temperature"])
            g = float(row["gas_ppm"])
            n_db = float(row["noise_db"])
            r = float(row["radiation"])
            hr = float(row["heart_rate"])
            fat = float(row["fatigue"])

            mo = machine_oracle_status(t, g, n_db, r)
            m = machine_agent.run(t, g, n_db, r)
            if m["status"] == mo:
                machine_ok += 1
            m_abs_err += abs(m["score"] - _TIER_PROXY[_MACHINE_MAP[mo]])

            exp_res = exposure_system.run(r, g, t, exp)
            exp = float(exp_res["score"])

            wo = worker_oracle_status(hr, fat, t, g, n_db, r, exp)
            w = worker_agent.run(hr, fat, exp, m["score"])
            if w["status"] == wo:
                worker_ok += 1
            w_abs_err += abs(w["score"] - _TIER_PROXY[_WORKER_MAP[wo]])

            sup = supervisor_agent.run(m["score"], w["score"], exp)
            mt = _MACHINE_MAP[mo]
            wt = _WORKER_MAP[wo]
            et = exp_tier_from_score(exp)
            so = supervisor_oracle_status(mt, wt, et)
            if sup["status"] == so:
                sup_ok += 1

            n += 1

    if n == 0:
        return _empty_metrics()

    return {
        "n_samples": n,
        "machine_accuracy": 100.0 * machine_ok / n,
        "worker_accuracy": 100.0 * worker_ok / n,
        "supervisor_accuracy": 100.0 * sup_ok / n,
        "overall_accuracy": 100.0 * (machine_ok + worker_ok + sup_ok) / (3 * n),
        "machine_mae_vs_tier": m_abs_err / n,
        "worker_mae_vs_tier": w_abs_err / n,
    }


def _empty_metrics() -> dict:
    return {
        "n_samples": 0,
        "machine_accuracy": 0.0,
        "worker_accuracy": 0.0,
        "supervisor_accuracy": 0.0,
        "overall_accuracy": 0.0,
        "machine_mae_vs_tier": 0.0,
        "worker_mae_vs_tier": 0.0,
    }


def live_alignment(
    m_result: dict,
    w_result: dict,
    sup_result: dict,
    sensors: dict,
    exp_score: float,
) -> dict:
    """Compare current agent outputs to the threshold oracle (this tick)."""
    t = sensors["temperature"]
    g = sensors["gas_ppm"]
    n_db = sensors["noise_db"]
    r = sensors["radiation"]
    hr = sensors["heart_rate"]
    fat = sensors["fatigue"]
    mo = machine_oracle_status(t, g, n_db, r)
    wo = worker_oracle_status(hr, fat, t, g, n_db, r, exp_score)
    so = supervisor_oracle_status(
        _MACHINE_MAP[mo], _WORKER_MAP[wo], exp_tier_from_score(exp_score)
    )
    return {
        "machine_match": m_result["status"] == mo,
        "worker_match": w_result["status"] == wo,
        "supervisor_match": sup_result["status"] == so,
        "oracle_machine": mo,
        "oracle_worker": wo,
        "oracle_supervisor": so,
    }
