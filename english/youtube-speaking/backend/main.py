from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# YouTube API Key
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.get("/api/quiz")
async def generate_quiz(channel_id: str = "UC_x5XG1OV2P6uZZ5FSM9Ttw"):
    # Fetch YouTube transcript
    video_id = get_latest_video_id(channel_id)
    transcript = get_transcript(video_id)
    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript not found.")

    # Generate Quiz using OpenAI
    prompt = f"Create a Korean-English quiz based on this transcript: {transcript[:1000]}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
    )
    quiz = response.choices[0].text.strip()
    return {"question": quiz.split("\n")[0], "answer": quiz.split("\n")[1]}

def get_latest_video_id(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?channelId={channel_id}&part=id&order=date&maxResults=1&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['items'][0]['id']['videoId']

def get_transcript(video_id):
    url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang=en"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.text
