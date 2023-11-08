import gradio as gr
import time

def greet_1(name): 
    greeting = f"{name} + Good Morning"
    return greeting
   
def greet_2(name, is_morning, temperature,progress=gr.Progress()):
 
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    time.sleep(2.0)
    list_array = [20, 40,60,80,100]
    for iterat in progress.tqdm(list_array):
        time.sleep(0.2)
    # progress(1.0)
    return greeting, round(celsius, 2)

# demo = gr.Interface(
#     fn=greet_2,
#     inputs=["text", "checkbox", gr.Slider(0, 100)],
#     outputs=[gr.Text(label="Greetings"), gr.Number(label='Celsius')],
# )

with gr.Blocks(css=".gradio-container {background-color: blue}") as demo:

    gr.HTML("The app for testing purpose")
    with gr.Tab("Greet"):
        input = [gr.Text(label="Name"), gr.Checkbox(label="is_morning"), gr.Slider(0, 100,label="Temperature")]
        output = [gr.Text(label="Greeting"), gr.Number(label='Celsius')]
        greet_btn = gr.Button("Greeting to Submit")
        greet_btn.click(fn=greet_2, inputs=input, outputs=output, api_name="greet",concurrency_limit=1)
    with gr.Tab("No Reply"):
        input = [gr.Text(label="Name")]
        output = [gr.Text(label="Greeting")]
        greet_btn = gr.Button("Submit")
        greet_btn.click(fn=greet_1, inputs=input, outputs=output, api_name="greet",concurrency_limit=2)
        # gr.Info("Tab Pressed")

    with gr.Accordion("Open for More Options!"):
        gr.Markdown("Look at me...")
        # with gr.Tab("More Tabs"):
        #     gr.Interface.load("spaces/eugenesiow/remove-bg", inputs="webcam",title="Remove your webcam background!")
        #     input = [gr.Text(label="Name")]
        #     output = [gr.Text(label="Greeting")]
        #     greet_btn = gr.Button("Submit")
        #     greet_btn.click(fn=greet_1, inputs=input, outputs=output, api_name="greet")
            

if __name__ == "__main__":
    demo.queue()
    demo.launch(show_api=False,share=False,debug=False)


### run with
### gradio gradio_app_dem_1.py