from flask import Flask, request, jsonify
import hashlib
import json
import os
from datetime import datetime

app = Flask(__name__)

class ProvenanceAttestationEngine:
    def __init__(self, output_file):
        self.output_file = output_file
        self.provenance_data = {
            "environment": self.get_environment_details(),
            "interactions": []
        }

    def get_environment_details(self):
        return {
            "os": os.name,
            "python_version": os.sys.version,
            "hostname": os.uname().nodename
        }

    def log_interaction(self, interaction_type, details):
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "type": interaction_type,
            "details": details
        }
        self.provenance_data["interactions"].append(interaction)

    def handle_webhook_event(self, event_data):
        for record in event_data['Records']:
            event_name = record['eventName']
            bucket_name = record['s3']['bucket']['name']
            object_name = record['s3']['object']['key']
            self.log_interaction(event_name, {
                "bucket_name": bucket_name,
                "object_name": object_name,
                "event_time": record['eventTime']
            })

    def export_attestation(self):
        with open(self.output_file, "w") as f:
            json.dump(self.provenance_data, f, indent=4)

attestation_engine = ProvenanceAttestationEngine("./logs/provenance_attestation.json")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        event_data = request.json
        if event_data and "Records" in event_data:
            attestation_engine.handle_webhook_event(event_data)
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "Invalid data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5011, debug=True)