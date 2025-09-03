import os
import json
import re
import fitz  # PyMuPDF library
import pandas as pd
import google.generativeai as genai


# 1. Add your API keys. It's best to use environment variables.
GOOGLE_API_KEY = "AIzaSyCac-5W_VqQkL6oQXWHsanGsRFOx_pDz0U"
#SARVAM_SUBSCRIPTION_KEY = "sk_9hc0hr0e_aoZkMmGP0CsmmIdZvY4m0Ias"

# 2. Add the path to your PDF file.
PDF_FILE_PATH = "Fruit crops-2.pdf"

# 3. Choose a name for your final dataset file.
OUTPUT_CSV_PATH = "malayalam_agri_dataset14.csv"

# --- FUNCTION DEFINITIONS ---------------------------------------------------

def extract_text_from_pdf(pdf_path):
    """Opens a PDF and extracts all its text content."""
    print(f"📄 Extracting text from '{pdf_path}'...")
    try:
        doc = fitz.open(pdf_path)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        print("   ✅ Text extracted successfully.")
        return text
    except Exception as e:
        print(f"   ❌ ERROR: Could not read PDF file. {e}")
        return None

def clean_text(text):
    """A simple function to clean text by removing non-standard characters."""
    if not text: return ""
    return re.sub(r'[^\w\s.,!?-]', ' ', text).strip()

# ✨ --- MISSING FUNCTION RESTORED --- ✨
def split_into_chunks(text, chunk_size):
    """Splits a large text into smaller chunks under the character limit."""
    if not text: return []
    paragraphs = text.split('\n')
    chunks, current_chunk = [], ""
    for p in paragraphs:
        if len(current_chunk) + len(p) + 1 > chunk_size:
            if current_chunk: chunks.append(current_chunk)
            current_chunk = p
        else:
            if current_chunk: current_chunk += "\n" + p
            else: current_chunk = p
    if current_chunk: chunks.append(current_chunk)
    return chunks

def save_to_csv(data_list, filename):
    """Saves the final data to a two-column CSV."""
    if not data_list:
        print("No data to save.")
        return
    print(f"💾 Saving data to '{filename}'...")
    try:
        df = pd.DataFrame(data_list)
        final_df = df[['title', 'malayalam_content']]
        final_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"   ✨ Success! Your dataset is ready.")
    except KeyError:
        print("   ❌ CRITICAL ERROR: Could not create CSV. The 'title' or 'malayalam_content' key was likely missing in the data from Gemini.")

# --- GEMINI AI FUNCTIONS ------------------------------------------------------

def get_topics_from_gemini(text_content, model):
    """Uses the Gemini API to split text into topics in a JSON format."""
    print("🧠 Splitting text into topics using Gemini...")
    try:
        prompt = f"""
        You are a data processing engine. Your only task is to parse the following text and structure it.
        Analyze the agricultural text below. Identify all distinct topics.
        Your output MUST be a valid JSON array. Each element of the array MUST be a JSON object.
        Each JSON object MUST contain exactly two string keys: "topic" and "content".
        Do NOT add any commentary or text outside of the single JSON array.

        Text to process: --- {text_content} ---
        """
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().lstrip("```json").rstrip("```").strip()
        print("   ✅ Topics identified by Gemini.")
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"   ❌ ERROR: Failed to parse Gemini's topic response. It might not be valid JSON. Error: {e}")
        return None

def translate_with_gemini(text_to_translate, model):
    """Translates English text to Malayalam using the Gemini API."""
    if not text_to_translate or not text_to_translate.strip():
        return ""
    
    prompt = f'Translate the following English text into professional, academic Malayalam. Return only the translated Malayalam text and nothing else.\n\nEnglish Text: "{text_to_translate}"'
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"       ERROR during Gemini translation: {e}")
        return "Gemini Translation Error"

# --- MAIN EXECUTION SCRIPT --------------------------------------------------

def main():
    """Main function to run the entire data processing pipeline."""
    print("🚀 Starting Agricultural Data Processing Pipeline (using Gemini only)...")
    
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-pro')
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Could not configure Gemini. Check your API Key. Error: {e}")
        return

    full_text = extract_text_from_pdf(PDF_FILE_PATH)
    if not full_text: return

    topics = get_topics_from_gemini(full_text, model)
    if not topics: return

    print(f"🗣️ Translating {len(topics)} topic(s) to Malayalam using Gemini...")
    final_dataset = []
    for i, topic_data in enumerate(topics):
        if not isinstance(topic_data, dict):
            print(f"   ⚠️ WARNING: Skipping item #{i+1} from Gemini's output because it was not formatted correctly.")
            continue

        topic_title = topic_data.get("topic", f"Untitled Topic #{i+1}")
        english_content = topic_data.get("content", "")
        
        print(f"\n   - Processing topic {i+1}/{len(topics)}: '{topic_title[:60]}...'")
        
        cleaned_content = clean_text(english_content)
        
        content_chunks = split_into_chunks(cleaned_content, chunk_size=8000)
        translated_chunks = []
        
        if not content_chunks:
            print("     (Topic has no content to translate)")
        else:
            for j, chunk in enumerate(content_chunks):
                print(f"       > Translating chunk {j+1}/{len(content_chunks)}...")
                translated_chunk = translate_with_gemini(chunk, model)
                if "Error" in translated_chunk:
                    print(f"       ❌ Error translating chunk.")
                    translated_chunks.append(f"[Chunk {j+1} Failed]")
                else:
                    translated_chunks.append(translated_chunk)

        full_malayalam_content = "\n\n".join(translated_chunks)
        
        final_dataset.append({
            "title": topic_title,
            "malayalam_content": full_malayalam_content
        })

    save_to_csv(final_dataset, OUTPUT_CSV_PATH)

if __name__ == "__main__":
    main()