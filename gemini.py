# https://pyimagesearch.com/2024/02/12/image-processing-with-gemini-pro/

# https://aistudio.google.com/app/apikey
# AIzaSyCG0XPw_w0R5R3Lohqv07CbbZOUcazzOko

# https://ai.google.dev/tutorials/python_quickstart

# python -m venv venv
# venv\Scripts\activate.bat

# python.exe -m pip install --upgrade pip

# pip install -q -U google-generativeai
# pip install pillow

import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv

# import pathlib
# import textwrap


# Load the .env file
load_dotenv()

# Access variables using os.getenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


image_file = "test.png"
prompt = """For this image.
Give me 5 title options. A description and a comma separated keyword list.
Make sure to mention the color scheme, if the image represents a specific holiday or nationality, artistic style, theme and subject matter.
DO NOT mention products that the image would be good for.
DO NOT give me Additional Notes.
Use high-quality SEO keywords."""

def analyze_image(google_api_key, file, prompt):
    genai.configure(api_key=google_api_key)

    # model = genai.GenerativeModel('gemini-pro')
    # Generate text based on a prompt
    # response = model.generate_content("The opposite of hot is")
    # print(response.text)  # cold.


    model = genai.GenerativeModel('gemini-pro-vision')
    img = PIL.Image.open(file)
    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    return(response.text)



def main():
    print(analyze_image(google_api_key, image_file, prompt))



if __name__ == "__main__":
    main()



