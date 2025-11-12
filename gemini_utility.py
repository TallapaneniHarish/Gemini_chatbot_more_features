import os
import json

import google.generativeai as gen_ai


working_dir = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_dir}/config.json"
config_data = json.load(open(config_file_path))


GOOGLE_API_KEY = config_data["GEMINI_API_KEY"]
gen_ai.configure(api_key=GOOGLE_API_KEY)

def load_generative_model():
    generative_model = gen_ai.GenerativeModel("gemini-2.5-flash")
    return generative_model


def load_generative_image_caption(prompt, image):
    generative_model_image = gen_ai.GenerativeModel("gemini-2.5-flash")
    responce =generative_model_image.generate_content([prompt, image])
    result = responce.text
    return result

def embeddings_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = gen_ai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type="retrieval_document")
    embedding_list = embedding["embedding"]
    return embedding_list


# get response from Gemini-Pro model - text to text
def gemini_pro_response(user_prompt):
    gemini_pro_model = gen_ai.GenerativeModel("gemini2.5-flash")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result