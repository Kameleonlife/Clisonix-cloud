#!/usr/bin/env python3
"""Quick test of YouTube API integration"""
import os
from googleapiclient.discovery import build

# Set API key
os.environ['YOUTUBE_API_KEY'] = 'AIzaSyDILX5WSVasL9CaBl8wtvQJlvD5MFzmIGc'

try:
    # Initialize YouTube API client
    youtube = build('youtube', 'v3', developerKey=os.environ['YOUTUBE_API_KEY'])
    
    # Test with a known video (Rick Astley - Never Gonna Give You Up)
    request = youtube.videos().list(
        part='snippet,statistics',
        id='dQw4w9WgXcQ'
    )
    response = request.execute()
    
    if response['items']:
        video = response['items'][0]
        print("✅ YouTube API CONNECTION SUCCESSFUL!\n")
        print(f"Title: {video['snippet']['title']}")
        print(f"Channel: {video['snippet']['channelTitle']}")
        print(f"Views: {int(video['statistics']['viewCount']):,}")
        print(f"Likes: {int(video['statistics']['likeCount']):,}")
        print(f"\n🎵 YouTube integration is ready!")
    else:
        print("⚠️ API works but no video found")
        
except Exception as e:
    print(f"❌ YouTube API Error: {e}")
    print("\nCheck:")
    print("1. API key is correct")
    print("2. YouTube Data API v3 is enabled")
    print("3. Quota not exceeded (10k requests/day)")

