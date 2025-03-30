from flask import Flask, request
import time
import threading
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1355854049270038639/KzwEP5eTgCfEo1CNAu75uYfQscecIgj1r8zKwyzk1yF2O4M2gZ13XFKh_cVAx-O9ZXL_"  # Replace with your Discord webhook

last_heartbeat = time.time()  # Stores the last received heartbeat time

@app.route('/heartbeat', methods=['GET'])
def receive_heartbeat():
    global last_heartbeat
    last_heartbeat = time.time()  # Update the last heartbeat time
    return "Heartbeat received", 200  # Respond to the computer

def monitor_computer():
    global last_heartbeat
    was_online = True  # Tracks last known state

    while True:
        time.sleep(60)  # Check every 60 seconds
        if time.time() - last_heartbeat > 120:  # More than 2 minutes since last heartbeat?
            if was_online:  # If it was online before
                requests.post(WEBHOOK_URL, json={"content": "Your computer is now offline."})
                print("Sent offline message to Discord")
                was_online = False  # Update state
        else:
            if not was_online:  # If it was offline before
                requests.post(WEBHOOK_URL, json={"content": "Your computer is now online."})
                print("Sent online message to Discord")
                was_online = True  # Update state

# Start monitoring in a separate thread
threading.Thread(target=monitor_computer, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
