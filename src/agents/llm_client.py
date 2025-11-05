"""
LLM Client Integration for AI-Powered OSINT

Provides unified interface to multiple LLM providers (OpenAI, Anthropic)
for autonomous decision-making throughout the intelligence lifecycle
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from enum import Enum


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class LLMClient:
    """
    Unified LLM client for AI-powered intelligence operations
    """

    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ):
        """
        Initialize LLM client

        Args:
            provider: LLM provider (openai, anthropic)
            api_key: API key (defaults to environment variable)
            model: Model name (defaults to best available)
            temperature: Temperature for generation
            max_tokens: Maximum tokens in response
        """
        self.provider = provider.lower()
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.logger = logging.getLogger('LLMClient')

        # Initialize provider-specific client
        if self.provider == "openai":
            self._init_openai(api_key, model)
        elif self.provider == "anthropic":
            self._init_anthropic(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _init_openai(self, api_key: Optional[str], model: Optional[str]):
        """Initialize OpenAI client"""
        try:
            import openai

            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

            self.client = openai.OpenAI(api_key=self.api_key)
            self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')

            self.logger.info(f"Initialized OpenAI client with model: {self.model}")

        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")

    def _init_anthropic(self, api_key: Optional[str], model: Optional[str]):
        """Initialize Anthropic client"""
        try:
            import anthropic

            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            if not self.api_key:
                raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")

            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.model = model or os.getenv('ANTHROPIC_MODEL', 'claude-3-opus-20240229')

            self.logger.info(f"Initialized Anthropic client with model: {self.model}")

        except ImportError:
            raise ImportError("Anthropic library not installed. Run: pip install anthropic")

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """
        Generate completion from LLM

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Override default temperature
            max_tokens: Override default max tokens
            json_mode: Force JSON output

        Returns:
            LLM response as string
        """
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens

        try:
            if self.provider == "openai":
                response = await self._complete_openai(prompt, system_prompt, temp, tokens, json_mode)
            elif self.provider == "anthropic":
                response = await self._complete_anthropic(prompt, system_prompt, temp, tokens, json_mode)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

            return response

        except Exception as e:
            self.logger.error(f"LLM completion failed: {e}")
            raise

    async def _complete_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        json_mode: bool
    ) -> str:
        """OpenAI completion"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)

        return response.choices[0].message.content

    async def _complete_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        json_mode: bool
    ) -> str:
        """Anthropic completion"""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)

        return response.content[0].text

    async def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ):
        """
        Stream completion from LLM (for real-time output)

        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Temperature override

        Yields:
            Response chunks
        """
        temp = temperature if temperature is not None else self.temperature

        if self.provider == "openai":
            async for chunk in self._stream_openai(prompt, system_prompt, temp):
                yield chunk
        elif self.provider == "anthropic":
            async for chunk in self._stream_anthropic(prompt, system_prompt, temp):
                yield chunk

    async def _stream_openai(self, prompt: str, system_prompt: Optional[str], temperature: float):
        """Stream from OpenAI"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def _stream_anthropic(self, prompt: str, system_prompt: Optional[str], temperature: float):
        """Stream from Anthropic"""
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text

    async def analyze_with_context(
        self,
        data: Any,
        analysis_type: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        AI-powered analysis with contextual understanding

        Args:
            data: Data to analyze
            analysis_type: Type of analysis (planning, processing, analysis, decision)
            context: Additional context

        Returns:
            Analysis results
        """
        system_prompts = {
            "planning": "You are an expert OSINT investigation planner. Create comprehensive, strategic investigation plans.",
            "processing": "You are a data processing specialist. Clean, normalize, and structure raw intelligence data.",
            "analysis": "You are a senior intelligence analyst. Synthesize information into actionable intelligence.",
            "decision": "You are a strategic decision-maker. Evaluate situations and recommend optimal actions.",
            "synthesis": "You are an intelligence synthesizer. Connect disparate information into coherent narratives."
        }

        system_prompt = system_prompts.get(analysis_type, "You are an AI assistant analyzing OSINT data.")

        data_str = json.dumps(data, indent=2, default=str) if not isinstance(data, str) else data
        context_str = json.dumps(context, indent=2) if context else ""

        prompt = f"""Analyze the following data:

DATA:
{data_str}

{f'CONTEXT:\n{context_str}' if context else ''}

Provide detailed analysis following best practices for {analysis_type}.
Output your response as valid JSON.
"""

        response = await self.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            json_mode=True
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {"raw_response": response, "error": "JSON parsing failed"}

    async def make_decision(
        self,
        objective: str,
        current_state: Dict,
        options: List[Dict]
    ) -> Dict:
        """
        AI-powered decision making

        Args:
            objective: Investigation objective
            current_state: Current investigation state
            options: Available options/actions

        Returns:
            Decision with rationale
        """
        prompt = f"""You are making a strategic decision for an OSINT investigation.

OBJECTIVE: {objective}

CURRENT STATE:
{json.dumps(current_state, indent=2, default=str)}

AVAILABLE OPTIONS:
{json.dumps(options, indent=2)}

Analyze the situation and make the best decision. Consider:
1. Alignment with objective
2. Efficiency and resource usage
3. Likelihood of success
4. Potential risks

Output as JSON with:
- chosen_option: index of selected option
- rationale: explanation of decision
- confidence: confidence level (0-1)
- alternative_considerations: what else was considered
"""

        response = await self.complete(
            prompt=prompt,
            system_prompt="You are an expert strategic decision-maker for intelligence operations.",
            json_mode=True
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "chosen_option": 0,
                "rationale": "Default choice due to parsing error",
                "confidence": 0.5
            }

    def get_model_info(self) -> Dict:
        """Get information about current model"""
        return {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }


class MockLLMClient(LLMClient):
    """
    Mock LLM client for testing without API keys
    """

    def __init__(self):
        """Initialize mock client"""
        self.provider = "mock"
        self.model = "mock-model"
        self.temperature = 0.7
        self.max_tokens = 4000
        self.logger = logging.getLogger('MockLLMClient')

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """Mock completion"""
        self.logger.info("Mock LLM responding...")

        if json_mode or "JSON" in prompt:
            return json.dumps({
                "mock_response": "This is a mock response",
                "note": "Using mock LLM client for testing",
                "prompt_length": len(prompt)
            })
        else:
            return "This is a mock response from the LLM client. In production, this would be an AI-generated response."

    async def analyze_with_context(self, data: Any, analysis_type: str, context: Optional[Dict] = None) -> Dict:
        """Mock analysis"""
        return {
            "analysis_type": analysis_type,
            "mock_analysis": "Mock analysis results",
            "note": "Using mock LLM client"
        }

    async def make_decision(self, objective: str, current_state: Dict, options: List[Dict]) -> Dict:
        """Mock decision"""
        return {
            "chosen_option": 0,
            "rationale": "Mock decision - choosing first option",
            "confidence": 0.8
        }


def create_llm_client(config: Optional[Dict] = None) -> LLMClient:
    """
    Factory function to create LLM client from configuration

    Args:
        config: Configuration dictionary

    Returns:
        LLM client instance
    """
    if config is None:
        config = {}

    provider = config.get('provider') or os.getenv('DEFAULT_LLM_PROVIDER', 'openai')

    # Check if we have API keys
    if provider == 'openai' and not os.getenv('OPENAI_API_KEY'):
        logging.warning("No OpenAI API key found. Using mock LLM client.")
        return MockLLMClient()
    elif provider == 'anthropic' and not os.getenv('ANTHROPIC_API_KEY'):
        logging.warning("No Anthropic API key found. Using mock LLM client.")
        return MockLLMClient()

    return LLMClient(
        provider=provider,
        api_key=config.get('api_key'),
        model=config.get('model'),
        temperature=config.get('temperature', 0.7),
        max_tokens=config.get('max_tokens', 4000)
    )
