import json
try:
    with open('projects_json.txt', 'r', encoding='utf-16le') as f:
        data = json.load(f)
    for p in data.get('result', []):
        print(f"ID: {p['projectId']} - Name: {p['displayName']}")
except Exception as e:
    print(f"Error: {e}")
    # Try alternate encoding
    try:
        with open('projects_json.txt', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for p in data.get('result', []):
            print(f"ID: {p['projectId']} - Name: {p['displayName']}")
    except Exception as e2:
        print(f"Error with utf-8: {e2}")
