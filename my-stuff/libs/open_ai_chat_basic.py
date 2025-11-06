
import os
import logging
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1500

class OpenAIChatClient:
    """Enhanced OpenAI chat client with better error handling and configuration."""
    
    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE, 
                 max_tokens: int = DEFAULT_MAX_TOKENS):
        """
        Initialize the OpenAI chat client.
        
        Args:
            model: The OpenAI model to use
            temperature: Controls randomness in responses (0.0 to 2.0)
            max_tokens: Maximum number of tokens in the response
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = ""
        self.client = self._init_openai_client()
    
    def _init_openai_client(self) -> OpenAI:
        """Initialize OpenAI client with proper error handling."""
        try:
            load_dotenv(override=True)
            api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key:
                raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file")
            
            if not api_key.startswith('sk-'):
                raise ValueError("Invalid OpenAI API key format. Key should start with 'sk-'")
            
            logger.info(f"OpenAI API Key configured (begins with: {api_key[:12]}...)")
            return OpenAI(api_key=api_key)
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def set_system_message(self, system_prompt: str) -> None:
        """
        Set the system message for the chat session.
        
        Args:
            system_prompt: The system prompt to guide the AI's behavior
        """
        if not isinstance(system_prompt, str):
            raise ValueError("System prompt must be a string")
        self.system_message = system_prompt
        logger.info("System message updated")
    
    def chat(self, message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Send a chat message and get a response.
        
        Args:
            message: The user's message
            history: Optional chat history as list of message dictionaries
            
        Returns:
            The AI's response as a string
            
        Raises:
            ValueError: If message is empty
            Exception: If API call fails
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        if history is None:
            history = []
        
        try:
            # Build messages array
            messages = []
            
            # Add system message if set
            if self.system_message:
                messages.append({"role": "system", "content": self.system_message})
            
            # Add chat history
            messages.extend(history)
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            if not response.choices:
                raise Exception("Empty response from OpenAI API")
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Chat API call failed: {e}")
            raise Exception(f"Failed to get response from OpenAI: {str(e)}")
    
    def chat_stream(self, message: str, history: Optional[List[Dict[str, str]]] = None):
        """
        Send a chat message and get a streaming response.
        
        Args:
            message: The user's message
            history: Optional chat history as list of message dictionaries
            
        Yields:
            Chunks of the AI's response
            
        Raises:
            ValueError: If message is empty
            Exception: If API call fails
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        if history is None:
            history = []
        
        try:
            # Build messages array
            messages = []
            
            # Add system message if set
            if self.system_message:
                messages.append({"role": "system", "content": self.system_message})
            
            # Add chat history
            messages.extend(history)
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            # Make streaming API call
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            content = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content += chunk.choices[0].delta.content
                    yield content
                    
        except Exception as e:
            logger.error(f"Streaming chat API call failed: {e}")
            raise Exception(f"Failed to get streaming response from OpenAI: {str(e)}")

# Global instance for backward compatibility
_global_client = None

def init_openai():
    """Initialize global OpenAI client (deprecated - use OpenAIChatClient instead)."""
    global _global_client
    _global_client = OpenAIChatClient()
    return _global_client.client

def set_system_message(system_prompt):
    """Set system message on global client (deprecated - use OpenAIChatClient instead)."""
    global _global_client
    if _global_client is None:
        _global_client = OpenAIChatClient()
    _global_client.set_system_message(system_prompt)

def chat(message, history):
    """Chat using global client (deprecated - use OpenAIChatClient instead)."""
    global _global_client
    if _global_client is None:
        _global_client = OpenAIChatClient()
    return _global_client.chat(message, history)