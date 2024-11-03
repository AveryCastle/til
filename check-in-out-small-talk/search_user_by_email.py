import os
from slack_bolt import App

# Install the Slack app and get xoxb- token in advance
SLACK_BOT_TOKEN=os.environ["CHEERY_MATE_SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["CHEERY_MATE_SLACK_APP_TOKEN"]
print(f"SLACK_BOT_TOKEN={SLACK_BOT_TOKEN}")
print(f"SLACK_APP_TOKEN={SLACK_APP_TOKEN}")

# Initialize the Slack app with your bot token
app = App(token=SLACK_BOT_TOKEN)


def get_user_id(email):
    """Fetches the Slack user ID based on the provided employee ID."""
    print(f"email = {email}")

    try:
        # Use the lookupByEmail method to find the user
        response = app.client.users_lookupByEmail(email=email)
        user_id = response['user']['id']  # Extract user ID from response
        return user_id
        
    except Exception as e:
        print(f"Error fetching user by email '{email}': {e}")
        return None


# Example usage
if __name__ == "__main__":
    email = "avery@gccompany.co.kr"
    user_id = get_user_id(email)
    
    if user_id:
        print(f"User ID for email '{email}': {user_id}")
    else:
        print("User not found.")
