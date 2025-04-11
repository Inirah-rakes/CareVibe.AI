from flask import Flask, request
from agents.health import HealthAgent

app = Flask(__name__)
health_agent = HealthAgent()

@app.route('/iot/health', methods=['POST'])
def receive_health():
    data = request.json
    hr = data.get("heart_rate")
    sys = data.get("bp_systolic")
    dia = data.get("bp_diastolic")
    print(f"📡 IoT Data: HR={hr}, BP={sys}/{dia}")
    # Future: health_agent.monitor_health_from_iot(hr, sys, dia)
    return {"status": "received"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)