from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize FastAPI app
app = FastAPI()

# Load CodeLlama Model
MODEL_PATH = "./saved_codellema"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# Define request model
class CodeRequest(BaseModel):
    code_snippet: str

def detect_and_fix_bug(code_snippet):
    """
    Detects and fixes bugs in a given code snippet using CodeLlama.
    Extracts only the fixed code and key analysis.
    """
    prompt = f"""
### Buggy Code:
{code_snippet}

### Task:
1. Identify the exact line where the error occurs.
2. Explain what the issue is.
3. Provide a corrected version of the code.

### Expected Output:
- Line of error: (Mention the exact line)
- Explanation: (What is wrong?)
- Fixed Code:
"""

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

    # Generate output
    try:
        output = model.generate(
            **inputs,
            max_length=512,
            temperature=0.2,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model generation error: {str(e)}")

    # Decode output
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract only the fixed code
    response_lines = response.split("\n")
    extracted_fix = []
    extracting = False

    for line in response_lines:
        if "Fixed Code:" in line:
            extracting = True
        if extracting:
            extracted_fix.append(line)

    fixed_code_output = "\n".join(extracted_fix) if extracted_fix else response

    return fixed_code_output

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    """API endpoint to analyze and fix code."""
    if not request.code_snippet.strip():
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty.")

    result = detect_and_fix_bug(request.code_snippet)
    return {"fixed_code": result}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize FastAPI app
app = FastAPI()

# Load CodeLlama Model
MODEL_PATH = "./saved_codellema"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# Define request model
class CodeRequest(BaseModel):
    code_snippet: str

def detect_and_fix_bug(code_snippet):
    """
    Detects and fixes bugs in a given code snippet using CodeLlama.
    Extracts only the fixed code and key analysis.
    """
    prompt = f"""
### Buggy Code:
{code_snippet}

### Task:
1. Identify the exact line where the error occurs.
2. Explain what the issue is.
3. Provide a corrected version of the code.

### Expected Output:
- Line of error: (Mention the exact line)
- Explanation: (What is wrong?)
- Fixed Code:
"""

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

    # Generate output
    try:
        output = model.generate(
            **inputs,
            max_length=512,
            temperature=0.2,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model generation error: {str(e)}")

    # Decode output
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract only the fixed code
    response_lines = response.split("\n")
    extracted_fix = []
    extracting = False

    for line in response_lines:
        if "Fixed Code:" in line:
            extracting = True
        if extracting:
            extracted_fix.append(line)

    fixed_code_output = "\n".join(extracted_fix) if extracted_fix else response

    return fixed_code_output

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    """API endpoint to analyze and fix code."""
    if not request.code_snippet.strip():
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty.")

    result = detect_and_fix_bug(request.code_snippet)
    return {"fixed_code": result}
