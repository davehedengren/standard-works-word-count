# Standard Works Word Count Analyzer

This project is a Streamlit application that allows users to search for the frequency of any string (word or phrase) across the standard works of The Church of Jesus Christ of Latter-day Saints:

*   Book of Mormon
*   New Testament
*   Old Testament
*   Doctrine and Covenants
*   Pearl of Great Price

## Features

*   **Search**: Users can input any string to search for.
*   **Frequency Metrics**:
    *   Display raw counts of the search term.
    *   Display instances per 10,000 words.
*   **Granularity**:
    *   View results summed across all standard works.
    *   View results for each standard work individually.
    *   View results for each book within each standard work (e.g., Genesis in the Old Testament, Alma in the Book of Mormon).
*   **Visualizations**: The app will present the data in tables and potentially charts for easier understanding.

## Project Goal

To provide a tool for analyzing word and phrase frequencies within the scriptures, facilitating study and research.

## Setup and Running

(Instructions to be added once the project structure is more defined, will include steps like:)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd standard-works-word-count
    ```
2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

## Data Source

The text for the standard works will be sourced from publicly available digital versions. The initial step involves downloading and processing these texts into a format suitable for fast querying by the Streamlit application. This will likely involve creating a pre-compiled data structure (e.g., a dictionary or JSON file) containing word counts for all books. 