import requests
import json
import base64

def encode_image64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    

# print(image_url)

header = {
'Content-Type':'application/json'
}
def interact_with_chatbot():
    # Replace with your server endpoint
    url = 'http://localhost:8080/ai'
    
    while True:
        # Take user input
        global image_url
        user_input = input("You: ")
        image = input('image? :')
        if image == 'yes':
            # image_url = input("Image_Url:")
            image_url = encode_image64('test\leaking_toilet_image.png')
            payload = {'query': user_input, "image_url":image_url}
            print(payload)
        else:
            image_url = None
            payload = {'query': user_input}
        # Create the payload
        
        
        try:
            # Send a POST request
            response = requests.post(url, data=json.dumps(payload), headers=header)
            
            # Raise an exception if the request was unsuccessful
            # response.raise_for_status()
            
            # Print the response from the server
            chatbot_response = response.json()
            print("Chatbot:", chatbot_response.get('content', 'No response from chatbot'))
            
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            break

if __name__ == "__main__":
    interact_with_chatbot()
