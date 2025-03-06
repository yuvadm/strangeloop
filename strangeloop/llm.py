"""
LLM integration module for Strangeloop.
Provides functionality to interact with Claude Sonnet 3.7.
"""
import os
import requests
import json
from typing import Dict, Any, Optional


class ClaudeClient:
    """Client for interacting with Anthropic's Claude API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        """
        Initialize the Claude client.
        
        Args:
            api_key: Anthropic API key. If None, will try to get from ANTHROPIC_API_KEY env var.
            model: The Claude model to use. Defaults to Claude Sonnet 3.7.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided or set as ANTHROPIC_API_KEY environment variable")
        
        self.model = model
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    
    def ask(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Ask Claude a question and get a response.
        
        Args:
            prompt: The question or prompt to send to Claude
            max_tokens: Maximum number of tokens in the response
            temperature: Controls randomness (0 = deterministic, 1 = creative)
            
        Returns:
            Dict containing the response and metadata
        """
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error communicating with Claude API: {str(e)}")
    
    def get_response_text(self, response: Dict[str, Any]) -> str:
        """
        Extract the text content from Claude's response.
        
        Args:
            response: The response dict from the ask method
            
        Returns:
            The text content of Claude's response
        """
        try:
            content = response.get("content", [])
            if content and len(content) > 0:
                return content[0].get("text", "")
            return ""
        except (KeyError, IndexError, AttributeError) as e:
            raise Exception(f"Error parsing Claude response: {str(e)}")


def ask_claude(prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
    """
    Convenience function to ask Claude a question and get the text response.
    
    Args:
        prompt: The question or prompt to send to Claude
        max_tokens: Maximum number of tokens in the response
        temperature: Controls randomness (0 = deterministic, 1 = creative)
        
    Returns:
        The text content of Claude's response
    """
    client = ClaudeClient()
    response = client.ask(prompt, max_tokens, temperature)
    return client.get_response_text(response)