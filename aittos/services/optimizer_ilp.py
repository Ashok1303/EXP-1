from __future__ import annotations

from typing import List

import pulp

from ..models.api import OptimizeRequest, OptimizeResponse


def optimize_schedule(req: OptimizeRequest) -> OptimizeResponse:
	trains: List[str] = [t.train_id for t in req.schedule.trains]
	if len(trains) <= 1:
		return OptimizeResponse(sequence=trains, total_travel_time_seconds=0, objective_value=0.0)

	# Decision vars: order of trains via pairwise precedence x[i,j] = 1 if i before j
	pairs = [(i, j) for i in trains for j in trains if i != j]
	model = pulp.LpProblem("throughput_max", pulp.LpMinimize)
	x = pulp.LpVariable.dicts("precede", (trains, trains), lowBound=0, upBound=1, cat=pulp.LpBinary)

	# Anti-symmetry and no self precedence
	for i in trains:
		x[i][i].lowBound = 0
		x[i][i].upBound = 0
	for i, j in pairs:
		model += x[i][j] + x[j][i] == 1

	# Transitivity via triangle inequalities (simplified)
	for a in trains:
		for b in trains:
			for c in trains:
				if len({a, b, c}) == 3:
					model += x[a][b] + x[b][c] - x[a][c] <= 1

	# Objective: proxy to minimize inversions wrt priority (higher priority should be earlier)
	priority = {t.train_id: t.priority for t in req.schedule.trains}
	model += pulp.lpSum((priority[j] - priority[i]) * x[i][j] for i, j in pairs)

	model.solve(pulp.PULP_CBC_CMD(msg=False))

	# Derive order by sorting with score s[i] = sum_j x[j,i]
	scores = {i: sum(int(pulp.value(x[j][i])) for j in trains if j != i) for i in trains}
	ordered = sorted(trains, key=lambda k: scores[k])

	# Placeholder total time and objective
	objective_value = pulp.value(model.objective) if model.objective is not None else 0.0
	return OptimizeResponse(sequence=ordered, total_travel_time_seconds=len(ordered) * req.headway_seconds, objective_value=float(objective_value or 0.0))