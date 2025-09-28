from __future__ import annotations

from typing import Dict

import networkx as nx

from ..models.api import NetworkModel


class DigitalTwin:
	def __init__(self, network: NetworkModel) -> None:
		self.network = network
		self.graph = self._build_graph(network)

	def _build_graph(self, network: NetworkModel) -> nx.DiGraph:
		g = nx.DiGraph()
		# Add blocks as nodes and sequential edges within each section
		for section in network.sections:
			prev = None
			for block in section.blocks:
				g.add_node(block, section=section.section_id)
				if prev is not None:
					g.add_edge(prev, block, section=section.section_id)
				prev = block
		return g

	def platform_capacity(self, station_code: str) -> int:
		return int(self.network.platforms.get(station_code, 0))


def build_digital_twin(network: NetworkModel) -> DigitalTwin:
	return DigitalTwin(network)