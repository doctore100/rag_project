from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from database import DatabaseSettings
from model_configuration import ModelConfiguration
from ssh_connection import SSHConnection


class Settings(BaseSettings):
    # General Settings
    app_name: str = Field(default="Mi Proyecto", description="Nombre de la aplicación")
    version: str = Field(default="0.0.1", description="Versión")
    environment: Literal["development", "testing", "production"] = Field(
        default="development"
    )
    debug: bool = Field(default=False)

    # Module-specific configurations
    model: ModelConfiguration
    database: DatabaseSettings
    ssh_connection: SSHConnection

    # Pydantic Settings Model Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False
    )

    @field_validator("environment")
    def validate_environment(cls, env_type):
        allowed = ["development", "testing", "production"]
        if env_type.lower() not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return env_type.lower()