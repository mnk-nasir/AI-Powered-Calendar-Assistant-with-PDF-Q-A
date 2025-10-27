import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    OPENAI_API_KEY: str
    GOOGLE_API_TOKEN: str
    CALENDAR_EMAIL: str
    SLACK_WEBHOOK_URL: str
    mock: bool

    @staticmethod
    def load_from_env() -> "Config":
        o = os.getenv("OPENAI_API_KEY", "")
        g = os.getenv("GOOGLE_API_TOKEN", "")
        c = os.getenv("CALENDAR_EMAIL", "")
        s = os.getenv("SLACK_WEBHOOK_URL", "")
        mock = not (o and g and c)
        return Config(o, g, c, s, mock)
