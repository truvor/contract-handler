from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    DROPBOX_TOKEN: str = ""
    items_per_user: int = 50
    SUPABASE_PROJECT_ID: str = ""
    ALGORITHM: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
