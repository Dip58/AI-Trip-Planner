import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

class ConfigLoader:
    def __init__(self):
        print("Loading configuration...")
        self.config = load_config()
    
    def __getitem__(self,key:str):
        return self.config[key]
    
class ModelLoader(BaseModel):
    
    model_provider: Literal['openai', 'groq']='groq'
    config: ConfigLoader = Field(exclude=True)
    
    def model_post_init(self, __context: Any) -> None:
        #mode_post_init is called after the model is initialized imimediately
        self.config = ConfigLoader()
        
    class Config:
        # This allows the model to accept arbitrary types, such as ConfigLoader
        # which is not a standard Pydantic type.
        arbitrary_types_allowed = True
        
    def load_llm(self):
        # Load the LLM based on the provider specified in the config
        load_dotenv()
        
        if self.model_provider == 'openai':
            print("Loading OpenAI model...")
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
            model_name = self.config['llm']['openai']['model_name']
            llm = ChatOpenAI(
                model=model_name,
                api_key=openai_api_key # type: ignore
            )
            
        elif self.model_provider == 'groq':
            print("Loading Groq model...")
            groq_api_key = os.getenv('GROQ_API_KEY')
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY is not set in the environment variables.")
            model_name= self.config['llm']['groq']['model_name']
            llm = ChatGroq(
                model=model_name,
                api_key=groq_api_key # type: ignore
            )
            
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
        
        return llm
        
    