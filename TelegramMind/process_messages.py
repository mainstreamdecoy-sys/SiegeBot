#!/usr/bin/env python3
"""Process pending Telegram messages"""

import os
import requests
import json

# Get updates and respond to them
def process_pending_messages():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    api_url = f"https://api.telegram.org/bot{token}"
    
    # Get pending updates
    response = requests.get(f"{api_url}/getUpdates")
    data = response.json()
    
    if not data.get('ok'):
        print(f"Error getting updates: {data}")
        return
    
    updates = data.get('result', [])
    print(f"Found {len(updates)} pending updates")
    
    for update in updates:
        try:
            # Process each update by sending to our local webhook
            webhook_response = requests.post('http://localhost:5000/webhook', 
                                           json=update, 
                                           headers={'Content-Type': 'application/json'})
            print(f"Processed update {update['update_id']}: {webhook_response.status_code}")
            
            # Mark as processed
            requests.get(f"{api_url}/getUpdates", params={'offset': update['update_id'] + 1})
            
        except Exception as e:
            print(f"Error processing update {update.get('update_id')}: {e}")

if __name__ == "__main__":
    process_pending_messages()