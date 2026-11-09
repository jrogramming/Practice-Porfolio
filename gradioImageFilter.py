import gradio as gr
import numpy as np

def purplizer(input_img):
    purplizer_filter = np.array([ # RGB shift, it's like the multiplier applied to the value of 
    [1.0, 0.15, 0.15], # red
    [0.15, 0.85, 0.15], # green
    [0.25, 0.15, 1.0] # blue
    ])

# Think of it like taking a single pixel's RGB to make a vector then transforming it with the purplizer_filter to get a new RGB value for that pixel, every pixel in the image
# Say you have a pixel with a RGB of [100 150 200], you (matrix) multiply the vector with the cols and sum the three numbers (dot product) to get the new R/G/B value

    purplizer_img = input_img.dot(purplizer_filter.T) # The .T is transpose to do dot product
    purplizer_img /= purplizer_img.max()
    return purplizer_img

demo = gr.Interface(
    fn = purplizer,

    title = "Purplizer Filterer",

    inputs = gr.Image(label = "Base Image"),

    outputs = gr.Image(label = "purplizer Image"),
    
    api_name = "purplizerer"                 
                     
)

demo.launch(share = False)