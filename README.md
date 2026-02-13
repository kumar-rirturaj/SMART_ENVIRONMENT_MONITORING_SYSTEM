Smart Environment Monitoring System
Overview

This project is an IoT-based Smart Environment Monitoring System using ESP32 and Flask backend. It monitors temperature and humidity, logs data, triggers alerts, and controls a buzzer.

System Architecture

1.ESP32 reads temperature and humidity using DHT11.

2.Data is formatted in JSON.

3.ESP32 sends HTTP POST request to Flask backend.

4.Backend:

Validates data

Logs to CSV

Displays latest values in browser

Checks threshold

Sends Telegram alert

Returns buzzer status

5.ESP32 activates buzzer if threshold exceeded.

Technologies Used

ESP32

DHT11 Sensor

Flask (Python)

Telegram Bot API

CSV Logging

Git & GitHub

Features

Real-time monitoring

Web interface

Telegram alert system

CSV data logging

Threshold-based buzzer alert

Errors Faced & Solutions

1.HTTP Response -1
Cause: Firewall blocking port 5000
Solution: Created inbound rule in Windows Firewall

2.Telegram not sending alerts
Cause: Incorrect token and threshold logic
Solution: Verified token and added threshold state control

3.Buzzer not sounding
Cause: Wrong GPIO pin connection
Solution: Corrected wiring

4.Browser not displaying data
Cause: No homepage route
Solution: Added "/" route and live display

Future Improvements

Add database instead of CSV

Add auto-refresh frontend

Deploy backend to cloud server