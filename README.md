# FastAPI Chat Completion API

This project is a FastAPI application that generates responses using the `llama_cpp` library and a specified language model. It includes CORS middleware to allow interactions with a frontend application, such as one built with Vue.js.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Files](#files)
- [Dependencies](#dependencies)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Quints497/web-api.git
   cd web-api
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Set up environment variables

Ensure you have a `.env` file in the project directory with the necessary environment variables:

- Add the path to your model in the `.env` file:
  - `MIXTRAL_MODEL_PATH`

### Running the Application

To start the FastAPI server, run the following command:

```bash
uvicorn main:app --reload
```

This will start the server with hot-reload enabled, making development easier.

## API Endpoints

### POST `/api/generate`

This endpoint generates a response based on the provided message and chat history.

- **Request**:
  - `message` (string): The user's message.
  - `history` (list): A list of previous messages in the chat (optional).

- **Response**:
  - A streaming response containing the generated response text.

#### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/api/generate" -H "Content-Type: application/json" -d '{"message": "Hello!", "history": []}'
```

## Project Structure

```raw
api/
├── src/
│   ├── __init__.py
│   └── main.py
├── venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Files

- **main.py**: The main FastAPI application code.
- **venv/**: Virtual environment (not included in the respository, needs to be created).
- **.env**: Environment variables file (not included in the repository, needs to be created).
- **.gitignore**: Files to be ignored from git commits.
- **README.md**: This readme file.
- **requirements.txt**: Python dependencies.

## Dependencies

- `fastapi`
- `uvicorn`
- `llama-cpp-python`
- `python-dotenv`
