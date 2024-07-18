import os
import requests
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

class GPT:
    def __init__(self) -> None:
        self.url = os.getenv('MODEL_URL')
        self.headers = {
            "Authorization": f"Bearer {os.getenv(
                'HUGGINGFACE_INFERENCE_TOKEN'
            )}",
            "Content-Type": "application/json"
        }
        self.payload = {
            "inputs": "",
            "parameters": {
                "return_full_text": False,
                "use_cache": True,
                "max_new_tokens": 25
            }
        }
        print(f"MODEL_URL: {self.url}")
        print(f"HUGGINGFACE_INFERENCE_TOKEN: {os.getenv(
            'HUGGINGFACE_INFERENCE_TOKEN'
        )}")

    def query(self, input: str) -> list:
        self.payload["inputs"] = f"Human: {input} Bot:"
        data = json.dumps(self.payload)
        response = requests.post(self.url, headers=self.headers, data=data)
        
        if response.status_code != 200:
            raise Exception(f"""Request failed with status code\
            {response.status_code}: {response.content.decode('utf-8')}""")

        try:
            data = json.loads(response.content.decode("utf-8"))
            text = data[0]['generated_text']
            print(text)
            res = str(text.split("Human:")[0]).strip("\n").strip()
            return res
        except json.JSONDecodeError as e:
            print("Failed to decode JSON response")
            print("Response content:", response.content)
            raise e

if __name__ == "__main__":
    gpt = GPT()
    try:
        gpt.query("Will artificial intelligence help humanity conquer the universe?")
    except Exception as e:
        print(e)
