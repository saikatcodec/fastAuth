from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    POSTGRES_URL: str
    JWT_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file='../.env')
    
setting = Setting()