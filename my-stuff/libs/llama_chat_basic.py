import logging
from typing import List, Dict, Optional
import ollama

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_MODEL = "llama3.2"

class LlamaChatClient:
    """Enhanced Llama chat client with better error handling and configuration."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """
        Initialize the Llama chat client.
        
        Args:
            model: The Llama model to use
        """
        self.model = model
        self.system_message = ""
        self._validate_ollama_connection()
    
    def _validate_ollama_connection(self) -> None:
        """Validate that Ollama is running and the model is available."""
        try:
            # Test if Ollama is responding
            ollama.list()
            logger.info(f"Ollama connection established, using model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            raise Exception("Ollama is not running or not accessible. Please start Ollama and ensure it's running on localhost:11434")
    
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
            response = ollama.chat(
                model=self.model,
                messages=messages,
                stream=False
            )
            
            if not response or 'message' not in response or 'content' not in response['message']:
                raise Exception("Invalid response from Ollama")
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Chat API call failed: {e}")
            raise Exception(f"Failed to get response from Ollama: {str(e)}")
    
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
            stream = ollama.chat(
                model=self.model,
                messages=messages,
                stream=True
            )
            content = ""
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    content += chunk['message']['content']
                    if content:
                        yield content
                        
        except Exception as e:
            logger.error(f"Streaming chat API call failed: {e}")
            raise Exception(f"Failed to get streaming response from Ollama: {str(e)}")

# Global instance for backward compatibility
_global_client = None

def set_system_message(system_prompt: str) -> None:
    """Set system message on global client (deprecated - use LlamaChatClient instead)."""
    global _global_client
    if _global_client is None:
        _global_client = LlamaChatClient()
    _global_client.set_system_message(system_prompt)

def chat(message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
    """Chat using global client (deprecated - use LlamaChatClient instead)."""
    global _global_client
    if _global_client is None:
        _global_client = LlamaChatClient()
    return _global_client.chat(message, history)

