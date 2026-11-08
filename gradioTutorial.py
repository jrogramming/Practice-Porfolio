import gradio as gr


def greet(name, ToD, intensity): # names function and takes inputs in the order the input components are arranged in the Interface class
    greetTime = "morning" if ToD else "evening"
    return "Good " + greetTime + " " +name + "!" * int(intensity) + " I am " + "so "*int(intensity) + "SO excited to meet you."

textDemo = gr.Interface( 
    fn = greet, # the function to execute once inputs are in

    title = "Greeter", # interface title

    # interface descriptor
    description = """ 
### Welcome to Greeter!

A simple interactive greeting generator created to practice Gradio. Customize the greeting using the inputs below.

**How it works:**
- **Name:** Enter the name of the person you're greeting.
- **Morning?:** Check the box for a morning greeting. Otherwise, you'll get an evening greeting.
- **Excitement:** Adjust the slider to control the enthusiasm of your greeting!

---

*Built with Python and Gradio.*

""",

    inputs = [ "text", 
              gr.Checkbox(label = "Morning?", value = True), # morning is default
              gr.Slider(label = "Excitement", value = 1, minimum = 1, maximum = 5, step = 2) 
               ], # the components to take inputs in the interface
    # value is default

    outputs = [gr.Textbox(label = "Greeting", lines = 4)], # the component that displays the function's output
    # lines controls how many rows are displayed initially

    api_name="greeter" # determines the function endpoint name to be called, calling greeter basically triggers the greet function in this interface
)


textDemo.launch(share = False) # share is a public link

