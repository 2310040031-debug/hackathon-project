"""
Synthetic dataset generator for all NEXUS GUARDIAN AI agents.
Generates 50,000 realistic samples with domain-informed labels.
Run: python training_data/generate_synthetic.py
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)
N = 50_000  # number of samples to generate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR  = os.path.join(BASE_DIR, "training_data")
os.makedirs(OUT_DIR, exist_ok=True)


# ── MACHINE HEALTH DATASET ─────────────────────────────────────────────────
def generate_machine_data(n):
    # Random sensor readings within realistic ranges
    temp      = np.random.uniform(18,  92,  n)
    gas       = np.random.uniform(0,   280, n)
    noise     = np.random.uniform(58,  108, n)
    radiation = np.random.uniform(0,   2.5, n)

    # Inject realistic correlations
    # Old machines run hotter and noisier
    age       = np.random.randint(0, 20, n)
    temp     += age * 0.5 + np.random.normal(0, 2, n)
    noise    += age * 0.3 + np.random.normal(0, 1, n)
    temp      = np.clip(temp,  18, 92)
    noise     = np.clip(noise, 58, 108)

    # Domain-informed risk score
    t_sc = (temp      - 18) / 74  * 100
    g_sc =  gas              / 250 * 100
    n_sc = (noise     - 58) / 50  * 100
    r_sc =  radiation        / 2.0 * 100

    score = t_sc*0.30 + g_sc*0.32 + n_sc*0.18 + r_sc*0.20

    # Compound hazard penalties (domain knowledge baked in)
    score += np.where((temp > 75) & (noise > 88), 14, 0)
    score += np.where((gas > 100) & (temp > 65),  16, 0)
    score += np.where(radiation > 0.4,             12, 0)
    score += np.where((gas > 60) & (noise > 85) & (temp > 70), 10, 0)

    # Add noise to make it realistic
    score += np.random.normal(0, 3, n)
    score  = np.clip(score, 0, 100)

    # Risk class: 0=safe, 1=warning, 2=critical
    risk_class = np.select(
        [score < 33, (score >= 33) & (score < 65), score >= 65],
        [0, 1, 2]
    )

    return pd.DataFrame({
        "temperature": np.round(temp,      1),
        "gas_ppm":     np.round(gas,       1),
        "noise_db":    np.round(noise,     1),
        "radiation":   np.round(radiation, 4),
        "age":         age,
        "risk_score":  np.round(score,     1),
        "risk_class":  risk_class,
    })


# ── WORKER HEALTH DATASET ──────────────────────────────────────────────────
def generate_worker_data(n):
    heart_rate   = np.random.uniform(62,  132, n)
    fatigue      = np.random.uniform(5,   95,  n)
    exposure     = np.random.uniform(0,   100, n)
    machine_risk = np.random.uniform(0,   100, n)
    hours_worked = np.random.uniform(0,   12,  n)

    # Fatigue increases with hours and exposure
    fatigue += hours_worked * 3.5 + exposure * 0.2
    fatigue  = np.clip(fatigue, 5, 95)

    # Heart rate rises with machine risk proximity
    heart_rate += machine_risk * 0.1 + np.random.normal(0, 3, n)
    heart_rate  = np.clip(heart_rate, 62, 132)

    # Domain-informed worker risk score
    eff_fatigue = np.clip(fatigue + exposure*0.28 + machine_risk*0.12, 0, 100)
    hr_sc       = np.clip((heart_rate - 60) / 72 * 100, 0, 100)
    rad_penalty = np.clip(exposure * 0.2, 0, 20)

    score = hr_sc*0.28 + eff_fatigue*0.38 + exposure*0.26 + rad_penalty*0.08

    # Compound health risk penalties
    score += np.where((heart_rate > 105) & (exposure > 50), 14, 0)
    score += np.where(exposure > 65,                         10, 0)
    score += np.where((fatigue > 70) & (heart_rate > 95),    8,  0)

    score += np.random.normal(0, 2, n)
    score  = np.clip(score, 0, 100)

    health_class = np.select(
        [score < 33, (score >= 33) & (score < 55),
         (score >= 55) & (score < 72), score >= 72],
        [0, 1, 2, 3]  # fit, caution, at-risk, critical
    )

    return pd.DataFrame({
        "heart_rate":   np.round(heart_rate,   1),
        "fatigue":      np.round(fatigue,       1),
        "exposure":     np.round(exposure,      1),
        "machine_risk": np.round(machine_risk,  1),
        "hours_worked": np.round(hours_worked,  1),
        "health_score": np.round(score,         1),
        "health_class": health_class,
    })


# ── SUPERVISOR DATASET ─────────────────────────────────────────────────────
def generate_supervisor_data(n):
    machine_risk = np.random.uniform(0, 100, n)
    worker_risk  = np.random.uniform(0, 100, n)
    exposure     = np.random.uniform(0, 100, n)

    combined = machine_risk*0.33 + worker_risk*0.42 + exposure*0.25

    # Single critical reading override
    max_single = np.maximum(np.maximum(machine_risk, worker_risk), exposure)
    combined   = np.where(max_single >= 80,
                          np.maximum(combined, max_single * 0.92),
                          combined)
    combined  += np.random.normal(0, 2, n)
    combined   = np.clip(combined, 0, 100)

    verdict = np.select(
        [combined < 28,
         (combined >= 28) & (combined < 48),
         (combined >= 48) & (combined < 68),
         combined >= 68],
        [0, 1, 2, 3]  # nominal, advisory, rotation, emergency
    )

    return pd.DataFrame({
        "machine_risk": np.round(machine_risk, 1),
        "worker_risk":  np.round(worker_risk,  1),
        "exposure":     np.round(exposure,     1),
        "combined":     np.round(combined,     1),
        "verdict":      verdict,
    })


# ── GENERATE AND SAVE ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Machine Health dataset...")
    machine_df = generate_machine_data(N)
    machine_df.to_csv(f"{OUT_DIR}/synthetic_machine.csv", index=False)
    print(f"  Saved {len(machine_df)} rows")
    print(f"  Risk distribution:\n{machine_df['risk_class'].value_counts().sort_index()}\n")

    print("Generating Worker Health dataset...")
    worker_df = generate_worker_data(N)
    worker_df.to_csv(f"{OUT_DIR}/synthetic_worker.csv", index=False)
    print(f"  Saved {len(worker_df)} rows")
    print(f"  Health distribution:\n{worker_df['health_class'].value_counts().sort_index()}\n")

    print("Generating Supervisor dataset...")
    supervisor_df = generate_supervisor_data(N)
    supervisor_df.to_csv(f"{OUT_DIR}/synthetic_supervisor.csv", index=False)
    print(f"  Saved {len(supervisor_df)} rows")
    print(f"  Verdict distribution:\n{supervisor_df['verdict'].value_counts().sort_index()}\n")

    print("All datasets generated successfully.")