from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# Lista de tokens de autenticación válidos
VALID_TOKENS = [
    "token1",
    "token2",
    "token3"
]

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    service_name = db.Column(db.String(255), nullable=False)
    log_level = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, timestamp, service_name, log_level, message):
        self.timestamp = timestamp
        self.service_name = service_name
        self.log_level = log_level
        self.message = message

# Middleware de autenticación
@app.before_request
def authenticate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header.split(" ")[1] not in VALID_TOKENS:
        return jsonify({"message": "Unauthorized"}), 401

@app.route('/logs', methods=['POST'])
def create_log():
    data = request.get_json()
    try:
        timestamp = datetime.fromisoformat(data['timestamp'])
        service_name = data['service_name']
        log_level = data['log_level']
        message = data['message']

        new_log = Log(timestamp=timestamp, service_name=service_name, log_level=log_level, message=message)
        db.session.add(new_log)
        db.session.commit()

        return jsonify({"message": "Log received"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error saving log"}), 500

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        log_level = request.args.get('log_level')

        query = Log.query

        if start_date:
            query = query.filter(Log.timestamp >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Log.timestamp <= datetime.fromisoformat(end_date))
        if log_level:
            query = query.filter(Log.log_level == log_level)

        logs = query.all()
        return jsonify([{
            'id': log.id,
            'timestamp': log.timestamp.isoformat(),
            'service_name': log.service_name,
            'log_level': log.log_level,
            'message': log.message,
            'received_at': log.received_at.isoformat()
        } for log in logs]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error retrieving logs"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
