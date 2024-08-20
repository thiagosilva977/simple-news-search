# simple-news-search-engine
## Overview
The simple-news-search-engine project is a tool designed to automate the process of collecting, parsing, and analyzing news data from various online sources. 

It uses a combination of web scraping (via BeautifulSoup), natural language processing (with SpaCy and SentenceTransformers), and machine learning techniques to extract, clean, and filter news articles based on specified search parameters. 

The project also includes capabilities for text embedding and similarity analysis, enabling the identification of relevant news articles according to specific topics and timeframes. Finally, the cleaned and filtered data is saved in an Excel file for further use.

- [Ideas and development draws](https://link.excalidraw.com/readonly/meFV9HK2aa13ySsz7IYg?darkMode=true)
  
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

#### Start the process
![image](https://github.com/user-attachments/assets/9f52b5ee-db00-497c-83e2-5fb801c15274)

*Example of custom input data*

#### Advanced Settings
You can Self-Host a worker with your own machine, to have fast processing while test.

![image](https://github.com/user-attachments/assets/65417b95-7155-41a3-9d39-4a893589ce06)

*Self host with your own machine*

See the [documentation here](https://robocorp.com/docs/courses/beginners-course-python/12-running-in-robocorp-cloud)


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
  - Need more testing and create a good dataset to see all the possibilities of data parsing.
  - It's possible to use LLMs to create synthetic tests (text_phrase)
- Add more options to filter data directly in websites
  - I skipped this part but it is easy to implement 
- Support more websites, specially that ones with anti-bot detection
  - We can use anticaptcha or imagetyperz to solve captchas.
  - More complex captchas need more time to develop, but it is not impossible.
  - Rotational proxies, managing better cookies, sometimes is enouth to some websites.
- Break the process in more steps
  - Better use of robocorp workitem
- Performance optimizations
   - Add parallelism
   - Isolate NLP tasks in different environments

## Time tracker

![image](https://github.com/user-attachments/assets/cb3186f4-e153-4064-9224-026c631187d9)









