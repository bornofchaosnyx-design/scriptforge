#!/usr/bin/env python3
"""
ScriptForge: AI-Powered Video Script Generator
Main Streamlit application for generating YouTube/TikTok scripts using AI.
"""

import streamlit as st
import os
import json
from datetime import datetime
from utils.ai import generate_script
from utils.export import export_script
from utils.search import search_trending_topics
import config

# Page configuration
st.set_page_config(
    page_title="ScriptForge - AI Video Script Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark glassmorphism theme
st.markdown('''
<style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Gradient headers */
    .gradient-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .gradient-subheader {
        background: linear-gradient(90deg, #00dbde 0%, #fc00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    /* Neon buttons */
    .neon-button {
        background: linear-gradient(90deg, #00dbde 0%, #fc00ff 100%);
        border: none;
        color: white;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 25px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .neon-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 219, 222, 0.4);
    }
    
    /* Script section colors */
    .script-intro {
        border-left: 5px solid #667eea;
    }
    
    .script-content {
        border-left: 5px solid #00dbde;
    }
    
    .script-conclusion {
        border-left: 5px solid #fc00ff;
    }
    
    .script-cta {
        border-left: 5px solid #764ba2;
    }
    
    /* Timeline visualization */
    .timeline-container {
        display: flex;
        align-items: center;
        margin: 30px 0;
        overflow-x: auto;
        padding: 10px 0;
    }
    
    .timeline-segment {
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.8rem;
        border-radius: 5px;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .timeline-segment:hover {
        transform: scale(1.05);
        z-index: 10;
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 1px solid #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Success/error messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* Script display box */
    .script-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        color: #e0e0e0;
        max-height: 400px;
        overflow-y: auto;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(90deg, #00dbde 0%, #fc00ff 100%);
    }
</style>
''', unsafe_allow_html=True)

# Helper functions for glassmorphism UI
def glass_card(content, title=None, color_class=""):
    """Create a glassmorphism card"""
    card_html = f'''
    <div class="glass-card {color_class}" style="margin: 15px 0;">
    '''
    if title:
        card_html += f'<h3 style="margin-top: 0; color: white;">{title}</h3>'
    card_html += f'{content}</div>'
    return card_html

def script_section_card(title, content, duration, section_type="content"):
    """Create a color-coded script section card"""
    colors = {
        "intro": "#667eea",
        "content": "#00dbde", 
        "conclusion": "#fc00ff",
        "cta": "#764ba2"
    }
    
    color = colors.get(section_type, "#00dbde")
    
    return f'''
    <div class="glass-card" style="border-left: 5px solid {color}; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="margin: 0; color: {color};">{title}</h4>
            <span style="background: {color}20; color: {color}; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem;">
                {duration}
            </span>
        </div>
        <div style="color: #e0e0e0; line-height: 1.6;">{content}</div>
    </div>
    '''

def create_timeline(sections):
    """Create a visual timeline for script sections"""
    if not sections:
        return ""
    
    timeline_html = '''
    <div class="timeline-container">
        <div style="display: flex; gap: 5px;">
    '''
    
    for section in sections:
        width = section.get('width', 100)
        color = section.get('color', '#667eea')
        title = section.get('title', 'Section')
        
        timeline_html += f'''
            <div class="timeline-segment" style="width: {width}px; background: {color};" 
                 title="{title} - {section.get('duration', '')}">
                {title}
            </div>
        '''
    
    timeline_html += '''
        </div>
    </div>
    '''
    return timeline_html

def preview_modal(template):
    """Create a preview modal for a template"""
    platform_colors = {
        "YouTube": "#FF0000",
        "TikTok": "#000000",
        "Instagram": "#E4405F",
        "LinkedIn": "#0A66C2"
    }
    
    color = platform_colors.get(template.get('platform', 'YouTube'), "#667eea")
    
    # Create modal HTML with template details
    modal_id = f"preview_modal_{template.get('name', 'default').replace(' ', '_').replace('/', '_')}"
    modal_html = f'''
<div id="{modal_id}" style="background: rgba(0, 0, 0, 0.8); position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 9999; display: flex; align-items: center; justify-content: center; padding: 20px;" onclick="if(event.target === this) document.getElementById('close_modal_submit').click()">
    <div class="glass-card" style="max-width: 800px; width: 100%; max-height: 80vh; overflow-y: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: white; display: flex; align-items: center; gap: 10px;">
                <div style="width: 40px; height: 40px; background: {color}; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                    {template.get('platform', 'YT')[0]}
                </div>
                {template.get('name', 'Unnamed Template')}
            </h3>
            <button onclick="document.getElementById('close_modal_submit').click()" style="background: transparent; border: none; color: #aaa; font-size: 1.5rem; cursor: pointer;">
                ×
            </button>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
            <div>
                <h4 style="color: {color}; margin: 0 0 10px 0;">📋 Template Details</h4>
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px;">
                    <p style="margin: 0 0 10px 0;"><strong>Platform:</strong> {template.get('platform', 'YouTube')}</p>
                    <p style="margin: 0 0 10px 0;"><strong>Length:</strong> {template.get('estimated_length', 'N/A')}</p>
                    <p style="margin: 0 0 10px 0;"><strong>Sections:</strong> {len(template.get('structure', []))}</p>
                    <p style="margin: 0;"><strong>Best for:</strong> {template.get('best_for', 'Various content')}</p>
                </div>
            </div>
            
            <div>
                <h4 style="color: {color}; margin: 0 0 10px 0;">🎯 Platform Tips</h4>
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px;">
'''
    
    # Add platform-specific tips
    platform_tips = {
        "YouTube": "• Hook in first 15 seconds<br>• Use chapters for navigation<br>• End screen for retention",
        "TikTok": "• Start with action<br>• Use trending audio<br>• Text overlays essential<br>• 7-15 seconds optimal",
        "Instagram": "• Vertical format (9:16)<br>• Caption storytelling<br>• Hashtag strategy (3-5-2)",
        "LinkedIn": "• Professional tone<br>• Value-first approach<br>• Call to action for engagement"
    }
    
    modal_html += platform_tips.get(template.get('platform', 'YouTube'), "• Clear structure<br>• Engaging content<br>• Strong call to action")
    
    modal_html += f'''
                </div>
            </div>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h4 style="color: {color}; margin: 0 0 10px 0;">📝 Description</h4>
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px;">
                <p style="margin: 0; line-height: 1.5;">{template.get('description', 'No description available.')}</p>
            </div>
        </div>
        
        <div style="margin-bottom: 20px;">
            <h4 style="color: {color}; margin: 0 0 10px 0;">🏗️ Template Structure</h4>
            <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px;">
'''
    
    # Add template structure
    structure = template.get('structure', [])
    if structure:
        for i, section in enumerate(structure, 1):
            modal_html += f'''
                <div style="margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: {color};">{i}. {section.get('title', 'Section')}</strong>
                        <span style="color: #aaa; font-size: 0.9rem;">{section.get('duration', 'N/A')}</span>
                    </div>
                    <p style="margin: 5px 0 0 0; color: #ccc; font-size: 0.9rem;">{section.get('description', '')}</p>
                </div>
'''
    else:
        modal_html += '<p style="color: #aaa; margin: 0;">No structure details available.</p>'
    
    modal_html += f'''
            </div>
        </div>
        
        <div style="display: flex; gap: 10px; justify-content: flex-end;">
            <button onclick="document.getElementById('close_modal_submit').click()" style="background: transparent; border: 1px solid {color}; color: {color}; padding: 10px 20px; border-radius: 20px; cursor: pointer; font-weight: bold;">
                Close Preview
            </button>
            <button onclick="document.getElementById('close_modal_submit').click(); alert('Click \\\"Use Template\\\" button on the template card to select this template.')" style="background: {color}; border: none; color: white; padding: 10px 20px; border-radius: 20px; cursor: pointer; font-weight: bold;">
                🚀 Use This Template
            </button>
        </div>
    </div>
</div>
'''
    
    return modal_html

def load_templates():
    """Load all template files from templates directory"""
    import json
    import os
    
    templates = []
    template_dir = "templates"
    
    if not os.path.exists(template_dir):
        return templates
    
    for filename in os.listdir(template_dir):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(template_dir, filename), 'r') as f:
                    template_data = json.load(f)
                    template_data['filename'] = filename
                    templates.append(template_data)
            except Exception as e:
                print(f"Error loading template {filename}: {e}")
    
    return templates

def template_card_html(template, index):
    """Generate HTML for a template card"""
    platform_colors = {
        "YouTube": "#FF0000",
        "TikTok": "#000000",
        "Instagram": "#E4405F",
        "LinkedIn": "#0A66C2"
    }
    
    color = platform_colors.get(template.get('platform', 'YouTube'), "#667eea")
    
    return f'''
    <div class="glass-card" style="margin: 10px 0; border-left: 5px solid {color};">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <div style="width: 50px; height: 50px; background: {color}; 
                 border-radius: 12px; display: flex; align-items: center; 
                 justify-content: center; color: white; font-size: 1.5rem; font-weight: bold;">
                {template.get('platform', 'YT')[0]}
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0; color: white;">{template.get('name', 'Unnamed Template')}</h4>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #aaa;">
                    {template.get('platform', 'YouTube')} • {template.get('estimated_length', 'N/A')}
                </p>
            </div>
        </div>
        
        <p style="font-size: 0.9rem; color: #ccc; margin-bottom: 15px; line-height: 1.4;">
            {template.get('description', 'No description available.')}
        </p>
        
        <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 15px;">
            <button class="neon-button" style="background: {color}40; border: 1px solid {color}; color: {color}; " 
                    onclick="document.getElementById('preview_btn_{index}').click()">
                👁️ Preview
            </button>
            <button class="neon-button" style="background: {color}; border: none; color: white; "
                    onclick="document.getElementById('use_template_btn_{index}').click()">
                Use Template →
            </button>
        </div>
    </div>
    '''

def map_template_to_form(template):
    """Map template data to form parameters"""
    platform = template.get('platform', 'YouTube')
    name = template.get('name', '')
    
    # Map template name to video format
    format_mapping = {
        # YouTube formats
        "YouTube Explainer": "Explainer/Tutorial",
        "YouTube Product Review": "Product Review",
        "YouTube Vlog / Storytime": "Vlog/Storytime",
        "YouTube Educational / How-To": "Educational",
        "YouTube Interview / Conversation": "Interview",
        
        # TikTok formats
        "TikTok Quick Tip": "Quick Tip",
        "TikTok Trend / Challenge": "Trend/Challenge",
        "TikTok Product Showcase": "Product Showcase",
        
        # Instagram formats
        "Instagram Reels Tutorial": "Quick Tip",  # Closest match
        "Instagram Reels Entertainment": "Entertainment",
        
        # LinkedIn formats
        "LinkedIn Professional Insight": "Professional",
        "LinkedIn Career Advice": "Educational"  # Closest match
    }
    
    # Map platform to tone suggestions
    tone_mapping = {
        "YouTube": "Professional",
        "TikTok": "Energetic/Exciting",
        "Instagram": "Casual/Friendly",
        "LinkedIn": "Professional"
    }
    
    # Parse estimated length from template
    estimated_length = template.get('estimated_length', '10 minutes')
    length_value = 10  # default
    
    try:
        # Extract number from string like "10-15 minutes" or "30-60 seconds"
        import re
        numbers = re.findall(r'\d+', estimated_length)
        if numbers:
            length_value = int(numbers[0])
    except:
        length_value = 10
    
    # Determine if minutes or seconds based on platform and estimated_length
    estimated_length_lower = estimated_length.lower()
    
    if "minute" in estimated_length_lower:
        # Template specifies minutes
        length_unit = "minutes"
        if platform != "YouTube":
            # Convert minutes to seconds for non-YouTube platforms in form
            length_value = length_value * 60
            if length_value > 180:  # Cap at 3 minutes (180 seconds)
                length_value = 180
        elif length_value > 30:  # Cap at 30 minutes for YouTube
            length_value = 30
    else:
        # Template specifies seconds or default
        length_unit = "seconds"
        if platform == "YouTube":
            # Convert seconds to minutes for YouTube
            length_value = max(1, length_value // 60)  # At least 1 minute
            if length_value > 30:  # Cap at 30 minutes
                length_value = 30
        elif length_value > 180:  # Cap at 3 minutes for short-form
            length_value = 180
    
    return {
        "video_type": platform,
        "video_format": format_mapping.get(name, "Explainer/Tutorial"),
        "target_length": length_value,
        "tone": tone_mapping.get(platform, "Professional"),
        "audience": ["General Public"],  # Default audience
        "include_cta": True
    }

# Initialize session state
if 'generated_script' not in st.session_state:
    st.session_state.generated_script = None
if 'script_metadata' not in st.session_state:
    st.session_state.script_metadata = {}
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'template_params' not in st.session_state:
    st.session_state.template_params = {}
if 'show_preview_modal' not in st.session_state:
    st.session_state.show_preview_modal = False
if 'preview_template' not in st.session_state:
    st.session_state.preview_template = None

def main():
    """Main application function"""
    
    # Header with gradient styling
    st.markdown('<h1 class="gradient-header">🎬 ScriptForge</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-subheader">AI-Powered Video Script Generator for YouTube & TikTok</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Enter your AI API Key:",
            type="password",
            help="Get an API key from DeepSeek, Anthropic, or Gemini"
        )
        
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
            st.success("✅ API Key set!")
        else:
            st.warning("⚠️ Please enter an API key to generate scripts")
        
        st.divider()
        
        # Video type selection - use template params if available
        default_video_type = st.session_state.template_params.get("video_type", "YouTube")
        video_type = st.selectbox(
            "Video Platform:",
            ["YouTube", "TikTok", "Instagram Reels", "LinkedIn Video"],
            index=["YouTube", "TikTok", "Instagram Reels", "LinkedIn Video"].index(default_video_type) 
            if default_video_type in ["YouTube", "TikTok", "Instagram Reels", "LinkedIn Video"] else 0
        )
        
        # Video format - use template params if available
        if video_type == "YouTube":
            youtube_formats = ["Explainer/Tutorial", "Product Review", "Vlog/Storytime", 
                              "List/Countdown", "Interview", "Educational"]
            default_format = st.session_state.template_params.get("video_format", "Explainer/Tutorial")
            format_index = youtube_formats.index(default_format) if default_format in youtube_formats else 0
            video_format = st.selectbox(
                "Video Format:",
                youtube_formats,
                index=format_index
            )
            default_length = st.session_state.template_params.get("target_length", 10)
            target_length = st.slider("Target Length (minutes):", 1, 30, default_length)
        else:  # Short-form
            short_formats = ["Quick Tip", "Trend/Challenge", "Behind the Scenes", 
                            "Product Showcase", "Question/Answer", "Entertainment"]
            default_format = st.session_state.template_params.get("video_format", "Quick Tip")
            format_index = short_formats.index(default_format) if default_format in short_formats else 0
            video_format = st.selectbox(
                "Video Format:",
                short_formats,
                index=format_index
            )
            default_length = st.session_state.template_params.get("target_length", 60)
            target_length = st.slider("Target Length (seconds):", 15, 180, default_length)
        
        # Tone selection - use template params if available
        tones = ["Professional", "Casual/Friendly", "Energetic/Exciting", 
                "Humorous/Funny", "Inspirational", "Educational/Authoritative"]
        default_tone = st.session_state.template_params.get("tone", "Professional")
        tone_index = tones.index(default_tone) if default_tone in tones else 0
        tone = st.selectbox(
            "Tone:",
            tones,
            index=tone_index
        )
        
        # Target audience - use template params if available
        audience_options = ["General Public", "Tech Enthusiasts", "Business Professionals", 
                           "Students", "Creatives/Artists", "Gamers", "Parents", "Fitness Enthusiasts"]
        default_audience = st.session_state.template_params.get("audience", ["General Public"])
        audience = st.multiselect(
            "Target Audience:",
            audience_options,
            default=default_audience
        )
        
        # Include call to action - use template params if available
        default_cta = st.session_state.template_params.get("include_cta", True)
        include_cta = st.checkbox("Include Call-to-Action", value=default_cta)
        
        # Template status and clear button
        if st.session_state.selected_template:
            st.divider()
            st.info(f"📋 Using template: **{st.session_state.selected_template.get('name')}**")
            if st.button("Clear Template", type="secondary", use_container_width=True):
                st.session_state.selected_template = None
                st.session_state.template_params = {}
                st.rerun()
        
        # Pro features (if enabled)
        if config.ENABLE_PRO_FEATURES:
            st.divider()
            st.header("🔍 Pro Features")
            
            use_trend_analysis = st.checkbox("Analyze trending topics")
            if use_trend_analysis:
                search_query = st.text_input("Search for trending topics related to:")
                if search_query:
                    with st.spinner("Searching for trends..."):
                        trends = search_trending_topics(search_query)
                        if trends:
                            st.info(f"Found {len(trends)} trending topics")
                            for trend in trends[:3]:
                                st.write(f"• {trend}")
                        else:
                            st.warning("""
                            **Trend analysis unavailable**  
                            Pro features require a Brave Search API key.  
                            Get a free key at: https://brave.com/search/api/
                            
                            Add to your `.env` file:
                            ```
                            BRAVE_API_KEY=your_key_here
                            ```
                            """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Script Generator Card
        st.markdown(glass_card('''
        <h3 style="margin-top: 0; color: white;">📝 Script Generator</h3>
        
        <div style="margin-bottom: 20px;">
        ''', color_class="script-content"), unsafe_allow_html=True)
        
        # Topic input
        topic = st.text_area(
            "Enter your video topic:",
            placeholder="e.g., 'How to start a YouTube channel in 2026' or '5 productivity apps that changed my life'",
            height=100
        )
        
        # Additional context
        with st.expander("➕ Add More Context (Optional)"):
            key_points = st.text_area(
                "Key points to include:",
                placeholder="List the main points you want to cover, one per line",
                height=100
            )
            brand_voice = st.text_input(
                "Brand voice/guidelines:",
                placeholder="e.g., 'Keep it casual, use emojis occasionally'"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate button with custom styling
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 Generate Script", type="primary", use_container_width=True):
                if not api_key:
                    st.error("Please enter your API key in the sidebar first!")
                elif not topic.strip():
                    st.error("Please enter a topic for your video!")
                else:
                    with st.spinner("🤖 AI is crafting your script..."):
                        try:
                            # Prepare parameters
                            params = {
                                "topic": topic,
                                "video_type": video_type,
                                "video_format": video_format,
                                "target_length": target_length,
                                "tone": tone,
                                "audience": audience,
                                "include_cta": include_cta,
                                "key_points": key_points if key_points else None,
                                "brand_voice": brand_voice if brand_voice else None
                            }
                            
                            # Generate script
                            script_result = generate_script(params)
                            
                            if script_result:
                                st.session_state.generated_script = script_result["script"]
                                st.session_state.script_metadata = {
                                    "params": params,
                                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "model_used": script_result.get("model", "Unknown")
                                }
                                st.success("✅ Script generated successfully!")
                            else:
                                st.error("Failed to generate script. Please check your API key and try again.")
                                
                        except Exception as e:
                            st.error(f"Error generating script: {str(e)}")
        
        # Display generated script
        if st.session_state.generated_script:
            st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)
            
            # Generated Script Card
            st.markdown(glass_card('''
            <h3 style="margin-top: 0; color: white;">📄 Generated Script</h3>
            
            <div style="margin-bottom: 20px;">
            ''', color_class="script-conclusion"), unsafe_allow_html=True)
            
            # Script metadata with timeline
            with st.expander("📊 Script Details & Timeline", expanded=True):
                col_meta1, col_meta2 = st.columns(2)
                
                with col_meta1:
                    st.write(f"**Generated:** {st.session_state.script_metadata.get('generated_at', 'Unknown')}")
                    st.write(f"**Platform:** {st.session_state.script_metadata['params']['video_type']}")
                    st.write(f"**Format:** {st.session_state.script_metadata['params']['video_format']}")
                
                with col_meta2:
                    st.write(f"**Tone:** {st.session_state.script_metadata['params']['tone']}")
                    st.write(f"**Length:** {st.session_state.script_metadata['params']['target_length']} {'minutes' if st.session_state.script_metadata['params']['video_type'] == 'YouTube' else 'seconds'}")
                    st.write(f"**Model:** {st.session_state.script_metadata.get('model_used', 'Unknown')}")
                
                # Create timeline visualization
                script_text = st.session_state.generated_script
                sections = []
                
                # Parse script for sections (simplified)
                if "[INTRO" in script_text or "[HOOK" in script_text:
                    sections.append({"title": "Intro", "duration": "0-30s", "width": 80, "color": "#667eea"})
                if "[MAIN" in script_text or "[CONTENT" in script_text:
                    sections.append({"title": "Content", "duration": "30s-4m", "width": 160, "color": "#00dbde"})
                if "[CONCLUSION" in script_text:
                    sections.append({"title": "Conclusion", "duration": "4-4:30m", "width": 60, "color": "#fc00ff"})
                if "CTA" in script_text:
                    sections.append({"title": "CTA", "duration": "End", "width": 40, "color": "#764ba2"})
                
                if sections:
                    st.markdown("**Script Timeline:**")
                    st.markdown(create_timeline(sections), unsafe_allow_html=True)
            
            # Script content in styled box
            st.markdown("**Script Content:**")
            st.markdown('<div class="script-box">', unsafe_allow_html=True)
            st.write(st.session_state.generated_script)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export options in a grid
            st.markdown("**💾 Export Options:**")
            export_col1, export_col2, export_col3, export_col4 = st.columns(4)
            
            with export_col1:
                if st.button("📋 Copy", use_container_width=True, help="Copy script to clipboard"):
                    st.success("📋 Script copied to clipboard!")
            
            with export_col2:
                if st.button("📄 TXT", use_container_width=True, help="Download as text file"):
                    export_path = export_script(
                        st.session_state.generated_script,
                        st.session_state.script_metadata,
                        format="txt"
                    )
                    if export_path:
                        with open(export_path, "r") as f:
                            st.download_button(
                                label="⬇️ TXT",
                                data=f.read(),
                                file_name=f"scriptforge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
            
            with export_col3:
                if st.button("📝 DOCX", use_container_width=True, help="Download as Word document"):
                    export_path = export_script(
                        st.session_state.generated_script,
                        st.session_state.script_metadata,
                        format="docx"
                    )
                    if export_path:
                        with open(export_path, "rb") as f:
                            st.download_button(
                                label="⬇️ DOCX",
                                data=f.read(),
                                file_name=f"scriptforge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
            
            with export_col4:
                if st.button("📊 JSON", use_container_width=True, help="Download as JSON data"):
                    export_path = export_script(
                        st.session_state.generated_script,
                        st.session_state.script_metadata,
                        format="json"
                    )
                    if export_path:
                        with open(export_path, "r") as f:
                            st.download_button(
                                label="⬇️ JSON",
                                data=f.read(),
                                file_name=f"scriptforge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                                use_container_width=True
                            )
            
            # Regenerate options
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            st.markdown("**🔄 Regenerate Options:**")
            regenerate_col1, regenerate_col2, regenerate_col3 = st.columns(3)
            
            with regenerate_col1:
                if st.button("🔄 Similar", use_container_width=True, help="Regenerate with similar parameters"):
                    # Clear current script to trigger regeneration
                    st.session_state.generated_script = None
                    st.rerun()
            
            with regenerate_col2:
                if st.button("🎯 Refine", use_container_width=True, help="Refine with adjustments"):
                    st.info("Refine feature coming in v2!")
            
            with regenerate_col3:
                if st.button("🆕 Fresh", use_container_width=True, help="Start fresh with new topic"):
                    # Clear everything
                    st.session_state.generated_script = None
                    st.session_state.script_metadata = {}
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Create tabs for different right panel content
        tab1, tab2 = st.tabs(["💡 Tips & Examples", "🎨 Template Gallery"])
        
        with tab1:
            # Tips & Examples Card
            st.markdown(glass_card('''
            <h3 style="margin-top: 0; color: white;">💡 Quick Start Guide</h3>
            
            <div style="margin-bottom: 20px;">
            ''', color_class="script-intro"), unsafe_allow_html=True)
            
            with st.expander("🎯 Example Topics", expanded=True):
                st.write("**YouTube Examples:**")
                st.write("- How to build a personal brand on LinkedIn")
                st.write("- 3 budgeting apps that saved me $500/month")
                st.write("- The future of AI in content creation")
                
                st.write("**TikTok Examples:**")
                st.write("- Quick morning routine for productivity")
                st.write("- Book recommendations for entrepreneurs")
                st.write("- Behind the scenes of my creative process")
            
            with st.expander("📊 Best Practices"):
                st.write("1. **Be specific** with your topic")
                st.write("2. **Define your audience** clearly")
                st.write("3. **Choose the right tone** for your brand")
                st.write("4. **Include a clear CTA** (Call to Action)")
                st.write("5. **Review and edit** the AI output")
            
            with st.expander("⚡ Quick Templates"):
                col_temp1, col_temp2 = st.columns(2)
                with col_temp1:
                    if st.button("📈 Explainer", use_container_width=True):
                        st.session_state.generated_script = '''[INTRO - 0:00-0:30]
Hook: "Have you ever wondered [question related to topic]?"
Preview: "Today I'm going to show you [what they'll learn]."

[MAIN CONTENT - 0:30-4:00]
Step 1: [First key point]
- Explanation
- Example/Visual

Step 2: [Second key point]  
- Explanation
- Example/Visual

Step 3: [Third key point]
- Explanation
- Example/Visual

[CONCLUSION - 4:00-4:30]
Summary: "So to recap, [brief summary]"
CTA: "If you found this helpful, [subscribe/like/comment]"
Outro: "Thanks for watching! See you in the next one.'''
                        st.rerun()
                
                with col_temp2:
                    if st.button("🎬 Storytime", use_container_width=True):
                        st.session_state.generated_script = '''[HOOK - 0:00-0:15]
"So something crazy happened to me [recently/time frame]..."

[SETUP - 0:15-1:00]
"Let me set the scene: [describe situation/context]"

[CONFLICT - 1:00-2:30]
"Then suddenly... [describe the problem/interesting event]"

[RESOLUTION - 2:30-3:30]
"Here's how it all worked out... [describe solution/outcome]"

[LESSON - 3:30-4:00]
"What I learned from this: [key takeaway]"

[CTA - 4:00-4:30]
"If you've had a similar experience, [share in comments/follow for more]'''
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            # Template Gallery Card
            st.markdown(glass_card('''
            <h3 style="margin-top: 0; color: white;">🎨 Template Gallery</h3>
            <p style="color: #aaa; margin-bottom: 20px;">Choose from professional templates optimized for different platforms</p>
            
            <div style="margin-bottom: 20px;">
            ''', color_class="script-content"), unsafe_allow_html=True)
            
            # Load and display templates
            templates = load_templates()
            
            if not templates:
                st.info("No templates found. Creating sample templates...")
                # Create some sample template data for display
                sample_templates = [
                    {
                        "name": "YouTube Product Review",
                        "platform": "YouTube",
                        "estimated_length": "8-12 minutes",
                        "description": "Professional product review format with pros/cons and recommendations",
                        "structure": []
                    },
                    {
                        "name": "YouTube Vlog / Storytime",
                        "platform": "YouTube",
                        "estimated_length": "10-15 minutes",
                        "description": "Personal storytelling format for vlogs and personal experiences",
                        "structure": []
                    },
                    {
                        "name": "TikTok Trend / Challenge",
                        "platform": "TikTok",
                        "estimated_length": "15-45 seconds",
                        "description": "Fast-paced trend participation optimized for TikTok algorithm",
                        "structure": []
                    }
                ]
                
                for i, template in enumerate(sample_templates):
                    st.markdown(template_card_html(template, i), unsafe_allow_html=True)
                    
                    # Hidden buttons for Streamlit to capture clicks
                    if st.button("Preview", key=f"preview_sample_btn_{i}", type="secondary", help="", args=None, kwargs=None):
                        st.session_state.show_preview_modal = True
                        st.session_state.preview_template = template
                        st.rerun()
                    
                    if st.button("Use Template", key=f"use_sample_template_btn_{i}", type="secondary", help="", args=None, kwargs=None):
                        st.session_state.selected_template = template
                        st.session_state.template_params = map_template_to_form(template)
                        st.success(f"✅ Template loaded: {template['name']}")
                        st.rerun()
            else:
                st.success(f"Loaded {len(templates)} templates")
                
                # Platform filter
                platforms = list(set([t.get('platform', 'YouTube') for t in templates]))
                selected_platform = st.selectbox("Filter by platform:", ["All"] + platforms)
                
                # Filter templates
                filtered_templates = templates
                if selected_platform != "All":
                    filtered_templates = [t for t in templates if t.get('platform') == selected_platform]
                
                # Display templates
                for i, template in enumerate(filtered_templates):
                    st.markdown(template_card_html(template, i), unsafe_allow_html=True)
                    
                    # Hidden buttons for Streamlit to capture clicks
                    if st.button("Preview", key=f"preview_btn_{i}", type="secondary", help="", args=None, kwargs=None):
                        st.session_state.show_preview_modal = True
                        st.session_state.preview_template = template
                        st.rerun()
                    
                    if st.button("Use Template", key=f"use_template_btn_{i}", type="secondary", help="", args=None, kwargs=None):
                        st.session_state.selected_template = template
                        st.session_state.template_params = map_template_to_form(template)
                        st.success(f"✅ Template loaded: {template['name']}")
                        st.rerun()

            # Display the preview modal if requested
            if st.session_state.show_preview_modal and st.session_state.preview_template:
                # Create an invisible form that can be submitted to close the modal
                # The form button MUST exist before the modal HTML references it
                with st.form(key="close_preview_modal_form", clear_on_submit=True):
                    # Create the submit button (will be hidden/triggered by JavaScript)
                    submitted = st.form_submit_button("Close Modal", key="close_modal_submit", help="", args=None, kwargs=None)
                    
                    # Display the modal INSIDE the form so it can reference the button
                    st.markdown(preview_modal(st.session_state.preview_template), unsafe_allow_html=True)
                    
                    # Check if form was submitted
                    if submitted:
                        st.session_state.show_preview_modal = False
                        st.rerun()

            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()