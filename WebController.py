from flask import Flask, request, jsonify, render_template_string


class WebController:
    def __init__(self, controller):
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule("/control", "control", self.control, methods=["POST"])
        self.motor_speed = 0
        self.controller = controller

    def index(self):
        html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Motor Control</title>
                <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
            }
            .controller {
                display: grid;
                grid-template-columns: repeat(3, 100px);
                grid-template-rows: 100px 100px 100px;
                gap: 10px;
                text-align: center;
            }
            .controller button {
                font-size: 24px;
                padding: 20px;
                cursor: pointer;
                border: 2px solid #000;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
            .controller button:active {
                background-color: #ccc;
            }
            #up {
                grid-column: 2 / 3;
                grid-row: 1 / 2;
            }
            #down {
                grid-column: 2 / 3;
                grid-row: 3 / 4;
            }
            #left {
                grid-column: 1 / 2;
                grid-row: 2 / 3;
            }
            #right {
                grid-column: 3 / 4;
                grid-row: 2 / 3;
            }
        </style>
            </head>
            <body>
                        <div class="controller">
            <button id="up" 
                    onmousedown="sendCommand('up')" 
                    onmouseup="sendCommand('stop')" 
                    ontouchstart="sendCommand('up')" 
                    ontouchend="sendCommand('stop')">↑</button>
            
            <button id="left" 
                    onmousedown="sendCommand('left')" 
                    onmouseup="sendCommand('stop')" 
                    ontouchstart="sendCommand('left')" 
                    ontouchend="sendCommand('stop')">←</button>
            
            <button id="right" 
                    onmousedown="sendCommand('right')" 
                    onmouseup="sendCommand('stop')" 
                    ontouchstart="sendCommand('right')" 
                    ontouchend="sendCommand('stop')">→</button>
            
            <button id="down" 
                    onmousedown="sendCommand('down')" 
                    onmouseup="sendCommand('stop')" 
                    ontouchstart="sendCommand('down')" 
                    ontouchend="sendCommand('stop')">↓</button>

            <button onclick="sendCommand('stop')">Stop</button>
        </div>

                <script>
                    function sendCommand(command) {
                        fetch("/control", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ command: command })
                        })
                        .then(response => response.json())
                        .catch(error => console.error("Error:", error));
                    }
                </script>
            </body>
            </html>
            """
        return render_template_string(html)

    def control(self):
        # Handle motor power update
        data = request.get_json()
        command = data.get("command")

        # TODO: Add another motor and figure out a way of either steering in reverse or stopping the motor completely to turn
        if command == "up":
            self.motor_speed = 100  # Example for going forward
        elif command == "down":
            self.motor_speed = 1  # Example for going backward (stopping motor)
        elif command == "left":
            self.motor_speed = 1  # Example for turning left
        elif command == "right":
            self.motor_speed = 0  # Example for turning right
        elif command == "stop":
            self.motor_speed = 0  # Stop all motors

        self.controller.change_motor_speed(self.motor_speed)
        return jsonify({"message": "Motor power set", "speed": self.motor_speed})

    def run(self):
        self.app.run(host="0.0.0.0", port=5000)
