# import requests
# import os
# from dotenv import load_dotenv
# load_dotenv()

# API_URL = "https://router.huggingface.co/novita/v3/openai/chat/completions"
# headers = {
#     "Authorization": f"Bearer {os.environ.get('huggingfacehub_api_token')}",
# }

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# response = query({
#     "messages": [
#         {
#             "role": "user",
#             "content": "What is the capital of France?"
#         }
#     ],
#     "model": "deepseek/deepseek-prover-v2-671b"
# })

# print(response["choices"][0]["message"])


# from langchain_huggingface import ChatHuggingFace
# from langchain_huggingface.llms import HuggingFaceEndpoint  # Correct import
# import os

# # 1. Set your Hugging Face token (replace with your actual token)
# HUGGINGFACEHUB_API_TOKEN = "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" 
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

# # 2. Initialize the LLM with a valid model
# llm = HuggingFaceEndpoint(
#     repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",  # Public model
#     task="text-generation",
#     temperature=0.7,
#     max_new_tokens=512,
# )

# # 3. Create the chat model
# chat_model = ChatHuggingFace(llm=llm)

# # 4. Invoke the model
# response = chat_model.invoke("Who is the prime minister of India?")
# print(response.content)



# from langchain_huggingface import HuggingFaceEndpoint
# from dotenv import load_dotenv
# import os

# load_dotenv()

# llm = HuggingFaceEndpoint(
#     repo_id="HuggingFaceH4/zephyr-7b-beta",
#     task="text-generation"
# )

# response = llm.invoke("Who is the prime minister of India?")
# print(response)



from langchain_huggingface import ChatHuggingFace
from langchain_huggingface.llms import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

# 1. Load environment variables from .env file
load_dotenv()

# 2. Verify the token is loaded (optional debug step)

"""create an .env file with the following content:
HUGGINGFACEHUB_API_TOKEN = "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" """
HUGGINGFACEHUB_API_TOKEN = os.environ.get('HUGGINGFACEHUB_API_TOKEN')
print(f"Token loaded: {'****' + HUGGINGFACEHUB_API_TOKEN[-4:] if HUGGINGFACEHUB_API_TOKEN else 'NOT FOUND'}")

# 3. Initialize the LLM
try:
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        task="text-generation",
        temperature=0.7,
        max_new_tokens=512,
    )
    
    chat_model = ChatHuggingFace(llm=llm)
    response = chat_model.invoke("Who is the prime minister of India?")
    print(response.content)
    
except Exception as e:
    print(f"Error: {str(e)}")
    if "401" in str(e):
        print("Authentication failed - please check your Hugging Face token")
    elif "404" in str(e):
        print("Model not found - check the repo_id")

