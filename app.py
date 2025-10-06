import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np


st.set_page_config(
    page_title="Brain Tumor Detector",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="auto",
)


@st.cache_resource
def load_keras_model():
    """Load the pre-trained Keras model from the .h5 file."""
    try:
       
        model = load_model('model1.h5')
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.error("Please ensure the 'model1.h5' file is in the correct directory.")
        return None

model = load_keras_model()


def preprocess_image(image):
    """Preprocesses the uploaded image to fit model's input requirements."""
    # Converting image to RGB format to handle different image modes (like grayscale)
    img = image.convert('RGB')
    # Resizing the image to the model's expected input size (128x128)
    img = img.resize((128, 128))
    # Converting image to numpy array
    img_array = np.array(img)
    # Expanding dimensions to create a batch of 1
    img_array = np.expand_dims(img_array, axis=0)
    # Normalizing the image data
    img_array = img_array / 255.0
    return img_array

# interface
st.title("🩺 Brain Tumor Detector")
st.markdown("Upload an MRI scan of a brain, and the model will predict whether a tumor is present.")

uploaded_file = st.file_uploader("Choose an MRI image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and model is not None:
    # Displaying the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded MRI Scan', use_column_width=True)
    st.write("")

    # Making prediction 
    if st.button('Analyze Image'):
        with st.spinner('Analyzing...'):
            # Preprocessing the image
            processed_image = preprocess_image(image)

            # Making a prediction
            prediction = model.predict(processed_image)
            score = prediction[0][0]

            # Displaying the result
            st.subheader("Analysis Result")
            if score > 0.5:
                st.error("**Tumor Detected**")
                st.write(f"Confidence Score: **{score*100:.2f}%**")
            else:
                st.success("**No Tumor Detected**")
                st.write(f"Confidence Score: **{(1-score)*100:.2f}%**")

st.markdown("""
---
*This app uses a Convolutional Neural Network (CNN) trained on a dataset of brain MRI scans to classify them as either containing a tumor or not.*
""")

st.markdown("""
---
*Created by Rishabh Aggarwal (<a href="https://github.com/vectorinfinity" target="_blank">GitHub</a>)*
""", unsafe_allow_html=True)


