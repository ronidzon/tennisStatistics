import requests


def talkToChatGpt():
    import requests

    # Set the API endpoint URL
    api_url = "https://api.openai.com/v1/images/generations"

    # Set the API key
    api_key = "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"

    # Set the model to use
    model = "image-alpha-001"

    # Set the file to share
    file_path = "C:\\Users\97254\PycharmProjects\\tennisStatistics\chatgpt.txt"

    # Open the file in binary mode
    with open(file_path, "rb") as file:
        # Set the request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Set the request parameters
        params = {
            "model": model,
            "prompt": "Sharing a file with ChatGPT"
        }

        # Send the request
        response = requests.post(api_url, headers=headers, params=params, data=file)

        # Check the status code
        if response.status_code == 200:
            # Print the response JSON
            print(response.json())
        else:
            # Print the error message
            print(response.text)


if __name__ == '__main__':
    talkToChatGpt()
