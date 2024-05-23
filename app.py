import gradio as gr
import requests
from PIL import Image
import io
from gradio.themes.base import Base
import os
from dotenv import load_dotenv

load_dotenv()

def process_images(face_image, model_image, watermark = False, vignette = False, quality = 100):
    # Convertir las imágenes PIL a bytes
    model_img_bytes = io.BytesIO()
    model_image.save(model_img_bytes, format='PNG')
    face_img_bytes = io.BytesIO()
    face_image.save(face_img_bytes, format='PNG')

    # Configurar los datos para la solicitud HTTP
    url = os.getenv('URL')
 
    files = [
    ('images', ('face.png', face_img_bytes.getvalue(), 'image/jpeg')),
    ('images', ('model.png', model_img_bytes.getvalue(), 'image/png'))
    ]      
    
    data = {
        'watermark': 0,
        'quality': quality
    }

    response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        # Log the Content-Type to ensure it's an image
        #print("Content-Type:", response.headers.get('Content-Type'))
        #print(response.content)
        
        # Attempt to open the response content as an image
        try:
            return Image.open(io.BytesIO(response.content))
        except Exception as e:
            print(f"Error opening image: {e}")
            return None  # Return None or handle the error as needed
    else:
        raise ValueError(f"Error in the request: Status Code {response.status_code}")


# Crear la interfaz de Gradio

iface = gr.Interface(
   fn=process_images,
   inputs=[
    gr.Image(type="pil", label="Face Image"),
    gr.Image(type="pil", label="Model Image") 
    ],
   outputs=gr.Image(type="pil", label="Result Image"),
   title="StoryFace Internal Tool",
   description="<h2 style='text-align: center; font-size: 24px;'>Take a photo or upload a clear photo of your face, upload a photo of the model you want to see yourself in, and press the submit button..</h2>",
   allow_flagging="never"
)

# Ejecutar la aplicación
iface.launch()
