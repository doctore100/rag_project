# RAG Project

A Retrieval-Augmented Generation (RAG) system that processes PDF documents, creates vector embeddings, and enables semantic search through a PostgreSQL database with pgvector extension.

## Project Overview

This project implements a RAG architecture using LangChain and OpenAI embeddings to:

1. Load and process PDF documents
2. Split documents into manageable chunks
3. Generate vector embeddings for each chunk
4. Store embeddings in a PostgreSQL database with pgvector extension
5. Perform semantic similarity searches to answer questions about the document content

The system uses a layered software architecture with clear separation of concerns between configuration, infrastructure, and presentation layers.

## Features

- PDF document processing with PyPDFLoader
- Text chunking with RecursiveCharacterTextSplitter
- Vector embeddings generation with OpenAI
- Secure remote database access via SSH tunneling
- PostgreSQL with pgvector extension for vector similarity search
- Configurable settings via environment variables

## Installation

### Prerequisites

- Python 3.13 or higher
- PostgreSQL database with pgvector extension
- SSH access to the database server (if remote)
- OpenAI API key

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-project
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` or `.env.development` file with your configuration:
   ```
   # General Settings
   APP_NAME="RAG Project"
   VERSION="0.1.0"
   ENVIRONMENT="development"
   DEBUG=true

   # Model Configuration
   MODEL__NAME="gpt-3.5-turbo"
   MODEL__EMBEDDING_NAME="text-embedding-ada-002"
   MODEL__API_KEY="your-openai-api-key"

   # Database Settings
   DATABASE__DB_USER="your-db-username"
   DATABASE__DB_PASSWORD="your-db-password"
   DATABASE__DB_HOST="localhost"
   DATABASE__DB_NAME="postgres"
   DATABASE__DB_PORT=5432
   DATABASE__COLLECTION_NAME="document_embeddings"
   DATABASE__COLLECTION_BB_NAME="vector_db"

   # SSH Connection Settings
   SSH_CONNECTION__HOST_NAME="your-ssh-host"
   SSH_CONNECTION__PORT=22
   SSH_CONNECTION__USERNAME="your-ssh-username"
   SSH_CONNECTION__LOCAL_BIND_PORT=5433
   ```

## Usage

### Basic Usage

```python
from main import main

# Run the main function to process the PDF and perform a similarity search
main()
```

### Custom Document Processing

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import create_settings
from infrastructure import DatabaseManager, SSHConnectionManager

settings = create_settings()

# Load and process a custom document
file_path_doc = "your_document.pdf"
loader = PyPDFLoader(file_path_doc)
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
chunks = text_splitter.split_documents(documents)

# Create embeddings
embeddings = OpenAIEmbeddings(model=settings.model.embedding_name, api_key=settings.model.api_key)

# Initialize database manager
manage_db = DatabaseManager(embeddings)

# Set up SSH tunnel
tunnel = SSHConnectionManager()
try:
    tunnel_generator = tunnel.start_ssh_tunnel()
    tunnel = next(tunnel_generator)
    if tunnel.is_active:
        # Initialize vector store
        vector_store = manage_db.initialize_vector_store()
        if vector_store:
            # Add documents to vector store
            vector_store.add_documents(documents=chunks)
            
            # Perform similarity search
            results = vector_store.similarity_search("Your question here?")
            print(results[0])
finally:
    # Clean up the tunnel
    if tunnel and hasattr(tunnel, 'is_active') and tunnel.is_active:
        tunnel.stop()
```

## Project Structure

```
rag_project/
├── config/                  # Configuration settings
│   ├── __init__.py          # Configuration initialization
│   ├── database.py          # Database settings
│   ├── model_configuration.py # LLM model settings
│   ├── settings.py          # General application settings
│   └── ssh_connection.py    # SSH connection settings
├── infrastructure/          # Infrastructure layer
│   ├── __init__.py          # Infrastructure initialization
│   ├── database/            # Database operations
│   │   └── __init__.py      # DatabaseManager implementation
│   └── ssh_connection/      # SSH connection handling
│       └── __init__.py      # SSHConnectionManager implementation
├── presentation/            # Presentation layer (UI/API)
│   └── __init__.py          # Presentation initialization
├── main.py                  # Main application entry point
├── nke_10k_2023.pdf         # Sample PDF document (Nike 10-K report)
├── poetry.lock              # Poetry lock file
├── poetry.toml              # Poetry configuration
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # Project documentation
```

## Configuration

The project uses Pydantic settings for configuration management, with support for environment variables and `.env` files. The main configuration components are:

### General Settings
- `app_name`: Name of the application
- `version`: Application version
- `environment`: Deployment environment (development, testing, production)
- `debug`: Debug mode flag

### Model Configuration
- `name`: Name of the chat model
- `embedding_name`: Name of the embedding model
- `api_key`: API key for the model service

### Database Settings
- `db_user`: PostgreSQL username
- `db_password`: PostgreSQL password
- `db_host`: Database host
- `db_name`: Database name
- `db_port`: Database port
- `collection_name`: Name for the vector collection
- `collection_bb_name`: Name of the database for storing vector embeddings

### SSH Connection Settings
- `host_name`: SSH server hostname
- `port`: SSH server port
- `username`: SSH username
- `local_bind_port`: Local port for SSH forwarding

## Dependencies

- `langchain-core`: Core LangChain functionality
- `langchain-community`: Community components for LangChain
- `langchain-openai`: OpenAI integration for LangChain
- `langchain-postgres`: PostgreSQL integration for LangChain
- `pydantic-settings`: Settings management
- `sshtunnel`: SSH tunneling
- `psycopg`: PostgreSQL database adapter
- `pypdf`: PDF processing

## Development

### Adding New Documents

To add new documents for processing:

1. Place the PDF file in the project root or a designated documents folder
2. Update the `file_path_doc` variable in `main.py` to point to your document
3. Run the application

### Customizing Vector Storage

To customize the vector storage:

1. Modify the `DatabaseSettings` in `config/database.py`
2. Update the collection name and database settings in your `.env` file
3. If needed, modify the `DatabaseManager` methods in `infrastructure/database/__init__.py`

## License

[Specify your license here]

## Contributors

- David (dg071018@gmail.com)