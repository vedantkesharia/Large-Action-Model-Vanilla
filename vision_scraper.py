from PIL import Image
import subprocess
import base64
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2024-05-01-preview"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

def resize_image(image_path, max_width=800):
    with Image.open(image_path) as img:
        width_percent = (max_width / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((max_width, height_size), Image.LANCZOS)
        img.save(image_path)

def image_b64(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()

def url2screenshot(url):
    print(f"Crawling {url}")

    if os.path.exists("screenshot.jpg"):
        os.remove("screenshot.jpg")

    result = subprocess.run(
        ["node", "screenshot.js", url],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("ERROR")
        return "Failed to scrape the website"

    resize_image("screenshot.jpg")

    if not os.path.exists("screenshot.jpg"):
        print("ERROR")
        return "Failed to scrape the website"
    
    b64_image = image_b64("screenshot.jpg")
    return b64_image

def visionExtract(b64_image, prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a web scraper, your job is to extract information based on a screenshot of a website and user's instruction.",
        },
        {
            "role": "user",
            "content": prompt,
            # "image": {
            #          "image_url": f"data:image/jpg;base64,{b64_image}"
            #      }
        },
        {
            "role": "user",
            "content": f"data:image/jpeg;base64,{b64_image}"
        }
    ]
    
    
    response = openai.chat.completions.create(
            model="Gpt4o",
            messages=messages,
            max_tokens=1024,
        )
   

    message = response.choices[0].message
    message_text = message.content

    if "ANSWER_NOT_FOUND" in message_text:
        print("ERROR: Answer not found")
        return "I was unable to find the answer on that website. Please pick another one"
    else:
        print(f"GPT: {message_text}")
        return message_text

def visionCrawl(url, prompt):
    b64_image = url2screenshot(url)

    print("Image captured")
    
    if b64_image == "Failed to scrape the website":
        return "I was unable to crawl that site. Please pick a different one."
    else:
        return visionExtract(b64_image, prompt)

response = visionCrawl("https://relevanceai.com/pricing", "Extract any information that you can")
print(response)



# import subprocess
# import base64
# import os
# from dotenv import load_dotenv
# import openai
# from openai import AzureOpenAI

# load_dotenv()

# openai.api_type = "azure"
# openai.api_version = "2024-05-01-preview"
# openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
# openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
#     api_version="2024-05-01-preview",
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
# )

# def image_b64(image):
#     with open(image, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# def url2screenshot(url):
#     print(f"Crawling {url}")

#     if os.path.exists("screenshot.jpg"):
#         os.remove("screenshot.jpg")

#     result = subprocess.run(
#         ["node", "screenshot.js", url],
#         capture_output=True,
#         text=True
#     )

#     exitcode = result.returncode
#     output = result.stdout

#     if not os.path.exists("screenshot.jpg"):
#         print("ERROR")
#         return "Failed to scrape the website"
    
#     b64_image = image_b64("screenshot.jpg")
#     return b64_image

# deploymentname = "Gpt4o"

# def visionExtract(b64_image, prompt):
#     response = openai.chat.completions.create(
#         model="Gpt4o",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a web scraper, your job is to extract information based on a screenshot of a website & user's instruction, read the image(upload if you have to inorder to read correctly) and answer the user's question.",
#             },
#             {
#                 "role": "user",
#                 "content": prompt,
#                 "image": {
#                     "image_url": f"data:image/jpeg;base64,{b64_image}"
#                 }
#             }
         
#         ],
#         max_tokens=1024,
#     )

#     message = response.choices[0].message
#     message_text =  message.content

#     if "ANSWER_NOT_FOUND" in message_text:
#         print("ERROR: Answer not found")
#         return "I was unable to find the answer on that website. Please pick another one"
#     else:
#         print(f"GPT: {message_text}")
#         return message_text

# def visionCrawl(url, prompt):
#     b64_image = url2screenshot(url)

#     print("Image captured")
    
#     if b64_image == "Failed to scrape the website":
#         return "I was unable to crawl that site. Please pick a different one."
#     else:
#         return visionExtract(b64_image, prompt)

# response = visionCrawl("https://relevanceai.com/pricing", "Extract the pricing info")
# print(response)








#works 90%
# import subprocess
# import base64
# import os
# from dotenv import load_dotenv
# import openai
# from openai import AzureOpenAI

# load_dotenv()

# openai.api_type = "azure"
# openai.api_version = "2024-05-01-preview"
# openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
# openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
#     api_version="2024-05-01-preview",
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
# )

# def image_b64(image):
#     with open(image, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# def url2screenshot(url):
#     print(f"Crawling {url}")

#     if os.path.exists("screenshot.jpg"):
#         os.remove("screenshot.jpg")

#     result = subprocess.run(
#         ["node", "screenshot.js", url],
#         capture_output=True,
#         text=True
#     )

#     exitcode = result.returncode
#     output = result.stdout

#     if not os.path.exists("screenshot.jpg"):
#         print("ERROR")
#         return "Failed to scrape the website"
    
#     b64_image = image_b64("screenshot.jpg")
#     return b64_image

# deploymentname = "Gpt4o"

# def visionExtract(b64_image, prompt):
#     response = openai.chat.completions.create(
#         model="Gpt4o",
#         messages=[
#             # {
#             #     "role": "system",
#             #     "content": "You are a web scraper, your job is to extract information based on a screenshot of a website & user's instruction.",
#             # },
#             # {
#             #     "role": "user",
#             #     "content": prompt,
#             #     "image": {
#             #         "image_url": f"data:image/jpeg;base64,{b64_image}"
#             #     }
#             # }
#              {
#                 "role": "system",
#                 "content": "You are a web scraper, your job is to extract information based on a screenshot of a website and user's instruction.",
#             },
#             {
#                 "role": "user",
#                 "content": prompt,
#             },
#             {
#                 "role": "user",
#                 "content": f"data:image/jpeg;base64,{b64_image}"
#             }
#         ],
#         max_tokens=1024,
#     )

#     message = response.choices[0].message
#     message_text =  message.content

#     if "ANSWER_NOT_FOUND" in message_text:
#         print("ERROR: Answer not found")
#         return "I was unable to find the answer on that website. Please pick another one"
#     else:
#         print(f"GPT: {message_text}")
#         return message_text

# def visionCrawl(url, prompt):
#     b64_image = url2screenshot(url)

#     print("Image captured")
    
#     if b64_image == "Failed to scrape the website":
#         return "I was unable to crawl that site. Please pick a different one."
#     else:
#         return visionExtract(b64_image, prompt)

# response = visionCrawl("https://relevanceai.com/pricing", "Extract the pricing info")
# print(response)












# # from openai import OpenAI
# import subprocess
# import base64
# import os
# from dotenv import load_dotenv
# import openai
# from openai import AzureOpenAI
# load_dotenv()

# # model = AzureOpenAI()
# # model.timeout = 30


# openai.api_type = "azure"
# openai.api_version = "2024-02-01"
# openai.api_base = "https://docs-test-001.openai.azure.com/"
# openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
#     # api_version="2024-02-01",
#     api_version="2024-05-01-preview",
#     azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
#     )
    
# # deployment_name='REPLACE_WITH_YOUR_DEPLOYMENT_NAME' #This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment. 
    


# def image_b64(image):
#     with open(image, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# def url2screenshot(url):
#     print(f"Crawling {url}")

#     if os.path.exists("screenshot.jpg"):
#         os.remove("screenshot.jpg")

#     result = subprocess.run(
#         ["node", "screenshot.js", url],
#         capture_output=True,
#         text=True
#     )

#     exitcode = result.returncode
#     output = result.stdout

#     if not os.path.exists("screenshot.jpg"):
#         print("ERROR")
#         return "Failed to scrape the website"
    
#     b64_image = image_b64("screenshot.jpg")
#     return b64_image


# deploymentname = "Gpt4o"

# def visionExtract(b64_image, prompt):
#     response = openai.chat.completions.create(
#         # model="gpt-4-vision-preview",
#         model="Gpt4o",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You a web scraper, your job is to extract information based on a screenshot of a website & user's instruction",
#             }
#         ] + [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image_url",
#                         "image_url": f"data:image/jpeg;base64,{b64_image}",
#                     },
#                     {
#                         "type": "text",
#                         "text": prompt,
#                     }
#                 ]
#             }
#         ],
#         max_tokens=1024,
#     )

#     message = response.choices[0].message
#     message_text = message.content

#     if "ANSWER_NOT_FOUND" in message_text:
#         print("ERROR: Answer not found")
#         return "I was unable to find the answer on that website. Please pick another one"
#     else:
#         print(f"GPT: {message_text}")
#         return message_text

# def visionCrawl(url, prompt):
#     b64_image = url2screenshot(url)

#     print("Image captured")
    
#     if b64_image == "Failed to scrape the website":
#         return "I was unable to crawl that site. Please pick a different one."
#     else:
#         return visionExtract(b64_image, prompt)

# response = visionCrawl("https://en.wikipedia.org/wiki/Elon_Musk", "give some information on elon musk")
# print(response)
















# from openai import OpenAI
# import subprocess
# import base64
# import os
# from dotenv import load_dotenv

# load_dotenv()

# model = OpenAI()
# model.timeout = 30

# def image_b64(image):
#     with open(image, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# def url2screenshot(url):
#     print(f"Crawling {url}")

#     if os.path.exists("screenshot.jpg"):
#         os.remove("screenshot.jpg")

#     result = subprocess.run(
#         ["node", "screenshot.js", url],
#         capture_output=True,
#         text=True
#     )

#     exitcode = result.returncode
#     output = result.stdout

#     if not os.path.exists("screenshot.jpg"):
#         print("ERROR")
#         return "Failed to scrape the website"
    
#     b64_image = image_b64("screenshot.jpg")
#     return b64_image

# def visionExtract(b64_image, prompt):
#     response = model.chat.completions.create(
#         model="gpt-4-vision-preview",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You a web scraper, your job is to extract information based on a screenshot of a website & user's instruction",
#             }
#         ] + [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image_url",
#                         "image_url": f"data:image/jpeg;base64,{b64_image}",
#                     },
#                     {
#                         "type": "text",
#                         "text": prompt,
#                     }
#                 ]
#             }
#         ],
#         max_tokens=1024,
#     )

#     message = response.choices[0].message
#     message_text = message.content

#     if "ANSWER_NOT_FOUND" in message_text:
#         print("ERROR: Answer not found")
#         return "I was unable to find the answer on that website. Please pick another one"
#     else:
#         print(f"GPT: {message_text}")
#         return message_text

# def visionCrawl(url, prompt):
#     b64_image = url2screenshot(url)

#     print("Image captured")
    
#     if b64_image == "Failed to scrape the website":
#         return "I was unable to crawl that site. Please pick a different one."
#     else:
#         return visionExtract(b64_image, prompt)

# response = visionCrawl("https://relevanceai.com/pricing", "Extract the pricing info")
# print(response)