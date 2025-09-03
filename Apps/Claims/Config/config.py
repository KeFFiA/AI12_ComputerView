import os
from pathlib import Path

import langchain_ollama
from dotenv import load_dotenv, find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEV_MODE = True

# PATH

def get_project_root() -> Path:
    current_file = Path(__file__).absolute()

    for parent in current_file.parents:
        if (parent / '.git').exists() or (parent / 'requirements.txt').exists():
            return parent

    return current_file.parents[2]

FILES_PATH: Path = get_project_root() / "data/input_files"
OUTPUT_CLAIMS_PATH: Path = get_project_root() / "data/output_claims"
NOPASSED_PATH: Path = get_project_root() / "data/nopassed"
RESPONSES_PATH: Path = get_project_root() / "data/responses"


FILES_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_CLAIMS_PATH.mkdir(parents=True, exist_ok=True)
NOPASSED_PATH.mkdir(parents=True, exist_ok=True)
RESPONSES_PATH.mkdir(parents=True, exist_ok=True)

# ENVIRONMENT

if DEV_MODE:
    ENV_PATH: str = ".env.dev"
else:
    ENV_PATH: str = os.getenv("ENV_PATH") or ".env"

PATH = find_dotenv(filename=ENV_PATH)

load_dotenv(dotenv_path=PATH)

# DATABASE

class DBSettings(BaseSettings):
    """
    ENVIRONMENT AUTO, NO PARAMS NEED
    """
    DB_USER: str = Field(default="")
    DB_PASSWORD: str = Field(default="")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="")

    # REDIS_HOST: str
    # REDIS_PORT: int

    model_config = SettingsConfigDict(
        env_file=PATH, extra='ignore'
    )

    @property
    def db_list(self) -> list[str]:
        """Splits a string into a DB list"""
        return [db.strip() for db in self.DB_NAME.split(",") if db.strip()]

    def get_db_url(self, db_name: str) -> str:
        """Returns DSN for the best matching database (substring match)."""
        if self.DB_USER == "" or self.DB_PASSWORD == "":
            raise ValueError("Database credentials not provided")

        matches = [db for db in self.db_list if db_name.lower() in db.lower()]
        if not matches:
            raise ValueError(f"No database similar to '{db_name}' found in {self.db_list}")
        if len(matches) > 1:
            raise ValueError(f"Ambiguous name '{db_name}', matches: {matches}")
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{matches[0]}")

    # def get_reddis_url(self):
    #     return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

#  LOGS

LOGS_DIR = get_project_root() / 'Logs'
LOGS_DIR.mkdir(exist_ok=True, parents=True)

# LLM

LLM_MODEL: str = os.getenv("LLM_MODEL")
LLM_BASE_URL: str = os.getenv("LLM_BASE_URL")
LLM_TEMPERATURE: float = os.getenv("LLM_TEMPERATURE") or 0.0

llm = langchain_ollama.OllamaLLM(
    model=LLM_MODEL,
    base_url=LLM_BASE_URL,
    temperature=LLM_TEMPERATURE
)


