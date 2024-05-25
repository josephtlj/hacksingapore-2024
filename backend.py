from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for simplicity
uploaded_data = []
notifications = []

@app.route('/upload', methods=['POST'])
def upload():
    """
    Endpoint to upload the selected station to the backend.
    """
    data = request.json
    station = data.get('station')
    if station:
        uploaded_data.append(station)
        return jsonify({"message": "Station uploaded successfully!"}), 200
    return jsonify({"message": "No station provided."}), 400

@app.route('/data', methods=['GET'])
def get_data():
    """
    Endpoint to retrieve the uploaded station data.
    """
    return jsonify({"uploaded_data": uploaded_data}), 200

@app.route('/notify', methods=['POST'])
def notify():
    """
    Endpoint to send a notification when a verified user with special needs selects a station.
    """
    data = request.json
    name = data.get('name')
    special_need = data.get('special_need')
    station = data.get('station')
    if name and special_need and station:
        notification = {
            "name": name,
            "special_need": special_need,
            "station": station
        }
        notifications.append(notification)
        return jsonify({"message": "Notification sent successfully!"}), 200
    return jsonify({"message": "Missing notification data."}), 400

@app.route('/notifications', methods=['GET'])
def get_notifications():
    """
    Endpoint to retrieve the list of notifications.
    """
    return jsonify({"notifications": notifications}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
