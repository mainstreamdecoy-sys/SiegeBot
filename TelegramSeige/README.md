# This file was previously named replit.md
# It is not required for Heroku or most production deployments.
# If you want to keep deployment notes, rename this file to README.md.

# HarleyBot Deployment Notes

- For Heroku, ensure you have a `Procfile` with:
  web: python main.py
- All dependencies should be listed in requirements.txt
- Environment variables should be set in Heroku config vars

# Usage
- Run locally: `python main.py`
- Deploy to Heroku: Push to Heroku Git and scale dynos

# Remove or rename this file if not needed.
