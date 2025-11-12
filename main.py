import os
import json

import streamlit as st
from  PIL import Image
from streamlit_option_menu import option_menu

from gemini_utility import (load_generative_model,
                            load_generative_image_caption,
                            embeddings_model_response,
                            gemini_pro_response)

working_dir = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_dir}/config.json"
config_data = json.load(open("config.json"))

st.set_page_config(
    page_title = "Generative Ai",
    page_icon=":book",
    layout="centered",
)

with st.sidebar:
    selected = option_menu(
        menu_title="Gemini AI",
        options=["Chatbot",
                 "Image captioning",
                 "Embedd Text",
                 "Ask me"],
        menu_icon='robot', icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
        default_index=0
    )

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if selected == "Chatbot":

    model = load_generative_model()

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("Chatbot")

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Ask somthing.....")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_responce = st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
             st.markdown(gemini_responce.text)


if selected == "Image captioning":
    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_img = image.resize((800, 500))
            st.image(resized_img)

        default_prompt = "write a short caption for this image"  # change this prompt as per your requirement

        # get the caption of the image from the gemini-pro-vision LLM
        caption = load_generative_image_caption(default_prompt, image)

        with col2:
            st.info(caption)

if selected == "Embed text":

    st.title("🔡 Embed Text")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Enter the text to get embeddings")

    if st.button("Get Response"):
        response = embeddings_model_response(user_prompt)
        st.markdown(response)


# text embedding model
if selected == "Ask me anything":

    st.title("❓ Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)