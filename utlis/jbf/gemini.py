import google.generativeai as genai
import PIL.Image

# https://pyimagesearch.com/2024/02/12/image-processing-with-gemini-pro/
# https://aistudio.google.com/app/apikey
# https://ai.google.dev/tutorials/python_quickstart


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

def parse_description(google_api_key, model, prompt, desc, parts):
    """
Parse the description using the Google Generative AI API.

Args:
    google_api_key (str): The API key for accessing the Google Generative AI API.
    model (str): The name of the generative model to use.
    prompt (str): The prompt to use for generating the content.
    desc (str): The description to include in the prompt.
    parts (list): A list of parts to generate content for.

Returns:
    parsed: A dictionary containing the generated content for each part.

Raises:
    Exception: If there is an error while parsing the description.

"""
    try:
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel(model)
        parsed = {}

        for part in parts:
            prompt1 = prompt.format(part=part, desc=desc)
            response = model.generate_content(prompt1)
            response.resolve()
            parsed[part] = response.text

        return parsed

    except Exception as e:
        raise e


def main():
    pass

if __name__ == "__main__":
    main()



