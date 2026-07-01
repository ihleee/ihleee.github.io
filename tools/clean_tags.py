#!/usr/bin/env python3
import os
import re

def clean_tags():
    posts_dir = "_posts"
    if not os.path.exists(posts_dir):
        print(f"Directory not found: {posts_dir}")
        return
        
    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
            
        front_matter = parts[1]
        body = parts[2]
        
        # 1. Check inline tags format: tags: [tag1, tag2]
        match_inline = re.search(r'tags:\s*\[(.*?)\]', front_matter)
        if match_inline:
            tags_str = match_inline.group(1)
            tags = [t.strip().replace(" ", "-").replace("\"", "").replace("'", "") for t in tags_str.split(",")]
            new_tags_line = "tags:\n" + "\n".join([f"  - {t}" for t in tags if t])
            front_matter = front_matter.replace(match_inline.group(0), new_tags_line)
        else:
            # 2. Check block tags format: 
            # tags:
            #   - tag one
            #   - tag two
            tags_block_match = re.search(r'tags:\s*\n(\s*-\s*.*\n?)+', front_matter)
            if tags_block_match:
                block = tags_block_match.group(0)
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if line.strip().startswith("-"):
                        tag_val = line.split("-", 1)[1].strip()
                        tag_val_clean = tag_val.strip("\"'")
                        tag_val_hyphen = tag_val_clean.replace(" ", "-")
                        new_lines.append(f"  - {tag_val_hyphen}")
                    else:
                        new_lines.append(line)
                new_block = "\n".join(new_lines)
                front_matter = front_matter.replace(block, new_block)
                
        new_content = "---" + front_matter + "---" + body
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Cleaned tags for: {filename}")

if __name__ == "__main__":
    clean_tags()
