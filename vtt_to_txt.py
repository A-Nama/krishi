import re

def vtt_to_text(vtt_file, txt_file):
    with open(vtt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove timestamp lines & metadata
    text_lines = [line.strip() for line in lines if not re.match(r"^\d{2}:\d{2}", line) and line.strip() and not line.startswith("WEBVTT")]
    
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(" ".join(text_lines))

# Example usage:
vtt_to_text("video.vtt", "video.txt")
