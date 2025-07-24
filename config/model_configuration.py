from pydantic import BaseModel, Field, SecretStr


class ModelConfiguration(BaseModel):
    chat_model_name: str = Field(..., description="Name of the chat model")
    embedding_model_name: str = Field(..., description="Name of the embedding model")
    api_key: SecretStr = Field(..., description="API key for the chat model")