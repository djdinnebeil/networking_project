from flask import Flask, request, jsonify, send_file
import os
import random

app = Flask(__name__)

# Directory containing static images
IMAGE_DIR = './images'

@app.route('/generate', methods=['POST'])
def generate_image():
    # Check the headers for the Authorization token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401

    # Log the incoming request headers for learning purposes
    print("Received Headers:", dict(request.headers))

    # Select a random image from the directory
    images = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.png')]
    if not images:
        return jsonify({"error": "No images available"}), 404

    # Mimicking image generation
    image_name = random.choice(images)
    image_path = os.path.join(IMAGE_DIR, image_name)

    # Respond with a fake JSON response as if an image was generated
    return jsonify({
        "data": [
            {"url": f"http://127.0.0.1:5000/static/{image_name}"}
        ]
    })

# Serve static images
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_file(os.path.join(IMAGE_DIR, filename))

@app.route('/image/<int:number>')
def get_image(number):
    return send_file(os.path.join(IMAGE_DIR, f'ff7_{number}.png'))

@app.route('/status/<int:code>', methods=['GET', 'POST'])
def return_status(code):
    """
    Demonstrates returning different HTTP status codes.
    Accepts a status code as a URL parameter.
    """
    # Status codes and their corresponding messages
    status_messages = {
        200: "OK - Successful request.",
        201: "Created - Resource was successfully created.",
        204: "No Content - Request succeeded, but no content to return.",
        400: "Bad Request - Invalid request syntax or parameters.",
        401: "Unauthorized - Authentication is required.",
        403: "Forbidden - You do not have permission to access this resource.",
        404: "Not Found - Resource does not exist.",
        500: "Internal Server Error - The server encountered an error.",
        502: "Bad Gateway - Server received an invalid response from an upstream server.",
        503: "Service Unavailable - Server is temporarily overloaded or down.",
    }

    # Get the message for the status code or use a generic message
    message = status_messages.get(code, f"Custom Status - Code {code}")

    # Log the status code and request method for demonstration
    print(f"Received {request.method} request, returning status code: {code}")

    # Return a JSON response with the status code and message
    return jsonify({"status": code, "message": message}), code

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
