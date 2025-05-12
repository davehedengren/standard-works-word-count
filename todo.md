# Project Todo List

## Phase 1: Data Acquisition and Preparation (Completed)

- [x] Find and download digital text of the Standard Works.
    - [x] Book of Mormon
    - [x] Old Testament
    - [x] New Testament
    - [x] Doctrine and Covenants
    - [x] Pearl of Great Price
- [x] Define a consistent structure for the text data (e.g., how to delineate books, chapters, verses).
- [x] Write a script (`data_processor.py`) to:
    - [x] Read the raw text files.
    - [x] Clean the text (e.g., remove verse numbers, chapter headings if necessary, handle punctuation, convert to lowercase).
    - [x] Tokenize the text into words for each book within each standard work.
    - [x] Count total words for each book and each standard work.
    - [x] Create a data structure (e.g., nested dictionary) mapping: `Standard Work -> Book -> Word -> Count`.
    - [x] Save the processed data structure to a file (e.g., JSON, Pickle) for fast loading by the Streamlit app.

## Phase 2: Streamlit Application Development (`app.py`)

- [x] Set up basic Streamlit app structure.
- [x] Load the pre-processed word count data.
- [x] Create UI elements:
    - [x] Text input for search term.
    - [x] Radio button/select box for choosing metric (raw counts vs. per 10,000 words).
    - [x] Radio button/select box for choosing display granularity:
        - [x] Summed across all works.
        - [x] Individual standard works.
        - [x] Individual books within standard works.
- [x] Implement search logic:
    - [x] Function to retrieve counts for the search term based on selected granularity and metric.
    - [x] Handle cases where the search term is not found.
    - [ ] Implement logic for phrase searching (multi-word strings).
- [x] Display results:
    - [x] Use `st.table` or `st.dataframe` to show frequency data.
    - [x] Implement calculations for "instances per 10,000 words".
- [ ] Add basic visualizations (e.g., bar charts using `st.bar_chart`).

## Phase 3: Refinements and Packaging

- [ ] Add error handling and input validation.
- [ ] Improve UI/UX (e.g., clear instructions, better layout, loading indicators).
- [ ] Write comprehensive docstrings and comments in the code.
- [x] Create `requirements.txt` with all necessary Python packages.
- [ ] Update `README.md` with final setup and usage instructions.
- [ ] Test thoroughly.

## Optional Enhancements

- [ ] Support case-sensitive and case-insensitive search.
- [ ] Allow regex searching.
- [ ] Lemmatization or stemming to count word variations (e.g., "run", "running", "ran" as the same word).
- [ ] Option to export search results (e.g., to CSV).
- [ ] More advanced visualizations. 