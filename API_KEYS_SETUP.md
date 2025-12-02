# API Keys Setup Guide

## Quick Setup

API keys are read from a `.env` file in the project root. No interactive prompts!

### Step 1: Create .env File

Create a file named `.env` in the project root directory:

```bash
# In the project root
touch .env
```

### Step 2: Add Your API Keys

Edit the `.env` file and add your keys:

```bash
# OpenAI API Key (optional - only if you want to use OpenAI)
OPENAI_API_KEY=sk-your-openai-key-here

# Google Gemini API Key (optional - only if you want to use Gemini)
GEMINI_API_KEY=your-gemini-key-here
```

### Step 3: Get Your API Keys

- **OpenAI**: Get from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Gemini**: Get from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### Step 4: Use in Notebook

Just run the notebook cells - keys will be loaded automatically from `.env`!

## Important Notes

- ✅ The `.env` file is gitignored (won't be committed to git)
- ✅ You only need to set keys for providers you want to use
- ✅ Ollama doesn't need any keys (runs locally)
- ✅ If a key is missing, that provider will be skipped automatically

## Example .env File

```bash
# Only set the keys you want to use
OPENAI_API_KEY=sk-proj-abc123...
GEMINI_API_KEY=AIzaSy...
```

## Troubleshooting

**Keys not loading?**
- Make sure `.env` file is in the project root (same directory as `README.md`)
- Check that keys don't have quotes around them: `KEY=value` not `KEY="value"`
- Restart the Jupyter kernel after creating/editing `.env`

**Want to use environment variables instead?**
```bash
export OPENAI_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
```

