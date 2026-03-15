# ScriptForge: AI-Powered Video Script Generator

![ScriptForge Banner](https://via.placeholder.com/800x200/FF4B4B/FFFFFF?text=ScriptForge+AI+Video+Script+Generator)

**Transform your ideas into engaging YouTube & TikTok scripts with AI-powered assistance.**

## 🎬 What is ScriptForge?

ScriptForge is a local Streamlit web application that helps content creators generate professional video scripts for YouTube, TikTok, Instagram Reels, and LinkedIn. Simply provide a topic, choose your parameters, and let AI craft a complete, ready-to-use script in seconds.

## ✨ Features

### 🚀 Core Features
- **AI-Powered Script Generation**: Generate scripts using DeepSeek, Anthropic Claude, or Google Gemini
- **Multiple Platforms**: Support for YouTube, TikTok, Instagram Reels, and LinkedIn Video
- **Customizable Parameters**: Control tone, length, audience, and format
- **Export Options**: Save scripts as TXT, DOCX, or JSON files
- **Template System**: Quick-start with pre-built templates for common video formats
- **No Subscriptions**: One-time purchase, runs locally on your computer

### 🔍 Pro Features (Optional)
- **Trend Analysis**: Integrate with Brave Search to analyze trending topics
- **Competition Analysis**: Get insights on search competition for your topics
- **Content Angle Suggestions**: AI-powered suggestions for unique content angles
- **Batch Generation**: Generate multiple scripts at once

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- An AI API key (DeepSeek, Anthropic, or Gemini)
- Internet connection (for API calls)

### Quick Start

1. **Clone or download** the ScriptForge package
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   Create a `.env` file in the scriptforge directory:
   ```bash
   DEEPSEEK_API_KEY=your_api_key_here
   # OR
   ANTHROPIC_API_KEY=your_api_key_here
   # OR  
   GEMINI_API_KEY=your_api_key_here
   
   # Optional: For Pro features
   BRAVE_API_KEY=your_brave_search_api_key
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📖 Usage Guide

### Basic Script Generation
1. **Enter your API key** in the sidebar
2. **Choose your video platform** (YouTube, TikTok, etc.)
3. **Select video format** (Explainer, Review, Tutorial, etc.)
4. **Enter your topic** in the main text area
5. **Adjust parameters** (tone, length, audience)
6. **Click "Generate Script"** and watch the magic happen!

### Exporting Scripts
- **Copy to Clipboard**: One-click copy for quick pasting
- **Download as TXT**: Plain text format for any text editor
- **Download as DOCX**: Microsoft Word format with formatting
- **Download as JSON**: Structured data for developers

### Using Templates
Click on any template in the "Quick Templates" section to instantly populate the script area with a structured template that you can customize.

## 🎯 Supported Video Formats

### YouTube
- Explainer/Tutorial
- Product Review  
- Vlog/Storytime
- List/Countdown
- Interview
- Educational

### TikTok & Short-Form
- Quick Tip
- Trend/Challenge
- Behind the Scenes
- Product Showcase
- Question/Answer
- Entertainment

## 🔧 Configuration

### AI Providers
ScriptForge supports multiple AI providers. Configure your preferred provider in `config.py`:

```python
DEFAULT_AI_PROVIDER = "deepseek"  # Options: "deepseek", "anthropic", "gemini"
```

### Pro Features
Enable or disable pro features in `config.py`:
```python
ENABLE_PRO_FEATURES = True  # Set to False for basic version
```

## 📁 Project Structure

```
scriptforge/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── INSTALL.md            # Detailed installation guide
├── LICENSE               # MIT License
├── utils/                # Utility modules
│   ├── ai.py            # AI script generation
│   ├── export.py        # Export functionality
│   └── search.py        # Brave Search integration (Pro)
├── templates/            # Script templates
├── examples/             # Example scripts
└── exports/              # Generated export files
```

## 🚀 Getting an API Key

### DeepSeek API
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key

### Anthropic Claude API
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up for an account
3. Generate an API key

### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Create an API key

### Brave Search API (Optional for Pro)
1. Visit [Brave Search API](https://brave.com/search/api/)
2. Sign up for an account
3. Generate an API key

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** by opening an issue
2. **Suggest features** in the issues section
3. **Submit pull requests** with improvements
4. **Share your scripts** in the examples folder

### Development Setup
```bash
# Clone the repository
git clone [repository-url]

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
pytest

# Format code
black .
```

## 📄 License

ScriptForge is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [DeepSeek](https://www.deepseek.com/), [Anthropic Claude](https://www.anthropic.com/), and [Google Gemini](https://deepmind.google/technologies/gemini/)
- Search integration with [Brave Search API](https://brave.com/search/api/)
- Icons from [Font Awesome](https://fontawesome.com/)

## 📞 Support

Having issues or questions?

1. **Check the [INSTALL.md](INSTALL.md)** for troubleshooting
2. **Review open issues** on GitHub
3. **Contact support** through Gumroad if purchased there

---

**Happy Scripting! 🎬**