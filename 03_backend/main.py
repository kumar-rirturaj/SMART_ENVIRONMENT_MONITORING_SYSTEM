from flask import Flask, request, jsonify
import requests
from datetime import datetime
import csv
import os

app = Flask(__name__)

# =========================
# CONFIGURATION
# =========================
TEMPERATURE_THRESHOLD = 27
TELEGRAM_BOT_TOKEN = "8554070883:AAFdQAlCHXYFQNoGzrIQEseSoaeb-X6esaQ"
TELEGRAM_CHAT_ID = "7338773200"

# =========================
# GLOBAL VARIABLES
# =========================
last_alert_state = False
latest_temperature = "No data yet"
latest_humidity = "No data yet"

CSV_FILE = "sensor_data.csv"

# =========================
# CSV INITIALIZATION
# =========================
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature (°C)", "Humidity (%)"])

# =========================
# TELEGRAM FUNCTION
# =========================
def send_telegram_alert(temp, humidity):
    message = (
        f"🚨 TEMPERATURE ALERT 🚨\n\n"
        f"Temperature: {temp}°C\n"
        f"Humidity: {humidity}%\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    url = f"https://api.telegram.org/bot8554070883:AAFdQAlCHXYFQNoGzrIQEseSoaeb-X6esaQ/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)
    print("Telegram status:", response.status_code)


# =========================
# HOME ROUTE (BROWSER VIEW)
# =========================
@app.route("/")
def home():
    return f"""
    <h2>IoT Temperature Monitoring System</h2>
    <p><strong>Latest Temperature:</strong> {latest_temperature} °C</p>
    <p><strong>Latest Humidity:</strong> {latest_humidity} %</p>
    <p>Threshold: {TEMPERATURE_THRESHOLD} °C</p>
    """


# =========================
# SENSOR API ROUTE
# =========================
@app.route('/api/sensor', methods=['POST'])
def receive_data():
    global last_alert_state
    global latest_temperature
    global latest_humidity

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except:
        return jsonify({"error": "Invalid data format"}), 400

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Update latest values
    latest_temperature = temperature
    latest_humidity = humidity

    # Console logging
    print("\n====================================", flush=True)
    print("New Sensor Reading Received", flush=True)
    print("Timestamp:", timestamp, flush=True)
    print("Temperature:", temperature, "°C", flush=True)
    print("Humidity:", humidity, "%", flush=True)
    print("====================================\n", flush=True)


    # CSV logging
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, temperature, humidity])

    # Threshold check
    alert_triggered = temperature > TEMPERATURE_THRESHOLD

    if alert_triggered and not last_alert_state:
        print("Threshold crossed → Sending Telegram alert")
        send_telegram_alert(temperature, humidity)

    last_alert_state = alert_triggered

    return jsonify({
        "status": "success",
        "buzzer": alert_triggered
    })


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)














