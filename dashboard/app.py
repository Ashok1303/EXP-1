import os
import json
import requests
import streamlit as st

BACKEND_DEFAULT = os.getenv("FRONTEND_BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="AITTOS Controller", layout="wide")
st.title("AITTOS: AI-Powered Track & Traffic Optimization")

with st.sidebar:
	st.header("Settings")
	backend_url = st.text_input("Backend URL", BACKEND_DEFAULT)
	st.markdown("---")
	st.caption("Fetch IRCTC train details by number")
	train_number = st.text_input("Train Number", "12952")
	if st.button("Fetch Train Details"):
		try:
			resp = requests.get(f"{backend_url}/train/{train_number}", timeout=20)
			resp.raise_for_status()
			st.session_state["train_details"] = resp.json()
			st.success("Fetched train details")
		except Exception as e:  # noqa: BLE001
			st.error(str(e))

col1, col2 = st.columns(2)

with col1:
	st.subheader("Train Details")
	train_details = st.session_state.get("train_details")
	if train_details:
		st.json(train_details)
	else:
		st.info("Use the sidebar to fetch train details.")

with col2:
	st.subheader("Optimization")
	example_payload = {
		"network": {
			"sections": [{"section_id": "S1", "blocks": ["B1"]}],
			"platforms": {"NDLS": 5, "BCT": 5},
		},
		"schedule": {
			"trains": [
				{"train_id": "T1", "route_station_codes": ["NDLS", "BCT"], "planned_times": ["10:00", "22:00"], "priority": 2},
				{"train_id": "T2", "route_station_codes": ["NDLS", "BCT"], "planned_times": ["10:10", "22:10"], "priority": 1},
			]
		},
		"headway_seconds": 180,
	}

	payload_text = st.text_area("Optimize Request JSON", json.dumps(example_payload, indent=2), height=240)
	if st.button("Run Optimize"):
		try:
			req = json.loads(payload_text)
			resp = requests.post(f"{backend_url}/optimize", json=req, timeout=30)
			resp.raise_for_status()
			st.session_state["optimize_result"] = resp.json()
			st.success("Optimization complete")
		except Exception as e:  # noqa: BLE001
			st.error(str(e))

	result = st.session_state.get("optimize_result")
	if result:
		st.json(result)