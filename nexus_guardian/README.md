# ⬡ NEXUS GUARDIAN
### Industrial AI Safety Intelligence Platform — Petrochemical & Pharmaceutical Edition

## Quick Start
```bash
cd nexus_guardian
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure
nexus_guardian/
├── app.py                  Entry point
├── constants.py            All shared constants, thresholds, rosters
├── agents/                 Modular AI agents (one concern per file)
├── data_pipeline/          Dataset generation + validated CSV loading
├── ui/                     CSS injection, HTML component builders, chart factories
├── data/                   Auto-generated sensor_data.csv lives here
└── .streamlit/config.toml  Theme + server config

## Fix: sensor_data.csv Schema Error
If you see a missing columns error, delete `data/sensor_data.csv` and restart.
The app will regenerate a clean, validated dataset automatically.

## Standards Referenced
- OSHA 29 CFR 1910 — General Industry
- ICRP Publication 103 — Radiation Protection
- NIOSH RELs — Occupational Exposure Limits
- WHO IEH — International Environmental Health
