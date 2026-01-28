# Quick Deployment to Streamlit Cloud

## Step 1: Push to GitHub

```bash
cd prompt-challenge
git init
git add .
git commit -m "Initial commit - AgriTrade Pro"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/prompt-challenge.git
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `prompt-challenge`
5. Set main file path: `app.py`
6. Click "Advanced settings"
7. Add environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: `your_gemini_api_key_here`
8. Click "Deploy"

## Step 3: Get Your Live URL

Your app will be available at:
`https://prompt-challenge-YOUR_USERNAME.streamlit.app`

## Alternative: Use Demo Mode

The app works without API key in demo mode with simulated responses.
Just deploy without setting GEMINI_API_KEY for a working demo.

## Troubleshooting

- If deployment fails, check the logs in Streamlit Cloud
- Ensure all dependencies are in requirements.txt
- Make sure app.py is in the root directory