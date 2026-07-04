import functions_framework
import json
import random
import string
from datetime import datetime, timedelta

@functions_framework.http
def workorder_tool(request):
    """Create a maintenance work order for a wind turbine."""
    
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    body = request.get_json(silent=True) or {}
    
    turbine_id  = body.get('turbine_id', 'T-001')
    fault_code  = body.get('fault_code', 'FC-000')
    priority    = body.get('priority', 'MEDIUM')
    description = body.get('description', 'Routine maintenance required')

    # Generate work order
    wo_id = 'WO-' + ''.join(random.choices(string.digits, k=8))
    
    # Estimate schedule based on priority
    now = datetime.utcnow()
    schedule_map = {
        'CRITICAL': now + timedelta(hours=2),
        'HIGH':     now + timedelta(hours=8),
        'MEDIUM':   now + timedelta(days=1),
        'LOW':      now + timedelta(days=7),
    }
    scheduled_time = schedule_map.get(priority.upper(), now + timedelta(days=1))
    
    # Parts lookup
    parts_map = {
        'FC-101': ['GB-FILTER-001 (Oil Filter) x1', 'Mobilgear SHC XMP 320 (200L)'],
        'FC-102': ['GB-PUMP-002 (Oil Pump) x1', 'Seal Kit x1'],
        'FC-201': ['GEN-FILTER-003 (Air Filter) x1'],
        'FC-202': ['GEN-BEAR-004 (Main Bearing) x1'],
        'FC-301': ['BLADE-MOTOR-005 (Pitch Motor) x1'],
    }
    parts = parts_map.get(fault_code, ['Standard maintenance kit'])

    response = {
        "work_order_id": wo_id,
        "status": "CREATED",
        "turbine_id": turbine_id,
        "fault_code": fault_code,
        "priority": priority.upper(),
        "description": description,
        "created_at": now.isoformat() + "Z",
        "scheduled_for": scheduled_time.isoformat() + "Z",
        "assigned_team": "Field Engineering Team - Palm Beach",
        "estimated_duration_hours": 6,
        "parts_required": parts,
        "safety_requirements": [
            "Lock-out Tag-out (LOTO) required",
            "Harness and fall protection mandatory above 2m",
            "Two-person minimum for gearbox work"
        ],
        "message": f"Work order {wo_id} created successfully. Team will arrive by {scheduled_time.strftime('%Y-%m-%d %H:%M')} UTC."
    }
    
    headers = {'Access-Control-Allow-Origin': '*'}
    return (json.dumps(response), 200, headers)
