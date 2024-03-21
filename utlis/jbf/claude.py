import anthropic
import re
import base64
import json

def base64_image(img_file):

    # Open the image in binary mode
    with open(img_file, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')

    return(data)




def analyze_image(apikey, img_file_fullpath, system_msg_file, prompt):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=apikey,
    )

    img = base64_image(img_file_fullpath)

    lines = []
    with open("system_msg.txt", "r") as file:
        lines = map(lambda x: re.sub("\n", "", x), file.readlines())

    system_msg = "\\n".join(lines)

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
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

    # print(message)

    data = extract_between_tags("metadata", message, True)
    return(data)



def extract_between_tags(tag: str, string: str, strip: bool = False) -> list[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    return json.loads(ext_list[0])


# athlete_sports_dict = json.loads(extract_between_tags("athlete_sports", message)[0])
# athlete_name_dicts = [
#     json.loads(d) for d in extract_between_tags("athlete_name", message)
# ]


def test():
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="my_api_key",
    )
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        system="you are a python programming expert. use the BeautifulSoup module to parse the html that is provided and return a \ndictionary of the contents of the table where class='metadata' the keys of the dictionary will come from the contents of the td element where class='label' and the value of the dictionary will come from the contents of the td element where class='value'",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "<html>\n<div id=\"2024-03-15_06-11-01_8874_png\" class=\"image-container\">\n    <hr>\n    <table>\n        <tr>\n            <td>\n                <div>2024-03-15_06-11-01_8874.png</div>\n            </td>\n            <td>\n                <table class='metadata'>\n                    <tr>\n                        <td class='label'>Negative Prompt</td>\n                        <td class='value'></td>\n                    </tr>\n                    <tr>\n                        <td class='label'>Refiner Switch</td>\n                        <td class='value'>0.5</td>\n                    </tr>\n                    <tr>\n                        <td class='label'>Sampler</td>\n                        <td class='value'>dpmpp_2m_sde_gpu</td>\n                    </tr>\n                    <tr>\n                        <td class='label'>Scheduler</td>\n                        <td class='value'>karras</td>\n                    </tr>\n                </table>\n            </td>\n        </tr>\n    </table>\n</div>\n<div id=\"2024-03-15\" class=\"image-container\">\n    <hr>\n    <table>\n        <tr>\n            <td>\n                <div>2024-03-15_06-11-01_8874.png</div>\n            </td>\n            <td>\n                <table class='metadata'>\n                    <tr>\n                        <td class='label'>Negative Prompt</td>\n                        <td class='value'></td>\n                    </tr>\n                    <tr>\n                        <td class='label'>Refiner Switch</td>\n                        <td class='value'>0.5</td>\n                    </tr>\n                    <tr>\n                        <td class='label'>Sampler</td>\n                        <td class='value'>dpmpp_2m_sde_gpu</td>\n                    </tr>\n                    <tr>\n                        <td class='label'>Scheduler</td>\n                        <td class='value'>karras</td>\n                    </tr>\n                </table>\n            </td>\n        </tr>\n    </table>\n</div>\n</html>",
                    }
                ],
            }
        ],
    )
    print(message.content)
