from __future__ import annotations

from typing import Any, Dict, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Settings


class IRCTCClient:
	def __init__(self, base_url: Optional[str], api_key: Optional[str], host: Optional[str], train_info_path: str) -> None:
		self.base_url = base_url.rstrip("/") if base_url else None
		self.api_key = api_key
		self.host = host
		self.train_info_path = train_info_path

	@classmethod
	def from_settings(cls, settings: Settings) -> "IRCTCClient":
		return cls(
			base_url=settings.irctc_api_base_url,
			api_key=settings.irctc_api_key,
			host=settings.irctc_api_host,
			train_info_path=settings.irctc_train_info_path,
		)

	def _headers(self) -> Dict[str, str]:
		headers: Dict[str, str] = {}
		if self.api_key:
			headers["X-RapidAPI-Key"] = self.api_key
		if self.host:
			headers["X-RapidAPI-Host"] = self.host
		return headers

	@retry(wait=wait_exponential(multiplier=0.5, min=0.5, max=4.0), stop=stop_after_attempt(3))
	def get_train_details(self, train_number: str) -> Dict[str, Any]:
		if not self.base_url or not self.api_key:
			return self._mock_train_details(train_number)
			
		url = f"{self.base_url}{self.train_info_path}"
		params = {"trainNumber": train_number}
		response = requests.get(url, headers=self._headers(), params=params, timeout=15)
		response.raise_for_status()
		data = response.json()
		return self._normalize_train_response(data)

	def _normalize_train_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
		# Providers differ; keep it simple and pass through with a minimal normalized view.
		return {
			"providerRaw": data,
			"normalized": {
				"trainNumber": data.get("trainNumber") or data.get("train_no") or data.get("number"),
				"trainName": data.get("trainName") or data.get("name"),
				"source": data.get("source") or data.get("from"),
				"destination": data.get("destination") or data.get("to"),
				"stops": data.get("stops") or data.get("route"),
			},
		}

	def _mock_train_details(self, train_number: str) -> Dict[str, Any]:
		return {
			"providerRaw": {"mock": True},
			"normalized": {
				"trainNumber": train_number,
				"trainName": "Demo Express",
				"source": "NDLS",
				"destination": "BCT",
				"stops": [
					{"code": "NDLS", "arr": None, "dep": "10:00"},
					{"code": "MTJ", "arr": "11:20", "dep": "11:25"},
					{"code": "KOTA", "arr": "14:10", "dep": "14:15"},
					{"code": "BRC", "arr": "18:30", "dep": "18:35"},
					{"code": "BCT", "arr": "22:00", "dep": None},
				],
			},
		}