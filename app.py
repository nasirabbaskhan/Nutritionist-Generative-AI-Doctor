import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai # type: ignore
from PIL import Image
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def generate_gemini_response( prompt, image):
   
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, image[0]])
    return response.text

# def input_image_setup(uploaded_file):
#     if uploaded_file is not None:
#         # Read the file into bytes
#         bytes_data = uploaded_file.getvalue()
        
#         # Create a dictionary for the image blob
#         image_blob = {
#             "mime_type": uploaded_file.type,
#             "data": bytes_data
#         }
#         return image_blob  # Return the image blob as a single dict
#     else:
#         raise FileNotFoundError("No File uploaded")
def input_image_setup(upload_file):
    if upload_file is not None:
        # read the file into bytes
        bytes_data= upload_file.getvalue()
        
        image_parts = [
            {
                "mime_type":upload_file.type,
                "data":bytes_data
            }
            
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


 
# streamlit app
st.set_page_config(page_title="Calories advisor App")
st.title("Gemini Health App")

uploaded_file = st.file_uploader("choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image , caption="Uploaded Image.", use_column_width=True)
    
    
prompt = """
        Your role is analyze the image and provide a nutritional breakdown.
        You are an expert in  nutritionist who analyzin any image, where you need to see the food items from the image
        and calculate the total calories, and also provide the details of every food items with 
        calories intake in below formate 

        1. Item 1 - no of calories 
        2. Item 2 - no of calories 
        -----
        -----

        Finally you can also mention wheather the food is healthy or not and also mention the
        percentage split of the ratio of carbohydrates,fates,fibers,sugar and other important
        things required in our diet
        
        You have need to provid the response based on the image with some general assumptions, 
        so there is not need to knowing the specific ingredients and quantities used.
 
    """
    
    
submit = st.button("Tell me abut the total calories")

if submit:
    image_data = input_image_setup(uploaded_file)
    if image_data:
        response = generate_gemini_response(prompt, image_data)
        st.subheader("The Response is:")
        st.write(response)
        
    
    
    
