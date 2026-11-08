import gradio as gr


def greet(name,intensity): # names function and takes two inputs
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface( 
    fn = greet, # the function to execute once inputs are in
    inputs = ["text", "slider"], # the components to take inputs in the interface
    outputs = ["text"], # the component that displays the function's output
    api_name="greeter" # determines the function endpoint name to be called, calling greeter basically triggers the greet function in this interface
)

demo.launch(share = True) # share is a public link

