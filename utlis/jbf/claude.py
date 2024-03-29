import anthropic
import re
import base64
import json
import os
import logging
from dotenv import load_dotenv

log = logging.getLogger(__name__)

# Load the .env file
load_dotenv()

# Access variables using os.getenv()
api_key = os.getenv("ANTHROPIC_API_KEY")


def base64_image(img_file):

    # Open the image in binary mode
    with open(img_file, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')

    return(data)




def analyze_image(img_file_fullpath, system_msg_file, prompt, ai_model):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=api_key,
    )

    img = base64_image(img_file_fullpath)

    lines = []
    with open(system_msg_file, "r") as file:
        lines = map(lambda x: re.sub("\n", "", x), file.readlines())

    system_msg = "\\n".join(lines)

    try:
        message = client.messages.create(
            model=ai_model,
            max_tokens=2000,
            temperature=0,
            system=system_msg,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img,
                            },
                        },
                    ],
                }
            ],
        ).content[0].text
    except anthropic.error.APIError as e:
        log.error(f"Error: {e.message}")
        return None
    except Exception as e:
        log.error(f"Error: {e}")
        return None

    data = extract_between_tags("metadata", message, True)
    return(data)



def extract_between_tags(tag: str, string: str, strip: bool = False) -> list[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    return json.loads(ext_list[0])



