from pydantic import BaseModel, Field, SecretStr


class ModelConfiguration(BaseModel):
    model_name: str = Field(..., description="Name of the chat model")
    embedding_model_name: str = Field(..., description="Name of the embedding model")
    api_key_model: SecretStr = Field(..., description="API key for the chat model")