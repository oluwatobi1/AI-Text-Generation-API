# AI-Powered Text Generation API

Allows users to generate and store AI-generated text using large language models. 

Application includes authentication, requesting AI-generated responses, and managing stored records.

## API Endpoints

- **POST /register**: Register a new user.
- **POST /login**: Authenticate and receive a JWT token.
- **POST /generate-text**: Send a prompt to OpenAI's API and store the generated response.
- **GET /generated-text/<id>**: Retrieve stored AI-generated text.
- **PUT /generated-text/<id>**: Update stored AI-generated text.
- **DELETE /generated-text/<id>**: Delete stored AI-generated text.

## Authentication
- **JWT**: Uses JWT tokens for authentication.

## Third-Party API Integration
- **OpenAI API**: Used to generate text responses based on user prompts.
- **Large Language Models (LLMs)**: Integration with modern LLMs (ie those in the Chat Model category) such as OpenAI and Groq requires API keys with a format specific to each LLM. 
To set them up, 
    1. Add the LLM API key and value to the environment variables. (e.g., `OPENAI_API_KEY=myopenapikey`, `GROQ_API_KEY=mygroqapikey`)
    2. The model name (e.g., `gpt-3-turbo)`
    3. The model provider.

    For example, for the OpenAI (e.g., `gpt-3-turbo`)  model, you would need to add the following to your `.env` file:
    ```env
    OPENAI_API_KEY=myopenapikey
    AI_MODEL_NAME=gpt-4o-mini
    AI_MODEL_PROVIDER=openai
    ```

- **Fallback Model**: If no model is specified, the system will fall back to a small/lightweight LLM. This fallback model runs locally and is slower, taking more time to generate responses.


## Database Configuration
- **PostgreSQL**: Used as the primary database when running with Docker Compose.
- **SQLite**: Used as a fallback database when Docker Compose is not available.

## Testing
The tests  are located in the `ai_text_generation/tests/`.

### Test Files and Types

- **Unit Tests**: Test database models, authentication, and API endpoints.
    - **ai_text_generation/tests/unit/test_auth.py**: Contains unit tests for authentication.
    - **ai_text_generation/tests/unit/test_model.py**: Contains unit tests for database.
    - **ai_text_generation/tests/unit/test_textgen.py**: Contains unit tests for the text generation functionality.

- **Integration Tests**: Ensure end-to-end functionality works correctly.
    - **ai_text_generation/tests/e2e/test_e2e.py**: Contains end-to-end tests for the application.

See below for instructions on running the tests.


## Containerization (Docker + Docker Compose)

- **Dockerfile**: Containerize the Flask application.
- **docker-compose.yml**: Set up PostgreSQL and the application.
    - **PostgreSQL Container**: Runs the PostgreSQL database.
    - **App Container**: Runs the Flask application, connecting to PostgreSQL when available, otherwise falling back to SQLite.



## Getting Started with Docker Compose

1. **Clone the repository**:
    ```sh
    git clone git@github.com:oluwatobi1/AI-Text-Generation-API.git
    cd insait_savannah/ai_text_generation
    ```

2. **Set up environment variables**:
    Create a `.env` file in the app directory (`insait_savannah/ai_text_generation`) and add the following variables:
    ```env
    OPENAI_API_KEY=myopenapikey
    AI_MODEL_NAME=gpt-4o-mini
    AI_MODEL_PROVIDER=openai
    DATABASE_URL=postgresql://user:password@db:5432/mydatabase
    ```
    or alternatively passed in docker-compose.yml environment section
   
    

3. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

4. **Access the API**:
    The API will be available at `http://localhost:5000`. You can now register, authenticate, generate text, and manage stored records using the provided endpoints.
5. Access Swagger documentation at `http://localhost:5000/swagger-ui` to interact with the API.
and redoc documentation at `http://localhost:5000/redoc` to interact with the API.


6. **To Run tests**:
    ```sh
    docker compose run --rm test

    ```

## Deployment
App is deployed on Render. Note that applications experience cold starts on Render, so the first request may take a few seconds to respond.


- Live API URL: https://ai-text-generation-api.onrender.com/
- Live Swagger UI: https://ai-text-generation-api.onrender.com/swagger-ui

## API Documentation
 - Swagger UI: `http://localhost:5000/swagger-ui`
Alternatively, https://ai-text-generation-api.onrender.com/swagger-ui
 - ReDoc: `http://localhost:5000/redoc`