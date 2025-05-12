# Standard Works Word Count Analyzer

This project is a Streamlit application that allows users to search for the frequency of any word or phrase across the standard works of The Church of Jesus Christ of Latter-day Saints:

*   Book of Mormon
*   New Testament
*   Old Testament
*   Doctrine and Covenants
*   Pearl of Great Price

## Features

*   **Search**: Users can input any word or phrase to search for (case-insensitive, exact match).
*   **Frequency Metrics Displayed in Table**:
    *   Raw count of the search term.
    *   Instances per 10,000 words (formatted to two decimal places).
    *   Total words in the searched scope.
*   **Granularity Options**:
    *   View results summed across all standard works.
    *   View results for each standard work individually.
    *   View results for each book within each standard work (e.g., Genesis in the Old Testament, Alma in the Book of Mormon).
*   **Visualization**:
    *   A bar chart displaying instances per 10,000 words, ranked in descending order.

## Project Goal

To provide a tool for analyzing word and phrase frequencies within the scriptures, facilitating study and research.

## Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/davehedengren/standard-works-word-count.git
    cd standard-works-word-count
    ```

2.  **Create a virtual environment and install dependencies:**
    It is highly recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Prepare the Data:**
    The application relies on a pre-processed JSON file containing word counts. To generate this file, you first need the raw scripture text. The `data_processor.py` script handles downloading and processing.

    *   **Download Raw Data (if not already present):**
        The `data_processor.py` script will attempt to use the raw scripture data from `data/lds-scriptures-2020.12.08/json/lds-scriptures-json.txt`.
        If this file is missing (e.g., after a fresh clone where only `data/processed_word_counts.json` might be committed), you would typically need to re-acquire the source data. For this project, the initial setup involved:
        ```bash
        mkdir -p data
        curl -L -o data/lds-scriptures.zip https://github.com/beandog/lds-scriptures/archive/2020.12.08.zip
        unzip data/lds-scriptures.zip -d data/
        # This creates data/lds-scriptures-2020.12.08/ which contains the json/lds-scriptures-json.txt
        ```
        *Note: For simplicity in a cloned environment that might already have `processed_word_counts.json`, these manual download steps for the *raw* data might not be strictly necessary unless you intend to re-process.*

    *   **Run the data processing script:**
        This script reads the raw scripture data (from `data/lds-scriptures-2020.12.08/json/lds-scriptures-json.txt`), cleans it, counts word frequencies, and saves the output to `data/processed_word_counts.json`.
        ```bash
        python data_processor.py
        ```
        Ensure `data/lds-scriptures-2020.12.08/json/lds-scriptures-json.txt` exists before running this, or modify the script if using a different source.

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser.

## Usage

1.  **Enter Search Term**: In the sidebar, type the word or phrase you want to search for in the "Enter word or phrase to search:" text box.
2.  **Select Granularity**: Choose how you want the results to be grouped:
    *   "All Standard Works Combined"
    *   "By Standard Work" (Default)
    *   "By Book (within each Standard Work)"
3.  **View Results**:
    *   The main panel will display a table with the search term, raw count, instances per 10,000 words, and total words for the selected scope.
    *   Below the table, a bar chart will show the instances per 10,000 words, ranked.
4.  **Search Behavior**: The search is case-insensitive and looks for exact matches of the entered word or phrase. For example, searching for "faith" will not find "faithful".

## Data Source

The primary text data is sourced from the [lds-scriptures dataset by beandog (version 2020.12.08)](https://github.com/beandog/lds-scriptures/tree/2020.12.08), specifically the `lds-scriptures-json.txt` file. The `data_processor.py` script processes this JSON file to create a structured word count file (`data/processed_word_counts.json`) which the Streamlit app uses for fast lookups. 