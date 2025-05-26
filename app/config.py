from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NARAKEET_API_URL: str = "https://api.narakeet.com/text-to-speech/m4a?voice=menzi"
    NARAKEET_API_KEY: str 
    VOICE: str = 'menzi'
    
    model_config = SettingsConfigDict(env_file=".env")
    
Config = Settings()