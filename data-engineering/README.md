# SAFE-ZONE Data Engineering

This branch prepares clean JSON/CSV datasets for the SAFE-ZONE project. Outputs are MongoDB- and AI-ready and follow the global models for **User**, **Alert**, and **Safe Spot**.

## Folder structure

- `raw-data/` – place raw CSV/JSON from any source here
- `clean-data/` – final cleaned outputs (alerts/safe-spots/users)
- `scripts/` – preprocessing and merging scripts
- `utils/` – shared helpers (logger, geospatial utilities)

## Main outputs (all under `clean-data/`)

- `alerts.json`, `alerts.csv`
- `safe-spots.json`, `safe-spots.csv`
- `users.json`, `users.csv`

All follow these models:

- Alert: `{ id, type, severity, timestamp, location: { lat, lng }, description }`
- Safe Spot: `{ id, name, type, address, location: { lat, lng } }`
- User: `{ id, name, phone, email }`

## Running the demo pipeline

From the repository root you can run:

```bash
python data-engineering/scripts/dataset_merger.py
```

If raw files are not present, the script will use small in-memory demo data to generate example `alerts.*`, `safe-spots.*`, and `users.*` in `clean-data/`.
