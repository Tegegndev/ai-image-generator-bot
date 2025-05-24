import requests
from termcolor import colored
from config import API_URL


def image_generator_api(prompt):
    url = f"{API_URL}/default/ai_image?prompt={prompt} add text @tegegn at the bottom &aspect_ratio=16:9"
    print(colored(url, 'blue'), prompt)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            print(colored("Imagae gegenaration secuss:", 'green'), data['image_link'])
            return data['image_link']
        else:
            print("Error generating image:", data['message'])
            return None
        return 0
    else:
        print(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    prompt = "A beautiful sunset over the mountains.  A MAN SITTING ON A ROCK and playing guitar with girl"
    result = image_generator_api(prompt)
    print(result)