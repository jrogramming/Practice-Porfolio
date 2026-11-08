import gradio as gr


def greet(name,intensity): # names function and takes two inputs
    return "Hello " + name + "!" * int(intensity) + " I am " + "so "*int(intensity) + "SO excited to meet you."

demo = gr.Interface( 
    fn = greet, # the function to execute once inputs are in

    inputs = [ "text", gr.Slider(label = "Excitement", value = 4, minimum = 1, maximum = 9, step = 2) ], # the components to take inputs in the interface
    # value is default

    outputs = [gr.Textbox(label = "Greeting", lines = 4)], # the component that displays the function's output
    # lines controls how many rows are displayed initially

    api_name="greeter" # determines the function endpoint name to be called, calling greeter basically triggers the greet function in this interface
)

demo.launch(share = False) # share is a public link

