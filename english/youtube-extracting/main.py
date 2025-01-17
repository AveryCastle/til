import os
from youtube_transcript_api import YouTubeTranscriptApi

def extract_unique_sentences(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    unique_sentences = []
    seen_sentences = set()
    
    for entry in transcript:
        sentence = entry['text'].strip()
        # 문장이 비어있지 않고, 이전에 보지 않은 경우에만 추가
        if sentence and sentence not in seen_sentences:
            unique_sentences.append(sentence)
            seen_sentences.add(sentence)
    
    return unique_sentences

# YouTube URL의 video_id 부분
video_id = "aaWj4oTUwKY"

unique_sentences = extract_unique_sentences(video_id)

print("고유한 문장들:")
for i, sentence in enumerate(unique_sentences, 1):
    print(f"{i}. {sentence}")
