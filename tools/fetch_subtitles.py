#!/usr/bin/env python3
import sys
import os
import json
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_playlist_videos(playlist_url):
    print(f"Fetching playlist info for: {playlist_url}")
    # Run yt-dlp to get playlist video list in JSON format
    cmd = [
        "python3", "-m", "yt_dlp",
        "--flat-playlist",
        "--dump-single-json",
        playlist_url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        playlist_data = json.loads(result.stdout)
        
        videos = []
        # Support both 'entries' list structure
        entries = playlist_data.get("entries", [])
        for i, entry in enumerate(entries):
            if not entry:
                continue
            video_id = entry.get("id")
            title = entry.get("title")
            # If flat-playlist, upload_date might not be present, but let's check
            # Some versions return upload_date, others don't unless we request full extraction.
            # Flat extraction is fast, but let's see.
            videos.append({
                "index": i + 1,
                "id": video_id,
                "title": title,
            })
        return videos
    except Exception as e:
        print(f"Error fetching playlist details: {e}")
        # Fallback print stderr if subprocess failed
        if 'result' in locals() and result.stderr:
            print(f"yt-dlp stderr: {result.stderr}")
        sys.exit(1)

def format_timestamp(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def download_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        # Try getting English transcripts first, or default
        transcript_list = api.list(video_id)
        
        # Prefer English (manual or generated), then Korean, then whatever is first
        try:
            transcript = transcript_list.find_transcript(['en'])
        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_transcript(['ko'])
            except NoTranscriptFound:
                # Get the first available
                transcript = next(iter(transcript_list))
        
        data = transcript.fetch()
        return data, transcript.language
    except TranscriptsDisabled:
        print(f"Subtitles are disabled for video {video_id}.")
        return None, None
    except Exception as e:
        print(f"Could not retrieve transcript for video {video_id}: {e}")
        return None, None

def format_transcript_paragraphs(data, interval_seconds=60):
    if not data:
        return ""
    
    formatted_lines = []
    current_chunk = []
    
    def get_text_and_start(item):
        if isinstance(item, dict):
            return item.get('text', ''), item.get('start', 0.0)
        else:
            return getattr(item, 'text', ''), getattr(item, 'start', 0.0)

    first_text, first_start = get_text_and_start(data[0])
    current_start = first_start
    current_chunk.append(first_text.replace('\n', ' ').strip())
    
    for item in data[1:]:
        text, start = get_text_and_start(item)
        text = text.replace('\n', ' ').strip()
        # Group transcripts by interval_seconds (e.g. 60s)
        if start - current_start >= interval_seconds:
            timestamp = format_timestamp(current_start)
            paragraph = " ".join(current_chunk)
            formatted_lines.append(f"[{timestamp}] {paragraph}")
            current_chunk = [text]
            current_start = start
        else:
            current_chunk.append(text)
            
    if current_chunk:
        timestamp = format_timestamp(current_start)
        paragraph = " ".join(current_chunk)
        formatted_lines.append(f"[{timestamp}] {paragraph}")
        
    return "\n\n".join(formatted_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_subtitles.py <playlist_url>")
        sys.exit(1)
        
    playlist_url = sys.argv[1]
    
    # Create target directories
    os.makedirs("_raw_subtitles", exist_ok=True)
    
    videos = get_playlist_videos(playlist_url)
    print(f"Found {len(videos)} videos in the playlist.")
    
    manifest = []
    
    for video in videos:
        idx = video["index"]
        vid_id = video["id"]
        title = video["title"]
        print(f"[{idx}/{len(videos)}] Processing video: {title} ({vid_id})")
        
        data, lang = download_transcript(vid_id)
        if data:
            # Format transcript
            formatted_text = format_transcript_paragraphs(data)
            
            # Save raw subtitle file
            filename = f"_raw_subtitles/{idx:02d}_{vid_id}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(formatted_text)
            
            video["subtitle_file"] = filename
            video["language"] = lang
            print(f"  Saved subtitles to {filename} (Language: {lang})")
        else:
            video["subtitle_file"] = None
            video["language"] = None
            print(f"  No subtitles retrieved.")
            
        manifest.append(video)
        
    # Write manifest file
    manifest_path = "_raw_subtitles/manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Finished. Manifest saved to {manifest_path}")

if __name__ == "__main__":
    main()
