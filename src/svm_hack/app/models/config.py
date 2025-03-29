from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()

class Configs(BaseModel):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "test")



cfg = Configs()