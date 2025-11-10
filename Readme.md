# AI Fashion Stylist - Backend API

This repository contains the backend API for the AI Fashion Stylist, a personalized wardrobe management and outfit suggestion engine. The API is built with Python using the FastAPI framework and is designed to be the core engine for a mobile (SwiftUI) or web application.

## Core Features

*   **User Authentication:** Secure user registration and login using JWT (JSON Web Tokens) for protected endpoints.
*   **Personalized Wardrobe Management:** Full CRUD (Create, Read, Update, Delete) functionality for users to manage their private digital wardrobes.
*   **AI-Powered Styling:** An intelligent endpoint that uses a vector database (ChromaDB) for semantic retrieval and a Large Language Model (OpenAI GPT series) for generating reasoned, context-aware outfit suggestions.

## Tech Stack

*   **Framework:** FastAPI
*   **Database:** SQLAlchemy with SQLite
*   **Data Validation:** Pydantic
*   **Authentication:** Passlib (for hashing), Python-JOSE (for JWT)
*   **AI Pipeline:** ChromaDB (Vector Database), OpenAI (LLM)
*   **Server:** Uvicorn

---

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

*   Python 3.9+
*   Git

### 1. Clone the Repository

```bash
git clone https://github.com/mythreyi1905/ai-stylist-backend.git
cd ai-stylist-backend
```

### 2. Create the `.env` File

This project requires an `.env` file in the root directory to store your secret keys. Create the file and add your keys.

```bash
# .env file

# Generate your own secret key. You can use: openssl rand -hex 32
SECRET_KEY="your_super_secret_32_character_hex_key_here"

# Add your OpenAI API key
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 3. Set Up the Virtual Environment

Create and activate a Python virtual environment.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Or activate it (Windows)
# .\venv\Scripts\activate
```

### 4. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Run the Application

The application server uses Uvicorn. The database will be created automatically on the first run.

```bash
uvicorn app.main:app --reload
```

The API will now be running at `http://127.0.0.1:8000`.

---

## API Usage & Testing

The API is self-documenting. Once the server is running, you can access the interactive Swagger UI documentation at:

**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

This interface allows you to test every endpoint directly from your browser.

For a complete guide with copy-pasteable cURL commands for every endpoint, please see the **[API Testing Guide](./API_TESTING_GUIDE.md)**.