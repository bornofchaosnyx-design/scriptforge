"""
AI script generation module for ScriptForge
Handles API calls to various AI providers
"""

import json
import requests
import config
from typing import Dict, Any, Optional

def generate_script(params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Generate a video script using AI based on provided parameters
    
    Args:
        params: Dictionary containing script generation parameters
        
    Returns:
        Dictionary with generated script and metadata, or None if failed
    """
    
    # Prepare the prompt based on parameters
    prompt = build_prompt(params)
    
    # Select AI provider based on available API keys
    provider = select_provider()
    
    if not provider:
        return None
    
    try:
        # Generate script using selected provider
        if provider == "deepseek":
            script_text = call_deepseek_api(prompt)
        elif provider == "anthropic":
            script_text = call_anthropic_api(prompt)
        elif provider == "gemini":
            script_text = call_gemini_api(prompt)
        else:
            return None
        
        if not script_text:
            return None
        
        # Parse and clean the script
        cleaned_script = clean_script(script_text)
        
        return {
            "script": cleaned_script,
            "model": config.MODEL_CONFIGS[provider]["model"],
            "provider": provider,
            "params": params
        }
        
    except Exception as e:
        print(f"Error generating script: {e}")
        return None

def build_prompt(params: Dict[str, Any]) -> str:
    """
    Build a detailed prompt for the AI based on parameters
    
    Args:
        params: Dictionary containing script generation parameters
        
    Returns:
        Formatted prompt string
    """
    
    video_type = params.get("video_type", "YouTube")
    video_format = params.get("video_format", "Explainer/Tutorial")
    topic = params.get("topic", "")
    tone = params.get("tone", "Professional")
    audience = params.get("audience", ["General Public"])
    target_length = params.get("target_length", 10)
    include_cta = params.get("include_cta", True)
    key_points = params.get("key_points")
    brand_voice = params.get("brand_voice")
    
    # Determine time units
    time_unit = "minutes" if video_type == "YouTube" else "seconds"
    
    prompt = f"""Generate a {video_type} video script with the following specifications:

TOPIC: {topic}

VIDEO TYPE: {video_type}
VIDEO FORMAT: {video_format}
TARGET LENGTH: {target_length} {time_unit}
TONE: {tone}
TARGET AUDIENCE: {', '.join(audience) if isinstance(audience, list) else audience}
INCLUDE CALL-TO-ACTION: {'Yes' if include_cta else 'No'}

"""
    
    if key_points:
        prompt += f"KEY POINTS TO INCLUDE:\n{key_points}\n\n"
    
    if brand_voice:
        prompt += f"BRAND VOICE/GUIDELINES:\n{brand_voice}\n\n"
    
    # Add format-specific instructions
    if video_type == "YouTube":
        prompt += '''STRUCTURE REQUIREMENTS:
1. Start with a strong HOOK (first 30 seconds) that grabs attention
2. Include clear TIMESTAMPS in brackets (e.g., [0:00-0:30])
3. Structure the content with clear sections
4. Use natural, conversational language
5. Include visual cues in parentheses (e.g., [SHOW SCREENSHOT])
6. End with a clear call-to-action

FORMAT THE SCRIPT LIKE THIS:
[INTRO - 0:00-0:30]
Hook: "Your attention-grabbing opening line here"
Preview: "Brief overview of what the video will cover"

[MAIN CONTENT - 0:30-4:00]
Section 1: [Title]
- Point 1 with explanation
- [VISUAL: Describe what to show]

[CONCLUSION - 4:00-4:30]
Summary: "Brief recap of main points"
CTA: "Clear call to action (subscribe, like, comment, etc.)"

Please generate a complete, ready-to-use script following this format.'''
    
    else:  # TikTok/Short-form
        prompt += '''STRUCTURE REQUIREMENTS:
1. Start with an immediate ATTENTION GRABBER (first 3 seconds)
2. Keep it concise and high-energy
3. Use emojis sparingly for emphasis
4. Include on-screen text suggestions in brackets
5. End with a clear call-to-action

FORMAT THE SCRIPT LIKE THIS:
[0-3s] - Attention grabber (hook)
[3-10s] - Problem/Question setup  
[10-45s] - Main content/solution
[45-55s] - Result/proof/entertainment
[55-60s] - CTA and outro

Please generate a complete, ready-to-use script following this format.'''
    
    return prompt

def select_provider() -> Optional[str]:
    """
    Select which AI provider to use based on available API keys
    
    Returns:
        Provider name or None if no API keys available
    """
    if config.DEEPSEEK_API_KEY:
        return "deepseek"
    elif config.ANTHROPIC_API_KEY:
        return "anthropic"
    elif config.GEMINI_API_KEY:
        return "gemini"
    else:
        return None

def call_deepseek_api(prompt: str) -> Optional[str]:
    """
    Call DeepSeek API to generate script
    
    Args:
        prompt: The prompt to send to the API
        
    Returns:
        Generated text or None if failed
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": config.MODEL_CONFIGS["deepseek"]["model"],
        "messages": [
            {
                "role": "system",
                "content": "You are a professional video scriptwriter specializing in YouTube and TikTok content. Generate engaging, well-structured scripts that follow the specified format exactly."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": config.MODEL_CONFIGS["deepseek"]["max_tokens"],
        "temperature": config.MODEL_CONFIGS["deepseek"]["temperature"],
        "stream": False
    }
    
    try:
        response = requests.post(
            config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            print(f"DeepSeek API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"DeepSeek API call failed: {e}")
        return None

def call_anthropic_api(prompt: str) -> Optional[str]:
    """
    Call Anthropic API to generate script
    
    Args:
        prompt: The prompt to send to the API
        
    Returns:
        Generated text or None if failed
    """
    headers = {
        "Content-Type": "application/json",
        "x-api-key": config.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": config.MODEL_CONFIGS["anthropic"]["model"],
        "max_tokens": config.MODEL_CONFIGS["anthropic"]["max_tokens"],
        "temperature": config.MODEL_CONFIGS["anthropic"]["temperature"],
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(
            config.ANTHROPIC_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["content"][0]["text"]
        else:
            print(f"Anthropic API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Anthropic API call failed: {e}")
        return None

def call_gemini_api(prompt: str) -> Optional[str]:
    """
    Call Gemini API to generate script
    
    Args:
        prompt: The prompt to send to the API
        
    Returns:
        Generated text or None if failed
    """
    url = f"{config.GEMINI_API_URL}?key={config.GEMINI_API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": config.MODEL_CONFIGS["gemini"]["max_tokens"],
            "temperature": config.MODEL_CONFIGS["gemini"]["temperature"]
        }
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Gemini API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return None

def clean_script(script_text: str) -> str:
    """
    Clean and format the generated script
    
    Args:
        script_text: Raw script text from AI
        
    Returns:
        Cleaned and formatted script
    """
    # Remove any markdown formatting if present
    script_text = script_text.replace("```", "")
    
    # Ensure proper line breaks
    lines = script_text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)