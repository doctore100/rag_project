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
        env_file=".env",
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

    @property
    def database_uri_with_env(self) -> str:
        if self.environment == "development":
            return self.database.vector_db_uri
        return f"sqlite:///test_{self.database.name}.db"

    def validate_required_for_production(self):
        """
        Validates the required configurations and settings to ensure they meet secure
        and production-ready standards. This method checks for appropriate values in
        specific settings when the environment is set to production. If any of these
        conditions fail, a ValueError is raised that includes details about the missing
        or insecure configurations.

        :raises ValueError: If any required fields are missing or have insecure values
                            when `is_production` is True.
        """
        if self.is_production:
            required_fields = []

            if not self.auth.secret_key or len(self.auth.secret_key) < 32:
                required_fields.append("AUTH__SECRET_KEY (min 32 chars)")

            if self.database.password == "password" or len(self.database.password) < 8:
                required_fields.append("DATABASE__PASSWORD (secure password)")

            if self.debug:
                required_fields.append("DEBUG should be False in production")

            if required_fields:
                raise ValueError(
                    f"Production validation failed. Required: {', '.join(required_fields)}"
                )

    @classmethod
    def from_env_file(cls, env_file: Path | None = None):
        """Factory method para crear Settings con archivo .env específico"""
        if env_file:
            return cls(_env_file=env_file)
        return cls()