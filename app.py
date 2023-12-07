import gradio as gr
import requests
from PIL import Image
import io
from gradio.themes.base import Base

def process_images(face_image, model_image, watermark = False, vignette = False):
    # Convertir las imágenes PIL a bytes
    model_img_bytes = io.BytesIO()
    model_image.save(model_img_bytes, format='PNG')
    face_img_bytes = io.BytesIO()
    face_image.save(face_img_bytes, format='PNG')

    # Configurar los datos para la solicitud HTTP
    url = 'http://storyfaceswapp-prod-env.eba-nmjv3puz.eu-west-3.elasticbeanstalk.com/swap_face'
    files = {
        'model': ('model.png', model_img_bytes.getvalue(), 'image/png'),
        'face': ('face.png', face_img_bytes.getvalue(), 'image/png'),
    }
    data = {
        'watermark': watermark,
        'vignette': vignette
    }

    response = requests.post(url, files=files, data=data)

    # Procesar la respuesta
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        raise ValueError("Error en la solicitud: Código de estado " + str(response.status_code))

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
