import requests
import json

# Function to obtain a vulnerability description from GPT-3.5-turbo using the chat model
def get_vulnerability_description(prompt):
    with open('secret.txt', 'r') as file:
        key = file.read().strip()
    api_key = key
    endpoint = "https://api.openai.com/v1/chat/completions"  # Use the chat model endpoint

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-3.5-turbo",  # Specify the model parameter
        "messages": [{"role": "system", "content": "You are a helpful assistant that provides vulnerability descriptions."}, {"role": "user", "content": prompt}],
        "max_tokens": 1000,  # Increase the max tokens to accommodate longer responses
    }

    response = requests.post(endpoint, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            response_text = response_data["choices"][0]["message"]["content"]

            # Check if there are more tokens available
            if "usage" in response_data and "total_tokens" in response_data["usage"]:
                total_tokens = response_data["usage"]["total_tokens"]
                while len(response_text.split()) < total_tokens:
                    data["messages"][1]["content"] = response_text  # Set the content to the previous response
                    response = requests.post(endpoint, json=data, headers=headers)
                    response_data = response.json()
                    response_text += response_data["choices"][0]["message"]["content"]

            return response_text
        else:
            return "No response from the model."
    else:
        return f"Error {response.status_code}: {response.text}"

# Main function
def main():
    # Step 1: Ask if the user wants to send a screenshot or text
    input_type = input("Do you want to send a screenshot or text? (screenshot/text): ").strip().lower()

    if input_type == "screenshot":
        screenshot_path = input("Please provide the path to the screenshot: ")
        prompt = f"Describe the vulnerability in the screenshot located at {screenshot_path} using the template:"
    elif input_type == "text":
        http_request = input("Please provide the HTTP request details: ")
        http_response = input("Please provide the HTTP response details: ")
        prompt = f"Describe the vulnerability in the HTTP request:\n{http_request}\n\nHTTP response:\n{http_response}\nUsing the template:"
    else:
        print("Invalid input. Please choose 'screenshot' or 'text'.")
        return

    # Step 2: Get vulnerability description from GPT-3
    description = get_vulnerability_description(prompt)

    # Step 3: Display the description in a readable form
    print("\nVulnerability Description:")
    print(description)

if __name__ == "__main__":
    main()
