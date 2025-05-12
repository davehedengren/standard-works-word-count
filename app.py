import streamlit as st
import json
import pandas as pd
# from collections import Counter # Counter is not explicitly used in app.py after data loading

# --- Page Config --- Must be the first Streamlit command ---
st.set_page_config(layout="wide")

DATA_FILE = "data/processed_word_counts.json"

@st.cache_data # Cache the data loading to improve performance
def load_data(file_path):
    """Loads the processed word count data from the JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(f"Error: Data file not found at {file_path}. Please run data_processor.py first.")
        return None
    except json.JSONDecodeError:
        st.error(f"Error: Could not decode JSON from {file_path}. The file might be corrupted.")
        return None

def get_search_results(search_term, data, granularity): # metric parameter removed for now
    """
    Processes the scripture data to find search term frequencies based on selected options.
    Returns a Pandas DataFrame with the results, including both raw and normalized counts.
    """
    results = []
    search_term_cleaned = search_term.lower().strip()
    if not search_term_cleaned:
        return pd.DataFrame()

    if granularity == "All Standard Works Combined":
        overall_raw_count = 0
        overall_total_words = data.get("total_words_overall", 0)

        for sw_name, sw_data in data["standard_works"].items():
            for book_name, book_data in sw_data["books"].items():
                overall_raw_count += book_data["word_counts"].get(search_term_cleaned, 0)
        
        normalized_count = (overall_raw_count / overall_total_words) * 10000 if overall_total_words > 0 else 0

        results.append({
            "Scope": "All Standard Works",
            "Search Term": search_term_cleaned,
            "Raw Count": overall_raw_count,
            "Per 10,000 Words": f"{normalized_count:.2f}",
            "Total Words in Scope": f"{overall_total_words:,}"
        })
        return pd.DataFrame(results)

    elif granularity == "By Standard Work":
        for sw_name, sw_data in data["standard_works"].items():
            sw_raw_count = 0
            sw_total_words = sw_data.get("total_words_in_standard_work", 0)
            for book_name, book_data in sw_data["books"].items():
                sw_raw_count += book_data["word_counts"].get(search_term_cleaned, 0)
            
            normalized_count = (sw_raw_count / sw_total_words) * 10000 if sw_total_words > 0 else 0
            
            results.append({
                "Standard Work": sw_name,
                "Search Term": search_term_cleaned,
                "Raw Count": sw_raw_count,
                "Per 10,000 Words": f"{normalized_count:.2f}",
                "Total Words in Standard Work": f"{sw_total_words:,}"
            })
        return pd.DataFrame(results)

    elif granularity == "By Book (within each Standard Work)":
        for sw_name, sw_data in data["standard_works"].items():
            for book_name, book_data in sw_data["books"].items():
                book_raw_count = book_data["word_counts"].get(search_term_cleaned, 0)
                book_total_words = book_data.get("total_words", 0)

                normalized_count = (book_raw_count / book_total_words) * 10000 if book_total_words > 0 else 0

                results.append({
                    "Standard Work": sw_name,
                    "Book": book_name,
                    "Search Term": search_term_cleaned,
                    "Raw Count": book_raw_count,
                    "Per 10,000 Words": f"{normalized_count:.2f}",
                    "Total Words in Book": f"{book_total_words:,}"
                })
        return pd.DataFrame(results)
    
    return pd.DataFrame()


# Load the data
scripture_data = load_data(DATA_FILE)

# --- Main App Title --- (Can come after page_config and data loading)
st.title("Standard Works Word/Phrase Frequency Analyzer")

if scripture_data:
    st.sidebar.header("Search Options")
    search_term_input = st.sidebar.text_input("Enter word or phrase to search:", "faith")

    # The metric_type is kept for now, though not used to select columns for display in the table
    metric_options = {
        "Raw Counts": "raw",
        "Instances per 10,000 Words": "normalized" 
    }
    selected_metric_display = st.sidebar.radio(
        "Display Metric (Currently informational, both shown in table):", # Clarified label
        options=list(metric_options.keys()),
        index=0
    )
    metric_type = metric_options[selected_metric_display]

    granularity_options = [
        "All Standard Works Combined", 
        "By Standard Work", 
        "By Book (within each Standard Work)"
    ]
    
    selected_granularity = st.sidebar.selectbox(
        "Select Granularity:",
        options=granularity_options,
        index=0
    )

    st.markdown("--- ")
    st.header("Search Results")

    if not search_term_input.strip():
        st.warning("Please enter a search term.")
    else:
        # Displaying search info (metric_type here is just informational from the radio button)
        st.write(f"Searching for: **'{search_term_input.strip().lower()}'**")
        st.write(f"Selected Metric Focus: **{selected_metric_display}**") 
        st.write(f"Granularity: **{selected_granularity}**")
        
        df_results = get_search_results(search_term_input, scripture_data, selected_granularity)

        if not df_results.empty:
            st.dataframe(df_results, use_container_width=True) # Display all columns from df_results
        else:
            if search_term_input.strip():
                st.info(f"The term '{search_term_input.strip().lower()}' was not found or resulted in no data for the selected options.")

else:
    st.error("Failed to load scripture data. Please check the data file and try again.")

# To run the app: streamlit run app.py 