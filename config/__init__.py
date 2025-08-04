from os import getenv
from pathlib import Path

from .settings import Settings


def create_settings() -> Settings:
    """
    Creates and initializes a `Settings` instance based on the project's environment configuration.

    This function determines the application's environment by reading the `ENVIRONMENT` system 
    environment variable. Based on its value, it selects the appropriate `.env` file for the 
    environment. If no valid environment is specified, it defaults to the development environment. 
    If the environment is set to production, additional validations are performed to ensure 
    critical configurations are proper.

    :param: None
    :return: A fully configured `Settings` instance.
    :rtype: Settings
    """

    # Project's root directory
    project_root = Path(__file__).resolve().parent

    # Get the ENVIRONMENT system variable directly (with fallback)
    env_value = getenv("ENVIRONMENT", "development").lower()

    #  Match the appropriate .env file
    env_file_map = {
        "development": project_root / ".env.development",
        "production": project_root / ".env.production",
        "testing": project_root / ".env.testing"
    }

    selected_env_file = env_file_map.get(env_value, None)

    # Instance Settings using that file
    environment_settings = Settings.from_env_file(selected_env_file.name) if selected_env_file else Settings.from_env_file()

    # Validaciones y setup
    if environment_settings.environment == "production":
        environment_settings.validate_required_for_production()

    return environment_settings
