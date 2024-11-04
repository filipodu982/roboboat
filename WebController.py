from flask import Flask, request, jsonify, render_template_string


class WebController:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule(
            "/set_power", "set_power", self.set_power, methods=["POST"]
        )
        self.motor_speed = 0

    def index(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Motor Control</title>
        </head>
        <body>
            <h2>Motor Control</h2>
            <input type="range" id="motorSlider" min="0" max="100" value="0">
            <p>Motor Power: <span id="powerValue">0</span></p>
            <button onclick="sendMotorPower()">Set Motor Power</button>

            <script>
                const slider = document.getElementById("motorSlider");
                const powerValue = document.getElementById("powerValue");

                slider.oninput = function() {
                    powerValue.textContent = this.value;
                }

                function sendMotorPower() {
                    const power = slider.value;
                    fetch("/set_power", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ power: power })
                    })
                    .then(response => response.json())
                    .then(data => alert("Motor power set to: " + data.speed))
                    .catch(error => console.error("Error:", error));
                }
            </script>
        </body>
        </html>
        """
        return render_template_string(html)

    def set_power(self, controller):
        # Handle motor power update
        data = request.get_json()
        self.motor_speed = int(data.get("power", 0))
        controller.change_motor_speed(self.motor_speed)
        return jsonify({"message": "Motor power set", "speed": self.motor_speed})

    def run(self):
        self.app.run(host="0.0.0.0", port=5000)
