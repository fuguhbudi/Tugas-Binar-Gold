import gradio as gr
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is the home page"

@app.route("/new-page")
def new_page():
    button = gr.inputs.Button(label="Go to Home Page")
    interface = gr.Interface(button, [gr.outputs.HTML()], title="New Page", action="/")
    return interface.launch(share=False)

if __name__ == "__main__":
    app.run()
