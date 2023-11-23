import dotenv
import os

dotenv.load_dotenv()

class Config :
    open_ai_key = os.getenv("OPENAI_API_KEY")
    assembly_ai_key = os.getenv("ASSEMBLY_AI_API_KEY")
    