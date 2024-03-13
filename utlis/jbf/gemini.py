import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv


def analyze_image(google_api_key, model, file, prompt):
    try:
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel(model)
        img = PIL.Image.open(file)
        response = model.generate_content([prompt, img], stream=True)
        response.resolve()
        return(response.text)

    except Exception as e:
        raise e




def main():
    pass

if __name__ == "__main__":
    main()



