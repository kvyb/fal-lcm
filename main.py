import fal
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_image(prompt, negative_prompt, image_url, strength, num_inference_steps):
    # Submit the request to the queue
    handler = fal.apps.submit(
        '110602490-lcm',
        arguments={
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'image_url': image_url,
            'strength': strength,
            'num_inference_steps': num_inference_steps,
        }
    )
    print(f"Request submitted. ID: {handler.request_id}")

    # Iterate through events until the request is completed
    for event in handler.iter_events(logs=False):
        if isinstance(event, fal.apps.InProgress):
            print('Request in progress')
            print(event.logs)
        elif isinstance(event, fal.apps.Queued):
            print(f"Request in queue at position: {event.position}")

    # Fetch the result
    result = handler.fetch_result()
    return result['images'][0]['url']

# Default values for the inputs
default_prompt = 'marty, man, sketch, pencil drawing, illustration, black and white, monochrome, 8k'
default_negative_prompt = 'photo, painting, realistic'
default_image_url = 'https://litter.catbox.moe/4lo9sp.png'
default_strength = 0.5
default_num_inference_steps = 10

iface = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(value=default_prompt, label="Prompt"),
        gr.Textbox(value=default_negative_prompt, label="Negative Prompt"),
        gr.Textbox(value=default_image_url, label="Image URL"),
        gr.Slider(minimum=0, maximum=1, step=0.1, value=default_strength, label="Strength"),
        gr.Slider(minimum=1, maximum=20, step=1, value=default_num_inference_steps, label="Number of Inference Steps")
    ],
    outputs="image",
    live=False
)

iface.launch(server_name="0.0.0.0", show_api=True)
