import json
import os
from typing import Generator

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from llama_cpp import Llama

load_dotenv()

# Model details
model_template = "mistralai/Mixtral-8x7B-Instruct-v0.1"
model_path = os.getenv("MIXTRAL_MODEL_PATH")
llm = Llama(
    model_path=model_path,
    n_gpu_layers=-1,
    n_ctx=4096 * 4,
    n_threads=4,
    chat_format="llama-2",
)

# API
app = FastAPI()

origins = [
    "http://localhost:8080",  # Adjust this to your Vue app's URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helper function to generate a response
def generate_response(message: str, history: list) -> Generator[str, None, None]:
    prompt = [
        {
            "role": "user",
            "content": f"Here is our chat history: {history}. Prompt: {message}",
        },
    ]

    response = llm.create_chat_completion(
        prompt,
        temperature=0.5,
        top_k=20,
        top_p=0.7,
        max_tokens=4096,
        stream=True,
        response_format={"type": "html"},
    )

    for idx, chunk in enumerate(response):
        if idx == 0:
            continue  # Skip the first chunk if it's not part of the actual response
        try:
            valid_chunk = chunk["choices"][0]["delta"]["content"]
            if valid_chunk is not None:
                yield valid_chunk
        except Exception as e:
            # Log or handle exceptions as necessary
            print(e)
            break


# API endpoint to generate a response
@app.post("/api/generate")
async def generate(request: Request):
    try:
        data = await request.json()
    except json.JSONDecodeError as e:
        error_message = f"Invalid JSON format: {str(e)}"
        return {"error": error_message}

    message = data.get("message")
    history = data.get(
        "history", []
    )  # Provide a default empty list for history if not provided

    if not message:
        return {"error": "The 'message' field is required."}

    response_generator = generate_response(message, history)
    return StreamingResponse(response_generator, media_type="text/plain")
