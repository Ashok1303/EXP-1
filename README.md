# AITTOS: AI-Powered Track & Traffic Optimization System

A reference implementation of the Unified Algorithm: AI-Powered Track & Traffic Optimization (AITTOS) with a FastAPI backend, Streamlit dashboard, and an IRCTC API client to fetch train details by train number.

## Features

- IRCTC API client: fetch train details by number (configurable provider; supports mock if no key)
- Digital twin data model for sections, tracks, junctions, platforms
- ILP-based conflict-free scheduling optimizer (via PuLP)
- Predictive ETA utilities and speed advisory stubs
- Incident detection hook and rapid re-optimization pathway
- FastAPI endpoints for integration and a Streamlit dashboard for controllers

## Quickstart

### 1) Setup Python environment

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment

Copy `.env.example` to `.env` and fill values as needed. If no IRCTC provider/key is configured, the backend returns mocked train data for demo purposes.

```bash
cp .env.example .env
```

Environment variables:
- `IRCTC_API_BASE_URL`: Base URL of your IRCTC data provider (e.g., RapidAPI endpoint base)
- `IRCTC_API_KEY`: API key/token
- `IRCTC_API_HOST`: Optional host header (e.g., `X-RapidAPI-Host`)
- `IRCTC_TRAIN_INFO_PATH`: Optional path for train info endpoint (default `/train/info`)
- `BACKEND_HOST`: Default `0.0.0.0`
- `BACKEND_PORT`: Default `8000`
- `FRONTEND_BACKEND_URL`: Frontend default backend URL (e.g., `http://localhost:8000`)

### 3) Run backend

```bash
uvicorn aittos.main:app --host 0.0.0.0 --port 8000 --reload
```

API endpoints:
- `GET /health`
- `GET /train/{train_number}`
- `POST /optimize`
- `POST /what-if`

### 4) Run dashboard

```bash
streamlit run dashboard/app.py
```

Set the backend URL in the sidebar if different from default.

## Notes on IRCTC API integration

- This project provides a flexible client. Supply your provider base URL and headers in the environment.
- For RapidAPI-style providers, `IRCTC_API_HOST` and `IRCTC_API_KEY` are passed as `X-RapidAPI-Host` and `X-RapidAPI-Key` respectively.
- Endpoint paths vary by provider. By default, the client uses `/train/info` with query parameter `trainNumber`. Override via `IRCTC_TRAIN_INFO_PATH`.
- When credentials are missing, the client returns a realistic mocked response for demo/testing.

## ILP Optimizer

- A simplified ILP model demonstrates conflict-free ordering with minimum headway on a single-line section.
- Extend `aittos/services/optimizer_ilp.py` with richer constraints for multi-block, platforms, and precedence.

## License

This repository is provided for educational and demonstration purposes. Ensure you comply with IRCTC and provider terms for any production usage.