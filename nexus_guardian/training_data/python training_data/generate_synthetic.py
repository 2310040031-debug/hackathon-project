"""
Train all three NEXUS GUARDIAN AI agents on synthetic data.
Run: python training_data/train_all_agents.py
"""

import os
import pickle
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, mean_absolute_error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "training_data")
MDL_DIR  = os.path.join(BASE_DIR, "models")
os.makedirs(MDL_DIR, exist_ok=True)


def train_agent(name, df, features, target_class, target_score):
    print(f"\n{'='*50}")
    print(f"Training: {name}")
    print(f"{'='*50}")

    X  = df[features]
    yc = df[target_class]
    yr = df[target_score]

    Xtr, Xte, yc_tr, yc_te, yr_tr, yr_te = train_test_split(
        X, yc, yr, test_size=0.2, random_state=42
    )

    # Classifier
    clf = Pipeline([
        ("sc",  StandardScaler()),
        ("clf", GradientBoostingClassifier(
            n_estimators=300, max_depth=5,
            learning_rate=0.05, random_state=42
        ))
    ])
    clf.fit(Xtr, yc_tr)
    print(classification_report(yc_te, clf.predict(Xte)))

    # Regressor
    reg = Pipeline([
        ("sc",  StandardScaler()),
        ("reg", GradientBoostingRegressor(
            n_estimators=300, max_depth=5,
            learning_rate=0.05, random_state=42
        ))
    ])
    reg.fit(Xtr, yr_tr)
    mae = mean_absolute_error(yr_te, reg.predict(Xte))
    print(f"Score MAE: {mae:.2f}")

    # Save
    with open(f"{MDL_DIR}/{name}_classifier.pkl", "wb") as f: pickle.dump(clf, f)
    with open(f"{MDL_DIR}/{name}_regressor.pkl",  "wb") as f: pickle.dump(reg, f)
    with open(f"{MDL_DIR}/{name}_features.pkl",   "wb") as f: pickle.dump(features, f)
    print(f"Saved to models/{name}_*.pkl")


if __name__ == "__main__":
    # Machine Health Agent
    machine_df = pd.read_csv(f"{DATA_DIR}/synthetic_machine.csv")
    train_agent(
        "machine",
        machine_df,
        features=["temperature", "gas_ppm", "noise_db", "radiation", "age"],
        target_class="risk_class",
        target_score="risk_score"
    )

    # Worker Health Agent
    worker_df = pd.read_csv(f"{DATA_DIR}/synthetic_worker.csv")
    train_agent(
        "worker",
        worker_df,
        features=["heart_rate", "fatigue", "exposure", "machine_risk", "hours_worked"],
        target_class="health_class",
        target_score="health_score"
    )

    # Supervisor Agent
    supervisor_df = pd.read_csv(f"{DATA_DIR}/synthetic_supervisor.csv")
    train_agent(
        "supervisor",
        supervisor_df,
        features=["machine_risk", "worker_risk", "exposure"],
        target_class="verdict",
        target_score="combined"
    )

    print("\nAll agents trained successfully.")