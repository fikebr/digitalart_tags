import anthropic

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


###################

"""
you are an art critic. i'm going to give you a picture and you are going to analyze it.
I want you to tell me...

1. The general art style of the piece.
2. A description of the subject of the piece
3. The emotion that the artist was trying to portray
4. the color scheme used.

Next tell me...

1. A single word that best describes the style
2. A single sentence that best describes the subject matter
3. A single word that best describes the emotion
4. The two most prominent colors used.
5. What holiday the piece most represents.


Then I want to add this art to a large database and I need to categorize it so that others can find it.
Give me 10 keyword seach terms that I can use to categorize this art.
"""

import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    temperature=0,
    system='you are an art critic and also understand SEO keyword trends. i will provide you with an image and the information that i have for it. Your task is to analyze the provided art work and give me information about it in JSON format. Put the JSON in <metadata> tags. I want a title (loaded with SEO keywords), a description, a list of 30 SEO keywords, the two most used colors, the art style, the location represented, the holiday best represented.\n\nBe descriptive but not repetitive. DO NOT use the names of real people even if they are in my data to you. If you cannot decide on a holiday then just pick your best guess.\n\nexample output...\n\n<metadata>\n{\n  "title": "title here",\n  "description": "description here",\n  "keywords": ["keyword 1", "keyword 2"],\n  "colors": ["color 1", "color 2"]\'\n  "art_style": "art style here",\n  "location": "location here",\n  "holiday": "holiday here"\n}\n</metadata>',
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "A surreal landscape with floating islands and a giant; glowing moon | Modern Line Icon; Vector Line Art; Cute; Icon Design; Bold Outline; Solid Color; Pixel Perfect; Isolate; white background; Minimalistic; Bold Colors",
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": "<base64_encoded_image>",
                    },
                },
            ],
        }
    ],
)
print(message.content)