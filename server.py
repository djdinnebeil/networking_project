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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
