import requests
from termcolor import colored


def image_generator_api(prompt):
    url = f"https://1yjs1yldj7.execute-api.us-east-1.amazonaws.com/default/ai_image?prompt={prompt}&aspect_ratio=16:9"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            print("Image generated successfully!")
            print(colored("Image URL:", 'green'), data['image_link'])
            return data['image_link']
        else:
            print("Error generating image:", data['message'])
            return None
        return 0
    else:
        print(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    prompt = "A beautiful sunset over the mountains."
    image_generator_api(prompt)