from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import DatabaseSettings
from .model_configuration import ModelConfiguration
from .ssh_connection import SSHConnection


class Settings(BaseSettings):
    # General Settings
    app_name: str = Field(default="Mi Proyecto", description="Nombre de la aplicación")
    version: str = Field(default="0.0.1", description="Versión")
    environment: Literal["development", "testing", "production"] = Field(
        default="development",
        description="Environment type",
    )
    debug: bool = Field(default=False)

    # Module-specific configurations
    model: ModelConfiguration
    database: DatabaseSettings
    ssh_connection: SSHConnection

    # Pydantic Settings Model Configuration
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        extra="allow",
        env_nested_delimiter="__",
        case_sensitive=False
    )

    @classmethod
    @field_validator("environment")
    def validate_environment(cls, env_type):
        allowed = ["development", "testing", "production"]
        if env_type.lower() not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return env_type.lower()

    @classmethod
    def from_env_file(cls, env_file: Path | None = None):
        """Factory method para crear Settings con archivo .env específico"""
        if env_file:
            return cls(_env_file=env_file)
        return cls()
