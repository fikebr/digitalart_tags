import utlis.jbf.claude as api
import utlis.jbf.file as file
import os
import json
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

api_key = os.getenv("ANTHROPIC_KEY")


img_file = "E:/Programs/Mmed/_Image/Fooocus_win64_2-0-50/Fooocus/outputs/2024-03-07/2024-03-07_03-35-17_2444.png"


system_msg_file = os.path.abspath(os.path.dirname(__file__))
system_msg_file = os.path.join(system_msg_file, "system_msg.txt")


json_file = os.path.join(
    os.path.dirname(img_file), os.path.splitext(os.path.basename(img_file))[0] + ".json"
)

with open(json_file, "r") as f:
    # Load the JSON data from the file
    data = json.load(f)

prompt = data['metadata']['fooocus']['Prompt']
data['description'] = {}

data["description"]['api'] = api.analyze_image(api_key, img_file, system_msg_file, prompt)
file.write_file(json_file, json.dumps(data))
pass