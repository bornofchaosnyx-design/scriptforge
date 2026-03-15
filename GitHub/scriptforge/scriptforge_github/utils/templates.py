"""
Template module for ScriptForge.
Handles script templates and template application.
"""

from typing import Dict, Any

def get_templates() -> Dict[str, Dict[str, Any]]:
    """
    Get all available script templates.
    
    Returns:
        Dictionary of template names to template configurations
    """
    templates = {
        "Explainer/Tutorial": {
            "description": "Step-by-step instructional content",
            "default_tone": "Educational",
            "structure": ["Hook", "Problem", "Solution Steps", "Summary", "CTA"],
            "platforms": ["YouTube", "LinkedIn Video"]
        },
        "Product Review": {
            "description": "Honest review of a product or service",
            "default_tone": "Honest/Critical",
            "structure": ["Hook", "Introduction", "Pros", "Cons", "Verdict", "CTA"],
            "platforms": ["YouTube", "TikTok", "Instagram Reels"]
        },
        "Storytelling": {
            "description": "Narrative-driven content with emotional arc",
            "default_tone": "Engaging/Emotional",
            "structure": ["Hook", "Setup", "Conflict", "Resolution", "Lesson", "CTA"],
            "platforms": ["YouTube", "TikTok"]
        },
        "News/Update": {
            "description": "Current events or industry updates",
            "default_tone": "Professional/Informative",
            "structure": ["Headline", "Context", "Details", "Implications", "Outlook", "CTA"],
            "platforms": ["YouTube", "LinkedIn Video"]
        },
        "List/Countdown": {
            "description": "Numbered list or countdown format",
            "default_tone": "Energetic/Exciting",
            "structure": ["Hook", "List Intro", "Items 1-10", "Summary", "CTA"],
            "platforms": ["YouTube", "TikTok", "Instagram Reels"]
        },
        "Q&A": {
            "description": "Question and answer format",
            "default_tone": "Conversational",
            "structure": ["Hook", "Question 1", "Answer 1", "Question 2", "Answer 2", "Summary", "CTA"],
            "platforms": ["YouTube", "Instagram Reels"]
        },
        "Behind the Scenes": {
            "description": "Authentic look at process or daily life",
            "default_tone": "Casual/Authentic",
            "structure": ["Hook", "Context", "Process", "Challenges", "Results", "CTA"],
            "platforms": ["YouTube", "TikTok", "Instagram Reels"]
        },
        "Challenge/Trend": {
            "description": "Participating in or reacting to trends",
            "default_tone": "Fun/Entertaining",
            "structure": ["Hook", "Challenge Intro", "Attempt", "Result", "Reaction", "CTA"],
            "platforms": ["TikTok", "Instagram Reels", "YouTube Shorts"]
        }
    }
    
    return templates

def apply_template(template_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply a template to modify script parameters.
    
    Args:
        template_name: Name of template to apply
        parameters: Current script parameters
    
    Returns:
        Modified parameters with template applied
    """
    templates = get_templates()
    
    if template_name not in templates:
        return parameters
    
    template = templates[template_name]
    
    # Apply template defaults
    modified_params = parameters.copy()
    
    # Set default tone if not specified
    if "tone" not in modified_params or not modified_params["tone"]:
        modified_params["tone"] = template["default_tone"]
    
    # Add template-specific instructions
    if "additional" not in modified_params:
        modified_params["additional"] = ""
    
    template_instructions = f"Use the {template_name} template structure: {', '.join(template['structure'])}. "
    template_instructions += f"Platform focus: {', '.join(template['platforms'])}. "
    template_instructions += f"Tone should be {template['default_tone'].lower()}."
    
    if modified_params["additional"]:
        modified_params["additional"] = template_instructions + " " + modified_params["additional"]
    else:
        modified_params["additional"] = template_instructions
    
    return modified_params

def get_template_prompt(template_name: str) -> str:
    """
    Get the prompt template for a specific template.
    
    Args:
        template_name: Name of template
    
    Returns:
        Template-specific prompt string
    """
    templates = get_templates()
    
    if template_name not in templates:
        return ""
    
    template = templates[template_name]
    
    prompt_parts = [
        f"TEMPLATE: {template_name}",
        f"DESCRIPTION: {template['description']}",
        f"RECOMMENDED STRUCTURE:",
    ]
    
    for i, section in enumerate(template['structure'], 1):
        prompt_parts.append(f"  {i}. {section}")
    
    prompt_parts.append(f"RECOMMENDED TONE: {template['default_tone']}")
    prompt_parts.append(f"OPTIMAL PLATFORMS: {', '.join(template['platforms'])}")
    
    return "\n".join(prompt_parts)

def validate_template_compatibility(template_name: str, platform: str) -> bool:
    """
    Check if a template is compatible with the selected platform.
    
    Args:
        template_name: Template name
        platform: Target platform
    
    Returns:
        True if compatible, False otherwise
    """
    templates = get_templates()
    
    if template_name not in templates:
        return True  # Allow unknown templates
    
    template = templates[template_name]
    return platform in template["platforms"]