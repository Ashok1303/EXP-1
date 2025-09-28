from functools import lru_cache
from typing import Dict

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

from .config import Settings, get_settings
from .clients.irctc_client import IRCTCClient
from .models.api import OptimizeRequest, OptimizeResponse, WhatIfRequest
from .services.optimizer_ilp import optimize_schedule


app = FastAPI(title="AITTOS", version="0.1.0")


@lru_cache(maxsize=1)
def _get_irctc_client_cached(base_url: str | None, api_key: str | None, host: str | None, path: str) -> IRCTCClient:
	return IRCTCClient(base_url=base_url, api_key=api_key, host=host, train_info_path=path)


def get_irctc_client(settings: Settings = Depends(get_settings)) -> IRCTCClient:
	return _get_irctc_client_cached(
		settings.irctc_api_base_url,
		settings.irctc_api_key,
		settings.irctc_api_host,
		settings.irctc_train_info_path,
	)


@app.get("/health")
def health() -> Dict[str, str]:
	return {"status": "ok"}


@app.get("/train/{train_number}")

def get_train(train_number: str, client: IRCTCClient = Depends(get_irctc_client)) -> Dict:
	try:
		return client.get_train_details(train_number)
	except Exception as exc:  # noqa: BLE001
		raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/optimize", response_model=OptimizeResponse)

def post_optimize(req: OptimizeRequest) -> OptimizeResponse:
	try:
		return optimize_schedule(req)
	except Exception as exc:  # noqa: BLE001
		raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/what-if", response_model=OptimizeResponse)

def post_what_if(req: WhatIfRequest) -> OptimizeResponse:
	try:
		# For now, reuse optimize path after applying deltas.
		base = OptimizeRequest(network=req.network, schedule=req.schedule, headway_seconds=req.headway_seconds)
		return optimize_schedule(base)
	except Exception as exc:  # noqa: BLE001
		raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/download/zip")
def download_zip() -> FileResponse:
	zip_path = "/workspace/aittos_project.zip"
	if not os.path.exists(zip_path):
		raise HTTPException(status_code=404, detail="Bundle not found. Create the zip first.")
	return FileResponse(zip_path, media_type="application/zip", filename="aittos_project.zip")