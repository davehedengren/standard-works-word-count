import json
import re
from collections import Counter, defaultdict

# Define the standard works we are interested in and their mapping from volume_title
# We'll use the volume_title directly from the JSON as keys if they are consistent.
# Standard Works: Book of Mormon, New Testament, Old Testament, Doctrine and Covenants, Pearl of Great Price.

# Path to the JSON data file
JSON_FILE_PATH = "data/lds-scriptures-2020.12.08/json/lds-scriptures-json.txt"
OUTPUT_FILE_PATH = "data/processed_word_counts.json"

def clean_text(text):
    """Converts text to lowercase and removes punctuation, keeping only words."""
    text = text.lower()
    text = re.sub(r"[^a-z\s']", '', text) # Keep apostrophes for contractions/possessives
    words = text.split()
    return words

def process_scriptures():
    """
    Reads scripture data from the JSON file, processes it, and counts word frequencies
    for each book within each standard work. Also counts total words per book.
    """
    # Structure:
    # {
    #   "Standard Work Name": {
    #     "Book Name": {
    #       "words": Counter_object_for_word_counts,
    #       "total_words": integer_total_word_count_for_book
    #     },
    #     ... (other books) ...
    #     "total_words_in_standard_work": integer_total_word_count_for_standard_work
    #   },
    #   ... (other standard works) ...
    #   "total_words_overall": integer_total_word_count_for_all_scriptures
    # }
    # Using defaultdict for easier nested dictionary creation.

    # Revised structure for easier JSON serialization with Counter
    processed_data = {
        "standard_works": defaultdict(lambda: {
            "books": defaultdict(lambda: {"word_counts": Counter(), "total_words": 0}),
            "total_words_in_standard_work": 0
        }),
        "total_words_overall": 0
    }

    print(f"Starting processing of {JSON_FILE_PATH}...")

    # Define the recognized standard works based on typical volume_title values
    # (These might need adjustment based on actual data in lds-scriptures-json.txt)
    recognized_standard_works = [
        "Old Testament",
        "New Testament",
        "Book of Mormon",
        "Doctrine and Covenants",
        "Pearl of Great Price"
    ]

    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            scripture_verses = json.load(f) # Load the entire JSON array
    except FileNotFoundError:
        print(f"Error: JSON file not found at {JSON_FILE_PATH}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_FILE_PATH}")
        return

    print(f"Successfully loaded {len(scripture_verses)} verses.")

    for verse_data in scripture_verses:
        volume_title = verse_data.get("volume_title")
        book_title = verse_data.get("book_title")
        scripture_text = verse_data.get("scripture_text")

        if not (volume_title and book_title and scripture_text):
            # Skip if essential data is missing
            continue

        # Normalize standard work names if necessary, or ensure they are in our list
        if volume_title not in recognized_standard_works:
            # This helps identify if there are other "volumes" we need to handle or ignore
            # print(f"Skipping unrecognized volume: {volume_title}")
            continue

        words = clean_text(scripture_text)
        num_words = len(words)

        # Update counts
        current_sw = processed_data["standard_works"][volume_title]
        current_book = current_sw["books"][book_title]

        current_book["word_counts"].update(words)
        current_book["total_words"] += num_words
        current_sw["total_words_in_standard_work"] += num_words
        processed_data["total_words_overall"] += num_words

    # Convert Counter objects to plain dicts for JSON serialization if needed,
    # but json.dump can handle Counter objects if they are first converted to dicts.
    # For this structure, we'll convert them explicitly.
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
                "word_counts": dict(book_data["word_counts"]), # Convert Counter to dict
                "total_words": book_data["total_words"]
            }
    
    print(f"Processed data structure has {len(final_data_for_json['standard_works'])} standard works.")
    for sw_name, sw_info in final_data_for_json["standard_works"].items():
        print(f"  - {sw_name} ({sw_info['total_words_in_standard_work']} words, {len(sw_info['books'])} books)")


    try:
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as outfile:
            json.dump(final_data_for_json, outfile, indent=4)
        print(f"Successfully processed and saved data to {OUTPUT_FILE_PATH}")
    except IOError:
        print(f"Error: Could not write to output file {OUTPUT_FILE_PATH}")

if __name__ == "__main__":
    process_scriptures() 