import asyncio
import inspect
import os
import sys
from pathlib import Path
from typing import Optional, Sequence, Mapping, Any, Literal, Union, Coroutine

from dotenv import load_dotenv, find_dotenv
from ollama import Options, ChatResponse
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


# ENVIRONMENT

if DEV_MODE:
    ENV_PATH: str = ".env.dev"
    FILES_PATH: Path = Path(r"D:\FTPFolder\input_files")
    OUTPUT_CLAIMS_PATH: Path = Path(r"D:\FTPFolder\output_claims")
    NOPASSED_PATH: Path = Path(r"D:\FTPFolder\nopassed")
    RESPONSES_PATH: Path = Path(r"D:\FTPFolder\responses")
else:
    ENV_PATH: str = os.getenv("ENV_PATH") or ".env"
    FILES_PATH: Path = get_project_root() / "data/input_files"
    OUTPUT_CLAIMS_PATH: Path = get_project_root() / "data/output_claims"
    NOPASSED_PATH: Path = get_project_root() / "data/nopassed"
    RESPONSES_PATH: Path = get_project_root() / "data/responses"

FILES_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_CLAIMS_PATH.mkdir(parents=True, exist_ok=True)
NOPASSED_PATH.mkdir(parents=True, exist_ok=True)
RESPONSES_PATH.mkdir(parents=True, exist_ok=True)

PATH = find_dotenv(filename=ENV_PATH)

load_dotenv(dotenv_path=PATH)


def require_env(name: str, additional = None):
    value = os.getenv(name)
    if not value and additional or additional == "":
        return additional
    if not value and not (additional or additional in [0, 0.0]):
        raise EnvironmentError(f"{name} is required in environment!")
    return value


# SERVER

HOST: str = require_env("HOST", "0.0.0.0")
PORT: int = require_env("PORT", 11434)

# DATABASE

class DBSettings(BaseSettings):
    """
    ENVIRONMENT AUTO, NO PARAMS NEED
    """
    DB_USER: str = Field(default="")
    DB_PASSWORD: str = Field(default="")
    DB_HOST: str = Field(default=HOST)
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="")

    REDIS_USER: str = Field(default="")
    REDIS_USER_PASSWORD: str = Field(default="")
    REDIS_HOST: str = Field(default=HOST)
    REDIS_PORT: int = Field(default=6379)

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

    def get_reddis_credentials(self):
        return self.REDIS_USER, self.REDIS_USER_PASSWORD, self.REDIS_HOST, self.REDIS_PORT


#  LOGS

LOGS_DIR = get_project_root() / 'Logs'
LOGS_DIR.mkdir(exist_ok=True, parents=True)

# LLM

LLM_MODEL: str = require_env("LLM_MODEL")
LLM_BASE_URL: str = require_env("LLM_BASE_URL", f"{HOST}:{PORT}")
EMBED_MODEL: str = require_env("EMBED_MODEL")

import ollama

class OllamaClient:
    def __init__(self, model: str = LLM_MODEL, url: str = LLM_BASE_URL):
        self._url = url
        self._models_list: list[str] = self.ModelsList
        if not model:
            if not self._models_list:
                raise ValueError("No models available from Ollama server")
            model = self._models_list[0]
        elif model not in self._models_list:
            raise ValueError(f"No model similar to '{model}' found in {self._models_list}")
        self._model: str = model
        self._client: Optional[None] | ollama.AsyncClient | ollama.Client = None

    @property
    async def AsyncClient(self):
        self._client = ollama.AsyncClient(host=self._url)
        return self

    @property
    def Client(self):
        self._client = ollama.Client(host=self._url)
        return self

    @property
    def ModelsList(self):
        models = [m.model for m in ollama.Client(host=self._url).list().models if m.model]
        return models

    def chat(
        self,
        messages: Optional[Sequence[Mapping[str, Any]]] = None,
        tools: Optional[Sequence[Mapping[str, Any]]] = None,
        think: Union[Literal['low', 'medium', 'high'], bool, None] = False,
        stream: bool = False,
        format: Optional[Union[Literal['', 'json'], dict[str, Any]]] = None,
        options: Optional[Mapping[str, Any]] = None,
        keep_alive: Optional[Union[float, str]] = None
    ) -> Union[ChatResponse, Coroutine[Any, Any, ChatResponse]]:
        """
        A universal chat method.
        If encountered in asynchronous await mode, AsyncClient is used.
        If encountered synchronously, Client is used.
        """

        try:
            asyncio.get_running_loop()
            is_async = True
        except RuntimeError:
            is_async = False

        if is_async:
            # Async
            async def _async_chat():
                return await self._client.chat(
                    model=self._model,
                    messages=messages,
                    tools=tools,
                    think=think,
                    format=format,
                    options=options,
                    keep_alive=keep_alive,
                    stream=stream
                )
            return _async_chat()

        # Sync
        return self._client.chat(
            model=self._model,
            messages=messages,
            tools=tools,
            think=think,
            format=format,
            options=options,
            keep_alive=keep_alive,
            stream=stream
        )

    def embeddings(self, input: str | Sequence[str] = '', truncate: bool | None = None,
                   options: Mapping[str, Any] | Options | None = None, keep_alive: float | str | None = None,
                   dimensions: int | None = None):
        try:
            asyncio.get_running_loop()
            is_async = True
        except RuntimeError:
            is_async = False

        if is_async:
            async def _async_embeddings():
                return await self._client.embed(
                    model=self._model,
                    input=input,
                    truncate=truncate,
                    options=options,
                    keep_alive=keep_alive,
                    dimensions=dimensions
                )
            return _async_embeddings()
        return self._client.embed(
            model=self._model,
            input=input,
            truncate=truncate,
            options=options,
            keep_alive=keep_alive,
            dimensions=dimensions
        )

AUTO_SYNONYM_SIM_THRESHOLD = 0.8
DEFAULT_EMBED_DIM = 1024
EMBED_BATCH = 16

# IMPORTS

_current_module = sys.modules[__name__]

__all__ = [
    name
    for name, obj in globals().items()
    if not name.startswith("__") and not name == "DEV_MODE" and not inspect.isfunction(obj)
]

