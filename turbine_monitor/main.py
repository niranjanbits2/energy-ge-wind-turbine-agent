import functions_framework
import json
import random
from datetime import datetime

@functions_framework.http
def turbine_monitor(request):
    """Fetch simulated telemetry for a wind turbine."""
    request.headers.get('Access-Control-Request-Method')
    
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    turbine_id = None
    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        turbine_id = body.get('turbine_id', 'T-001')
    else:
        turbine_id = request.args.get('turbine_id', 'T-001')

    # Simulate telemetry data
    wind_speed = round(random.uniform(6, 18), 1)
    power_output = round(wind_speed * 0.3 * random.uniform(0.85, 1.0), 2)
    gearbox_temp = round(random.uniform(55, 88), 1)
    vibration = round(random.uniform(3, 12), 2)
    rpm = round(random.uniform(10, 14), 1)
    
    # Determine status
    alerts = []
    status = "NORMAL"
    
    if gearbox_temp > 80:
        alerts.append("FC-101: Gearbox oil temperature high")
        status = "FAULT"
    if vibration > 10:
        alerts.append("FC-202: Generator vibration high")
        status = "WARNING" if status == "NORMAL" else status
    if power_output < wind_speed * 0.2:
        alerts.append("Power curve deviation detected")
        status = "WARNING" if status == "NORMAL" else status

    response = {
        "turbine_id": turbine_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": status,
        "telemetry": {
            "wind_speed_ms": wind_speed,
            "power_output_mw": power_output,
            "rotor_rpm": rpm,
            "gearbox_temp_c": gearbox_temp,
            "vibration_mms": vibration,
            "blade_pitch_deg": round(random.uniform(0, 15), 1),
            "availability_pct": round(random.uniform(94, 99), 1)
        },
        "alerts": alerts,
        "recommended_action": "Immediate inspection required" if status == "FAULT" else ("Monitor closely" if status == "WARNING" else "No action required")
    }
    
    headers = {'Access-Control-Allow-Origin': '*'}
    return (json.dumps(response), 200, headers)
