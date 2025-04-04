import torch
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load CodeLlama Model
MODEL_NAME = "codellama/CodeLlama-7b-hf"  # You can use your local path here as well.

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Use CUDA if available; otherwise, fallback to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model on available device
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype=torch.float32, device_map=device
)

def detect_and_fix_bug(code_snippet):
    """
    Detects and fixes bugs in a given code snippet using CodeLlama.
    Also identifies the exact line of error.
    """
    prompt = f"""
### Buggy Code:
{code_snippet}

### Task:
1. Identify if there is an error in the code.
2. Highlight the exact line where the error occurs.
3. Provide a corrected version of the code.

### Analysis:
"""
    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generate output with proper settings
    output = model.generate(
        **inputs,
        max_length=300,  # Reduced max length to speed up
        temperature=0.2,
        do_sample=False,  # Disable sampling to improve speed
        pad_token_id=tokenizer.eos_token_id  # Suppress warning
    )

    # Decode output
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return response

# Gradio Interface
def analyze_code(code):
    return detect_and_fix_bug(code)

# Create a Gradio interface with a text input and text output
interface = gr.Interface(
    fn=analyze_code,
    inputs=gr.Textbox(label="Enter your Python code here", placeholder="Enter buggy Python code", lines=10),
    outputs=gr.Textbox(label="Fixed Code & Analysis"),
    title="Code Bug Detector & Fixer",
    description="Enter your Python code to detect bugs and get the fixed version."
)

# Launch the interface
if __name__ == "__main__":
    interface.launch(share=False)  # Set `share=True` if you want a public link
