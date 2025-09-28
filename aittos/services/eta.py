from __future__ import annotations

from typing import Dict, List

from ..models.api import ScheduleModel, NetworkModel


def estimate_eta_seconds(network: NetworkModel, schedule: ScheduleModel, base_speed_kmph: float = 60.0) -> Dict[str, int]:
	# Placeholder computation: proportional to number of legs
	result: Dict[str, int] = {}
	for t in schedule.trains:
		legs = max(1, len(t.route_station_codes) - 1)
		result[t.train_id] = int(legs * 3600 / max(1.0, base_speed_kmph / 60.0))
	return result


def generate_speed_advisories(network: NetworkModel, schedule: ScheduleModel) -> Dict[str, List[Dict[str, int]]]:
	# Placeholder advisories: maintain constant nominal speed per leg
	advisories: Dict[str, List[Dict[str, int]]] = {}
	for t in schedule.trains:
		legs = max(1, len(t.route_station_codes) - 1)
		advisories[t.train_id] = [{"segment": i + 1, "recommended_kmph": 60} for i in range(legs)]
	return advisories