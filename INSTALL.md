# ScriptForge Installation Guide

Complete step-by-step instructions to get ScriptForge running on your computer.

## 🖥️ System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Internet Connection**: Required for AI API calls

### Recommended Requirements
- **Python**: Version 3.10 or higher
- **RAM**: 8GB or more
- **Storage**: 1GB free space
- **Browser**: Chrome, Firefox, or Edge (latest version)

## 📦 Installation Methods

### Method 1: Quick Install (Recommended)

#### Windows
1. **Download Python** from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation
   
2. **Open Command Prompt** as Administrator
   ```cmd
   # Verify Python installation
   python --version
   
   # Install pip if not present
   python -m ensurepip --upgrade
   ```

3. **Install ScriptForge dependencies**
   ```cmd
   pip install streamlit requests python-docx python-dotenv
   ```

4. **Download ScriptForge** and extract to a folder

5. **Navigate to ScriptForge folder**
   ```cmd
   cd path\to\scriptforge
   ```

6. **Run the application**
   ```cmd
   streamlit run app.py
   ```

#### macOS
1. **Install Homebrew** (if not installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**
   ```bash
   brew install python
   ```

3. **Install dependencies**
   ```bash
   pip3 install streamlit requests python-docx python-dotenv
   ```

4. **Download and extract ScriptForge**

5. **Navigate to folder and run**
   ```bash
   cd ~/Downloads/scriptforge
   streamlit run app.py
   ```

#### Linux (Ubuntu/Debian)
1. **Update package list**
   ```bash
   sudo apt update
   ```

2. **Install Python and pip**
   ```bash
   sudo apt install python3 python3-pip
   ```

3. **Install dependencies**
   ```bash
   pip3 install streamlit requests python-docx python-dotenv
   ```

4. **Download and extract ScriptForge**

5. **Navigate and run**
   ```bash
   cd ~/Downloads/scriptforge
   streamlit run app.py
   ```

### Method 2: Using Virtual Environment (Advanced)

1. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔑 API Key Setup

### Getting Your API Key

#### Option A: DeepSeek API (Recommended - Free tier available)
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Click "Sign Up" and create an account
3. After login, go to "API Keys" in the sidebar
4. Click "Create New API Key"
5. Copy your key (keep it secure!)

#### Option B: Anthropic Claude API
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up for an account
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy your key

#### Option C: Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy your key

### Configuring Your API Key

1. **Create a `.env` file** in the ScriptForge folder
2. **Add your API key** (choose one provider):
   ```bash
   # For DeepSeek
   DEEPSEEK_API_KEY=your_key_here
   
   # For Anthropic
   ANTHROPIC_API_KEY=your_key_here
   
   # For Gemini
   GEMINI_API_KEY=your_key_here
   ```

3. **Save the file** - ScriptForge will automatically load it

## 🚀 First Run

1. **Start ScriptForge**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Enter your API key** in the sidebar

4. **Test with a simple topic** like "How to make coffee"

5. **Generate your first script!**

## ⚙️ Configuration Options

### Changing Default Settings
Edit `config.py` to customize:

```python
# Change default AI provider
DEFAULT_AI_PROVIDER = "deepseek"  # Options: "deepseek", "anthropic", "gemini"

# Enable/disable Pro features
ENABLE_PRO_FEATURES = True

# Change export directory
EXPORT_DIR = "my_scripts"
```

### Using Pro Features
1. **Get Brave Search API key** from [brave.com/search/api](https://brave.com/search/api/)
2. **Add to `.env` file**:
   ```bash
   BRAVE_API_KEY=your_brave_key_here
   ```
3. **Restart ScriptForge**

## 🔧 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Install dependencies
```bash
pip install streamlit requests python-docx python-dotenv
```

#### "API key not working"
**Solution**:
1. Verify your API key is correct
2. Check if you have credits/usage available
3. Try a different AI provider

#### "Streamlit won't open in browser"
**Solution**:
1. Check if port 8501 is in use
2. Manually open `http://localhost:8501`
3. Try a different browser

#### "Export not working"
**Solution**:
1. Ensure you have write permissions in the folder
2. Check if `python-docx` is installed for DOCX export
3. Look for error messages in the terminal

### Windows-Specific Issues

#### "Python not recognized"
**Solution**: Add Python to PATH
1. Search "Environment Variables" in Start Menu
2. Click "Environment Variables"
3. Under "System Variables", find "Path" and click Edit
4. Add Python installation path (e.g., `C:\Python39\`)

#### "Permission denied"
**Solution**: Run Command Prompt as Administrator

### macOS/Linux-Specific Issues

#### "Command not found: python3"
**Solution**: Install Python
```bash
# macOS
brew install python

# Ubuntu/Debian
sudo apt install python3
```

#### "Permission denied: venv"
**Solution**: Change permissions
```bash
chmod +x venv/bin/activate
```

## 📁 File Locations

### Default Locations
- **Scripts**: `exports/` folder in ScriptForge directory
- **Configuration**: `.env` file in ScriptForge directory
- **Logs**: Check terminal/command prompt output

### Changing Export Location
Edit `config.py`:
```python
EXPORT_DIR = "/path/to/your/preferred/location"
```

## 🔄 Updating ScriptForge

1. **Backup your `.env` file** and any custom scripts
2. **Download the latest version**
3. **Replace files** (except `.env`)
4. **Restart the application**

## 🆘 Getting Help

### Quick Fixes
1. **Restart ScriptForge**
2. **Clear browser cache**
3. **Check internet connection**
4. **Verify API key is valid**

### Additional Resources
- **README.md**: Basic usage and features
- **Example scripts**: Check `examples/` folder
- **Online documentation**: Visit the GitHub repository

### Contact Support
If issues persist:
1. **Check error messages** in terminal
2. **Take screenshot** of the problem
3. **Contact** through Gumroad or GitHub issues

## ✅ Verification Checklist

Before contacting support, verify:
- [ ] Python 3.8+ is installed
- [ ] Dependencies are installed (`pip list`)
- [ ] API key is in `.env` file
- [ ] `.env` file is in ScriptForge folder
- [ ] Port 8501 is not blocked
- [ ] Internet connection is working
- [ ] You have API credits/usage

---

**Need more help?** Check the README.md or contact the developer through your purchase platform.