import requests
import json

# Load the configuration from the external file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract the API key and URL from the config
api_key = config['api_key']
url = config['url']

# Update headers with the authorization token
headers = config['headers']
headers['Authorization'] = f"Bearer {api_key}"

# Extract the payload from the config
payload = config['payload']

# Extract the desired filename from the config
filename = config['filename']

try:
    # Send a POST request to the local server
    response = requests.post(url, headers=headers, json=payload, timeout=5)
    response.raise_for_status()  # Raises an HTTPError if the status is not 200

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Iterate over the generated images and save them
        for i, image_info in enumerate(data['data']):
            image_url = image_info['url']
            try:
                image_response = requests.get(image_url, timeout=5)

                if image_response.status_code == 200:
                    # Save the image with the desired filename and index
                    image_filename = f"{filename}{i + 1}.png"
                    with open(image_filename, 'wb') as img_file:
                        img_file.write(image_response.content)
                    print(f"Image saved as {image_filename}")
                else:
                    print(f"Failed to download image {i + 1}: {image_response.status_code} {image_response.content}")
            except requests.RequestException as e:
                print(f"Error downloading image {i + 1}: {e}")
    else:
        print(f"Failed to generate image: {response.status_code}")
        print(response.text)

except requests.ConnectionError:
    print(f"Error: Could not connect to the server at {url}. Is the server running?")
except requests.Timeout:
    print("Error: The request timed out. Please check your network or try again later.")
except requests.RequestException as e:
    print(f"An unexpected error occurred: {e}")
