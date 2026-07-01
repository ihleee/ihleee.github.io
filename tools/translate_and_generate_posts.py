#!/usr/bin/env python3
import sys
import os
import json
import re
import time
from deep_translator import GoogleTranslator

def slugify(text):
    # Remove "Lasers & Optoelectronics Lecture X:"
    text = re.sub(r'^Lasers\s*&\s*Optoelectronics\s*Lecture\s*\d+\s*:\s*', '', text, flags=re.IGNORECASE)
    # Remove Cornell ECE part
    text = text.split("(Cornell")[0].strip()
    # Lowercase, replace spaces and non-word characters with hyphens
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def extract_tags(title):
    # Remove common prefix/suffix
    title_clean = title.replace("Lasers & Optoelectronics Lecture", "")
    title_clean = title_clean.split("(Cornell")[0]
    words = re.findall(r'[a-zA-Z]+', title_clean)
    
    # Filter out stopwords and short words
    stopwords = {
        'and', 'or', 'of', 'for', 'the', 'in', 'on', 'at', 'to', 'a', 'an', 'is', 'with', 
        'examples', 'design', 'designs', 'review', 'intro', 'basics', 'physics', 'summary', 'lecture'
    }
    filtered = []
    for w in words:
        w_lower = w.lower()
        if len(w_lower) > 2 and w_lower not in stopwords:
            filtered.append(w_lower)
            
    # Get unique words up to 3
    tags = []
    for w in filtered:
        if w not in tags:
            tags.append(w)
        if len(tags) == 3:
            break
            
    fallbacks = ['laser', 'optoelectronics', 'physics']
    for f in fallbacks:
        if len(tags) < 3 and f not in tags:
            tags.append(f)
            
    return tags

def translate_text(text, translator, retries=3):
    if not text.strip():
        return ""
    for attempt in range(retries):
        try:
            val = translator.translate(text)
            time.sleep(0.3)  # Sleep after a successful translation to be polite
            return val
        except Exception as e:
            print(f"  Error translating: {e}. Retrying {attempt+1}/{retries} after sleep...")
            time.sleep(5)
    return text

def main():
    manifest_path = "_raw_subtitles/manifest.json"
    if not os.path.exists(manifest_path):
        print(f"Manifest file not found: {manifest_path}")
        sys.exit(1)
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    os.makedirs("_subtitles_ko", exist_ok=True)
    os.makedirs("_posts", exist_ok=True)
    
    translator = GoogleTranslator(source='auto', target='ko')
    
    total_videos = len(manifest)
    print(f"Translating and generating blog posts for {total_videos} videos...")
    
    for video in manifest:
        idx = video["index"]
        vid_id = video["id"]
        title = video["title"]
        sub_file = video["subtitle_file"]
        
        if not sub_file or not os.path.exists(sub_file):
            print(f"[{idx}/{total_videos}] Skipping {title} (No subtitle file)")
            continue
            
        print(f"[{idx}/{total_videos}] Translating: {title}")
        
        # Read English subtitle file
        with open(sub_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        
        # Chunk paragraphs into blocks of up to 4000 characters
        chunks = []
        current_chunk = []
        current_length = 0
        for p in paragraphs:
            if current_length + len(p) + 2 > 4000:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [p]
                current_length = len(p)
            else:
                current_chunk.append(p)
                current_length += len(p) + 2
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
            
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            translated_chunk = translate_text(chunk, translator)
            translated_chunks.append(translated_chunk)
            time.sleep(0.5)
            
        translated_content = "\n\n".join(translated_chunks)
        
        # Save Korean subtitle file
        ko_sub_filename = f"_subtitles_ko/{idx:02d}_{vid_id}_ko.txt"
        with open(ko_sub_filename, "w", encoding="utf-8") as f:
            f.write(translated_content)
        print(f"  Saved translated subtitles to {ko_sub_filename}")
        
        # Generate Blog Post
        slug = slugify(title)
        post_filename = f"_posts/2026-07-01-lecture-{idx:02d}-{slug}.md"
        
        # Jekyll date format: YYYY-MM-DD HH:MM:SS +0900
        # Offset time by video index so they order chronologically
        post_date = f"2026-07-01 12:{idx:02d}:00 +0900"
        
        tags = extract_tags(title)
        
        # Jekyll Front Matter and content
        post_body = f"""---
title: "{title} (한글 번역)"
date: {post_date}
categories:
  - laser
tags:
  - {tags[0]}
  - {tags[1]}
  - {tags[2]}
---

유튜브 강의 영상 자막의 한글 번역본입니다.

### 강의 동영상

<iframe width="100%" height="400" src="https://www.youtube.com/embed/{vid_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

---

### 자막 번역 스크립트

"""
        # Append translated content to the post body
        post_body += translated_content + "\n\n"
            
        with open(post_filename, "w", encoding="utf-8") as f:
            f.write(post_body)
            
        print(f"  Generated blog post: {post_filename}")
        
        # Avoid hitting request limits
        time.sleep(1)

if __name__ == "__main__":
    main()
