from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class StationStop(BaseModel):
	code: str
	arrival: Optional[str] = Field(default=None)
	departure: Optional[str] = Field(default=None)


class TrainPlan(BaseModel):
	train_id: str
	route_station_codes: List[str]
	planned_times: List[str]
	priority: int = 1


class NetworkSection(BaseModel):
	section_id: str
	blocks: List[str]


class NetworkModel(BaseModel):
	sections: List[NetworkSection]
	platforms: Dict[str, int] = Field(default_factory=dict)


class ScheduleModel(BaseModel):
	trains: List[TrainPlan]


class OptimizeRequest(BaseModel):
	network: NetworkModel
	schedule: ScheduleModel
	headway_seconds: int = 120


class OptimizeResponse(BaseModel):
	sequence: List[str]
	total_travel_time_seconds: int
	objective_value: float


class WhatIfRequest(OptimizeRequest):
	pass