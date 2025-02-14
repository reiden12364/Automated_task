import requests
from bs4 import BeautifulSoup
import re
import hashlib
import json

def save_text_to_file(text, filename):
    try:
        with open(filename, 'w') as file:
            file.write(text)
        print("Text has been successfully saved to the file", filename)
    except Exception as e:
        print("An error occurred while saving the text to the file:", e)

def extract_text_between_keywords(text, keyword1, keyword2):
    pattern = re.compile(rf'{re.escape(keyword1)}(.*?){re.escape(keyword2)}', re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    else:
        return None
    
def scrape_and_extract_text(url, looked_for):
    # Sending a GET request
    response = requests.get(url)
    
    # Checking if the request was successful
    if response.status_code == 200:
        # Retrieving the entire text from a plain-text page
        page_text = response.text
        
        # Searching for the index where the phrase "request to" starts
        index = page_text.find(looked_for)
        
        # If the phrase "request to" was found
        if index != -1:
            # Extracting the text after the phrase "request to"
            extracted_text = page_text[index + len(looked_for):]
            
            return extracted_text.strip()  # Removing any leading or trailing whitespace
        else:
            print("Phrase "+looked_for+" was not found on the page.")
            return None
    else:
        print("Error while retrieving the page:", response.status_code)
        return None

def send_get_request(url):
    try:
        # Sending a GET request
        response = requests.get(url)
        
        # Checking if the request was successful
        response.raise_for_status()
        
        # Retrieving the response page content
        page_content = response.text
        
        return page_content
    except requests.exceptions.RequestException as e:
        print("Error while sending the GET request:", e)
        return None
    
def send_get_request_with_headers(url, headers1):
    try:
        # Sending a GET request with headers
        response = requests.get(url, headers=headers1)
        
        # Checking if the request was successful
        response.raise_for_status()
        
        # Retrieving the response page content
        page_content = response.text
        
        return page_content
    except requests.exceptions.RequestException as e:
        print("Error while sending the GET request:", e)
        return None
# --------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
# STEP 1

    url = "https://task.zostansecurity.ninja/"
    
    extracted_text = scrape_and_extract_text(url, "request to")
    if extracted_text:
        print("Extracted text:", extracted_text)
    
    tekst1 = "https://task.zostansecurity.ninja" + extracted_text
    page_content = send_get_request(tekst1)
    if page_content:
        print("Response page content:")
        print(page_content)
# --------------------------------------------------------------------------------------------------

# STEP 2
index2 = page_content.find("request:")
extracted_text2 = page_content[index2 + len("request:"):]
# print(extracted_text2)
keyword1 = "X-challenge: "
keyword2 = "\n"
keyword3 = "X-timestamp: "
keyword4 = "\n"

# Extracting text between the key phrases
extracted_text3 = extract_text_between_keywords(extracted_text2, keyword1, keyword2)
if extracted_text3:
    print("Extracted text:")
    print(extracted_text3)
extracted_text4 = extract_text_between_keywords(extracted_text2, keyword3, keyword4)
if extracted_text4:
    print("Extracted text:")
    print(extracted_text4)

custom_headers = {
    "X-challenge": extracted_text3,
    "X-timestamp": extracted_text4
}

url_step2 = url + "/?step=2"
page_content2 = send_get_request_with_headers(url_step2, custom_headers)
if page_content2:
    print(page_content2)
    
# --------------------------------------------------------------------------------------------------

#  STEP 3
url_step3 = url + "/?step=3"

# print(extracted_text2)
keyword1 = "challenge: "
keyword2 = "\n"
keyword3 = "timestamp: "
keyword4 = "\n"

challenge = extract_text_between_keywords(page_content2, keyword1, keyword2)
if extracted_text3:
    print("Extracted text:")
    print(extracted_text3)
timestamp = extract_text_between_keywords(page_content2, keyword3, keyword4)
if extracted_text4:
    print("Extracted text:")
    print(extracted_text4)
    
data = "{"+extract_text_between_keywords(page_content2, "{\n", "\n}") + "}"
# print(data)
response_dict = json.loads(data)
# print(response_dict)
# Serialization and alphabetical sorting of keys
serialized_data = "&".join([f"{key}={response_dict[key]}" for key in sorted(response_dict.keys())])
# print(serialized_data)
# Calculating the SHA256 hash
hash_value = hashlib.sha256(serialized_data.encode()).hexdigest()

# Sending a POST request

response = requests.post(url_step3, data={
    "challenge": challenge,
    "timestamp": timestamp,
    "hash": hash_value
})
    
# Checking if the request was successful
print(response.raise_for_status())
print(response.text)

# Saving the text to a file
save_text_to_file(response.text, "etap")  
import base64
i = 0
encoded_email = 'HERE WAS A MULTIPLE BASE64 URL ENCODED MAIL'
decoded_email = encoded_email
while True:
    try:
        decoded_email = base64.b64decode(decoded_email).decode('utf-8')
        i = i+1
        
    except Exception as e:
        break

print(decoded_email) # Some_UUID@Some_Company.net
print(i)
