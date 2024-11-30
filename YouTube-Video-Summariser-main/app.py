from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, VideoUnavailable
from transformers import pipeline
import re

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    # Hardcode your YouTube URL here for testing
    url = "https://youtu.be/nyhRNwTfydU?si=f39AMKnLEP8hPwa7"  # Your YouTube video URL
    video_id = extract_video_id(url)
    
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400
    
    try:
        transcript = get_transcript(video_id)
        summary = get_summary(transcript)
        return jsonify({"summary": summary}), 200
    except VideoUnavailable:
        return jsonify({"error": "Transcript not available for this video"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_video_id(url):
    # Regex pattern to match YouTube video ID in different URL formats
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+|(?:v|e(?:mbed)?)\/|(?:.*[?&]v=))|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    summarizer = pipeline('summarization')
    summary = ''
    
    # Summarizing in chunks of 1000 characters to avoid tokenizer length limit
    for i in range(0, len(transcript), 1000):
        chunk = transcript[i:i+1000]
        summary_text = summarizer(chunk)[0]['summary_text']
        summary += summary_text + ' '
    return summary

if __name__ == '__main__':
    app.run(debug=True)
