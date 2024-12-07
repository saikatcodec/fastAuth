from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    POSTGRES_URL: str
    JWT_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    SECRET_KEY: str
    SALT: str
    DOMAIN: str
    
    model_config = SettingsConfigDict(env_file='../.env')
    
setting = Setting()