import re
import gradio as gr

def data_preprocessing(text):
    return re.sub(r'[^a-zA-Z0-9]', ' ', text)

gradio_ui = gr.Interface(
    fn = data_preprocessing,
    title  = "Data Preprocessing and Modeling",
    description = "Aplikasi Web Data Processing dan Modeling",
    inputs = gr.inputs.Textbox(lines=10, label="Paste some text here"),
    outputs= [
        gr.outputs.Textbox(label='Results'),
    ],
)

gradio_ui.launch()