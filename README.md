# DeadBoot - Virtual Numbers Bot

Telegram bot for selling virtual phone numbers based on real SIM cards.

## Deployment on Railway via GitHub

### Step 1: Push to GitHub

1. Open GitHub Desktop
2. Click "Fetch origin" to get the latest changes
3. Click "Commit to main" to commit your changes
4. Click "Push origin" to push to GitHub

### Step 2: Set up Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect it's a Python project

### Step 3: Add Environment Variables

In Railway project settings, add these environment variables:

- `BOT_TOKEN` - Your Telegram bot token from @BotFather
- `ADMIN_ID` - Your Telegram user ID (default: 7846160465)

### Step 4: Deploy

1. Click "Deploy" in Railway
2. Railway will automatically build and deploy your bot
3. Future pushes to GitHub will trigger automatic deployments

### Local Development

Create a `.env` file in the project root:

```
BOT_TOKEN=your_bot_token_here
ADMIN_ID=7846160465
```

Then run:

```bash
pip install -r requirements.txt
python bot.py
```

## Project Structure

- `bot.py` - Main bot file
- `requirements.txt` - Python dependencies
- `Procfile` - Railway deployment configuration
- `railway.json` - Railway project configuration
- `.gitignore` - Git ignore rules
