from functools import lru_cache
from pydantic import BaseModel
from pydantic import Field
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
	backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
	backend_port: int = Field(default=8000, alias="BACKEND_PORT")

	front_backend_url: str = Field(default="http://localhost:8000", alias="FRONTEND_BACKEND_URL")

	irctc_api_base_url: str | None = Field(default=None, alias="IRCTC_API_BASE_URL")
	irctc_api_key: str | None = Field(default=None, alias="IRCTC_API_KEY")
	irctc_api_host: str | None = Field(default=None, alias="IRCTC_API_HOST")
	irctc_train_info_path: str = Field(default="/train/info", alias="IRCTC_TRAIN_INFO_PATH")

	@computed_field
	@property
	def irctc_configured(self) -> bool:
		return bool(self.irctc_api_base_url and self.irctc_api_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
	return Settings()  # type: ignore[call-arg]