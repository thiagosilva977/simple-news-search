# simple-news-search-engine
## Overview
The simple-news-search-engine project is a tool designed to automate the process of collecting, parsing, and analyzing news data from various online sources. 

It uses a combination of web scraping (via BeautifulSoup), natural language processing (with SpaCy and SentenceTransformers), and machine learning techniques to extract, clean, and filter news articles based on specified search parameters. 

The project also includes capabilities for text embedding and similarity analysis, enabling the identification of relevant news articles according to specific topics and timeframes. Finally, the cleaned and filtered data is saved in an Excel file for further use.

![image](https://github.com/user-attachments/assets/a5a31c2d-2109-49b1-93dd-801c4eb0bcf7)
*Robocorp dashboard to initialize automation process*

![image](https://github.com/user-attachments/assets/87345b6d-e9cc-48b8-80c8-8d9de85e66db)
*System Design*


## Features
- **Robocorp Integration:** Run workflows in Robocorp workspace. 
- **News Search:** Automatically searches for news articles based on a text phrase across multiple online sources.
- **HTML Content Extraction:** Retrieves and parses HTML content from the listed news URLs.
- **Data Normalization:** Cleans and normalizes extracted data, including text, dates, and authors.
- **Text Embedding & Similarity Calculation:** Generates embeddings for news content and calculates cosine similarity to filter relevant articles.
- **Monetary Information Detection:** Identifies articles containing monetary information based on common currency symbols and keywords.
- **Image Downloading:** Downloads images associated with news articles and saves them locally.
- **Date Filtering:** Filters articles based on their publication date, allowing for time-bound searches.
- **Data Export:** Saves the final filtered and normalized data into an Excel file.

## Installation

To run this tool, you'll need Python installed along with the following dependencies:

```bash
pip install .
```

## Usage

### Initialization

The tool can be initialized using two main functions depending on the desired step in the extraction process.


### Local Execution

To execute the full process in one go, simply run the script: <pre>python -m run news_data_extractor/source/main.py </pre>

### Robocorp execution

To execute the full process in one go, simply run in the dashboard:


### Configuration
- **Search Parameters:** Defined during class initialization or passed to the functions. Includes
   - `text_phrase`:str
   - `news_category`:str
   - `max_months`:int.

### Logging

The tool generates log files (`my_log.log`) capturing detailed information about the extraction process, including warnings and errors.

### Output

The final output is saved as an Excel file (`results.xlsx`) in the `output` directory located at the root of the project.

## Next Steps

- Fix parsing errors
- Add more options to filter data directly in websites
- Support more websites, specially that ones with anti-bot detection
- Break the process in more steps
- Performance optimizations
   - Add parallelism
   - Isolate NLP tasks in different environments









