"""
Processes raw scripture text from a JSON file to generate a structured dataset
containing word counts (both raw and lemmatized) for each book within each
standard work.

The input JSON file is expected to be an array of objects, where each object
represents a verse and contains at least 'volume_title', 'book_title', and
'scripture_text' keys.

The output is a JSON file ('processed_word_counts.json') that stores:
- Raw word frequencies for each book.
- Lemmatized word frequencies for each book.
- Total word counts for each book.
- Total word counts for each standard work.
- Overall total word count across all processed scriptures.

This pre-processed data is designed for fast loading and querying by the
Streamlit application.
"""
import json
import re
from collections import Counter, defaultdict

# Attempt to import NLTK and necessary components
try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    # NLTK Downloader is used to fetch resources
    # from nltk.downloader import Downloader # Not directly used, nltk.download is simpler

    NLTK_RESOURCES_OK = True

    def ensure_nltk_resource(resource_name, download_name):
        global NLTK_RESOURCES_OK
        try:
            nltk.data.find(resource_name)
            print(f"NLTK resource '{resource_name}' found.")
        except LookupError: # Catch LookupError when resource is not found
            print(f"NLTK resource '{resource_name}' not found. Attempting to download '{download_name}'...")
            try:
                nltk.download(download_name, quiet=True)
                print(f"NLTK resource '{download_name}' downloaded successfully.")
                # Verify after download
                nltk.data.find(resource_name)
            except Exception as e:
                print(f"Error downloading NLTK resource '{download_name}': {e}. Lemmatization might fail or be inaccurate.")
                NLTK_RESOURCES_OK = False
        except Exception as e:
            print(f"An unexpected error occurred while checking NLTK resource '{resource_name}': {e}")
            NLTK_RESOURCES_OK = False

    # Ensure necessary NLTK data is available
    ensure_nltk_resource('tokenizers/punkt', 'punkt')
    ensure_nltk_resource('corpora/wordnet', 'wordnet')
    
    if NLTK_RESOURCES_OK:
        lemmatizer = WordNetLemmatizer()
        print("NLTK Lemmatizer initialized.")
    else:
        print("NLTK resources not fully available. Lemmatization may be skipped or inaccurate.")
        lemmatizer = None
    NLTK_AVAILABLE = NLTK_RESOURCES_OK

except ImportError:
    print("NLTK library not found. Lemmatization will be skipped. Please install NLTK: pip install nltk")
    NLTK_AVAILABLE = False
    lemmatizer = None

# Define the standard works we are interested in.
RECOGNIZED_STANDARD_WORKS = [
    "Old Testament", "New Testament", "Book of Mormon",
    "Doctrine and Covenants", "Pearl of Great Price"
]
JSON_FILE_PATH = "data/lds-scriptures-2020.12.08/json/lds-scriptures-json.txt"
OUTPUT_FILE_PATH = "data/processed_word_counts.json"

def clean_and_tokenize_text(text: str) -> list[str]:
    """
    Cleans scripture text and tokenizes it into raw words.
    Process: lowercase, remove most punctuation (keeps intra-word apostrophes), splits into words.
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s']", '', text) 
    raw_words = text.split()
    return raw_words

def lemmatize_tokens(tokens: list[str]) -> list[str]:
    """
    Lemmatizes a list of word tokens if NLTK is available and lemmatizer is initialized.
    Uses WordNetLemmatizer with default POS (noun).
    Returns original tokens if NLTK is not available/setup failed or lemmatization itself fails.
    """
    if not NLTK_AVAILABLE or not lemmatizer:
        return tokens 
    try:
        lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized
    except Exception as e:
        print(f"Error during lemmatization of a token batch: {e}. Returning original tokens for this batch.")
        return tokens

def process_scriptures():
    """
    Reads scripture data, processes it, and counts raw and lemmatized
    word frequencies for each book within each standard work.
    """
    processed_data = {
        "standard_works": defaultdict(lambda: {
            "books": defaultdict(lambda: {
                "word_counts": Counter(), 
                "lemmatized_word_counts": Counter(),
                "total_words": 0
            }),
            "total_words_in_standard_work": 0
        }),
        "total_words_overall": 0
    }

    print(f"Starting processing of {JSON_FILE_PATH}...")
    if not NLTK_AVAILABLE:
        print("Note: NLTK not fully available or initialized. Lemmatized counts will be based on raw tokens or may be empty.")

    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            scripture_verses = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input JSON file not found at {JSON_FILE_PATH}.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_FILE_PATH}.")
        return

    print(f"Successfully loaded {len(scripture_verses)} verses.")

    for verse_data in scripture_verses:
        volume_title = verse_data.get("volume_title")
        book_title = verse_data.get("book_title")
        scripture_text = verse_data.get("scripture_text")

        if not (volume_title and book_title and scripture_text):
            continue
        if volume_title not in RECOGNIZED_STANDARD_WORKS:
            continue

        raw_words = clean_and_tokenize_text(scripture_text)
        num_words_in_verse = len(raw_words)
        
        lemmatized_words = lemmatize_tokens(raw_words) # Will return raw_words if lemmatization fails
        
        current_sw_data = processed_data["standard_works"][volume_title]
        current_book_data = current_sw_data["books"][book_title]

        current_book_data["word_counts"].update(raw_words)
        current_book_data["lemmatized_word_counts"].update(lemmatized_words) # Update regardless of NLTK status; content differs
        
        current_book_data["total_words"] += num_words_in_verse
        current_sw_data["total_words_in_standard_work"] += num_words_in_verse
        processed_data["total_words_overall"] += num_words_in_verse

    final_data_for_json = {
        "standard_works": {},
        "total_words_overall": processed_data["total_words_overall"]
    }
    for sw_name, sw_data in processed_data["standard_works"].items():
        final_data_for_json["standard_works"][sw_name] = {
            "books": {},
            "total_words_in_standard_work": sw_data["total_words_in_standard_work"]
        }
        for book_name, book_data in sw_data["books"].items():
            final_data_for_json["standard_works"][sw_name]["books"][book_name] = {
                "word_counts": dict(book_data["word_counts"]),
                "lemmatized_word_counts": dict(book_data["lemmatized_word_counts"]),
                "total_words": book_data["total_words"]
            }
    
    print(f"Finished processing. Processed data structure has {len(final_data_for_json['standard_works'])} standard works.")
    for sw_name, sw_info in final_data_for_json["standard_works"].items():
        book_count = len(sw_info['books'])
        print(f"  - {sw_name} (Total Words: {sw_info['total_words_in_standard_work']:,}, Books: {book_count})")

    try:
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as outfile:
            json.dump(final_data_for_json, outfile, indent=4)
        print(f"Successfully processed and saved data to {OUTPUT_FILE_PATH}")
    except IOError:
        print(f"Error: Could not write to output file {OUTPUT_FILE_PATH}.")

if __name__ == "__main__":
    process_scriptures() 