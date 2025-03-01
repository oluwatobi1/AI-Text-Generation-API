# AI-Powered Text Generation API

## Objective
Backend service that allows users to generate and store AI-generated text using OpenAI's language models. Users should be able to authenticate, request AI-generated responses, and manage stored records.

## API Endpoints

- **POST /register**: Register a new user.
- **POST /login**: Authenticate and receive a JWT token.
- **POST /generate-text**: Send a prompt to OpenAI's API and store the generated response.
- **GET /generated-text/<id>**: Retrieve stored AI-generated text.
- **PUT /generated-text/<id>**: Update stored AI-generated text.
- **DELETE /generated-text/<id>**: Delete stored AI-generated text.


## Database Schema (PostgreSQL + SQLAlchemy)
- **Users**: Stores user information and authentication details.
- **GeneratedText**: Stores AI-generated text responses along with metadata.

## Third-Party API Integration

- **OpenAI API**: Used to generate text responses based on user prompts.
- Store responses in the database for later retrieval.

<!-- ## Testing

- **Unit Tests**: Test database models, authentication, and API endpoints.
- **Integration Tests**: Ensure end-to-end functionality works correctly.

## Containerization (Docker + Docker Compose)

- **Dockerfile**: Containerize the Flask application.
- **docker-compose.yml**: Set up PostgreSQL and the application.
- Ensure smooth deployment and scalability.

## Getting Started

1. Clone the repository.
2. Set up the environment variables for OpenAI API key, database URL, and JWT secret.
3. Build and run the Docker containers using Docker Compose.
4. Access the API endpoints to register, authenticate, generate text, and manage stored records.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. -->
