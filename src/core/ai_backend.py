import requests
from ..utils.logger import logger
from ..utils.config_manager import config

class AIBackend:
    """Handles communication with the AI Provider (Groq)."""
    
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    def __init__(self):
        self.api_key = config.groq_api_key
        self.model = config.get("ai_model", "llama-3.3-70b-versatile")
        
        self.system_prompt = """You are "One Above All", an advanced AI assistant that analyzes screen content to help users.

Your task:
1. Identify any questions in the captured screen text.
2. For multiple choice questions: state the correct answer with a brief explanation.
3. For programming questions: provide concise code solutions.
4. For factual questions: give accurate, direct answers.
5. If no clear question is found, summarize the key information visible.

Format your responses cleanly. Be direct, accurate, and helpful. Use markdown formatting with **bold** for important points."""

    def query(self, screen_text: str) -> str:
        """Sends extracted text to the AI and returns the response."""
        if not self.api_key:
            logger.error("Groq API key is missing.")
            return "❌ **API Key Missing**\n\nPlease add your Groq API key to the `.env` file."
            
        logger.info(f"Querying AI ({self.model})...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Analyze this screen content and help me:\n\n{screen_text[:4000]}"}
            ],
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(
                self.GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                
                usage = result.get('usage', {})
                tokens_used = usage.get('total_tokens', 'N/A')
                logger.info(f"AI Response received. Tokens used: {tokens_used}")
                
                return answer
            elif response.status_code == 401:
                logger.error("Invalid Groq API Key.")
                return "❌ **Invalid API Key**\n\nPlease check your Groq API key in the `.env` file."
            elif response.status_code == 429:
                logger.warning("Rate limit exceeded.")
                return "⏳ **Rate Limit**\n\nFree tier limit reached. Please wait a moment."
            else:
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
                logger.error(f"API Error {response.status_code}: {error_msg}")
                return f"❌ **API Error {response.status_code}**\n\n{error_msg[:200]}"
                
        except requests.exceptions.Timeout:
            logger.error("AI request timed out.")
            return "⏱️ **Request Timed Out**\n\nPlease try again."
        except Exception as e:
            logger.error(f"Connection error to AI backend: {e}")
            return f"❌ **Connection Error**\n\nCould not connect to AI backend."
