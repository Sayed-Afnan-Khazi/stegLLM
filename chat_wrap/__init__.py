import requests

class chat_wrap:
    def __init__(self,API_URL: str,API_TOKEN: str) -> None:
        '''Creates a chat_wrap instance using a Huggingface API_URL, and a Huggingface API_TOKEN.'''
        self.API_URL = API_URL
        self.API_TOKEN = API_TOKEN
        self.headers = {"Authorization": f"Bearer {self.API_TOKEN}"}
        if not self.API_URL or not self.API_TOKEN:
            print("WARNING: API_URL or API_TOKEN not set.")

    def _query(self,payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()

    def get_response(self,prompt):
        try:
            data = self._query({
                'inputs': f'<bos><start_of_turn>user\nBelow is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\\n\\n### Instruction: You are a helpful assistant that provides answers to user questions\\n\\n\\n### Input:\\n{prompt}\\n\\n### Response:\\n<end_of_turn>\n<start_of_turn>model\n',
                'parameters': {"return_full_text": "false", "max_new_tokens": 100}
            })
            if type(data) == type([]):
                return data[0]['generated_text']
            else:
                if "Model" in data["error"] and "is currently loading" in data["error"]:
                    return "The model is currently loading. Please try again in a few seconds."
                else:
                    raise RuntimeError
        except:
            return ConnectionError('An Error Occurred. Please try again.')

# while True:
#         prompt = input("User > ")
#         data = query({
#             'inputs': f'<bos><start_of_turn>user\nBelow is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\\n\\n### Instruction: You are a helpful assistant that provides answers to user questions\\n\\n\\n### Input:\\n{prompt}\\n\\n### Response:\\n<end_of_turn>\n<start_of_turn>model\n',
#             'parameters': {"return_full_text": "false", "max_new_tokens": 100}
#         })
#         # if data[0] and data[0].error == 'Model oofnan/stegBot2 is currently loading':
#         #     print("Helpful ChatBot > ","LOADING MODEL...Please try again in a few seconds.")
#         # else:
#         print("Helpful ChatBot > ",data[0]['generated_text'])