from __future__ import annotations

from typing import Any, Dict

from ..models.api import OptimizeRequest, OptimizeResponse
from .optimizer_ilp import optimize_schedule


def reoptimize_on_incident(req: OptimizeRequest, incident: Dict[str, Any]) -> OptimizeResponse:
	# Future: remove blocked blocks/routes from req.network before re-optimizing
	return optimize_schedule(req)