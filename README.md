# Web Scraping Assignment

This repository contains web scraping solutions for various platforms using Selenium WebDriver and Jupyter notebooks.

## Tasks

### Task 1: Web Scraping Introduction
- Notebook: `L226639_1.ipynb`
- Features:
  - Basic web scraping concepts
  - HTML parsing techniques
  - Data extraction fundamentals
  - Introduction to Selenium WebDriver

### Task 2: Advanced Web Scraping
- Notebook: `L226639_2.ipynb`
- Features:
  - Advanced scraping techniques
  - Dynamic content handling
  - Error handling and retries
  - Data processing and storage

### Task 3: Amazon Product Search
- Script: `L226639_3.py`
- Features:
  - Searches for products on Amazon
  - Extracts product details including prices and ratings
  - Handles dynamic content loading

### Task 4: Daraz iPhone 15 Price Comparison
- Script: `L226639_4.py`
- Features:
  - Searches for iPhone 15 on Daraz
  - Compares prices across sellers
  - Extracts ratings and delivery options
  - Identifies best deals based on price and rating

### Task 5: Goodreads Book Recommendation
- Script: `L226639_5.py`
- Output: `goodreads_books.csv`
- Features:
  - Scrapes book details from multiple genres
  - Extracts titles, authors, ratings, and reviews
  - Compares average ratings across genres
  - Identifies highest-rated books in each category

## Project Documentation
- Report: `L226639_REPORT.pdf`
  - Detailed analysis of each task
  - Implementation approaches
  - Challenges and solutions
  - Results and conclusions

## Requirements
- Python 3.x
- Jupyter Notebook
- Selenium WebDriver
- Chrome WebDriver
- pandas
- numpy

## Setup
1. Install required Python packages:
```bash
pip install selenium pandas numpy jupyter
```

2. Download ChromeDriver matching your Chrome version

3. Place ChromeDriver in the project directory

## Running the Project
1. Jupyter Notebooks (Tasks 1 & 2):
```bash
jupyter notebook L226639_1.ipynb  # Task 1
jupyter notebook L226639_2.ipynb  # Task 2
```

2. Python Scripts (Tasks 3-5):
```bash
python L226639_3.py  # Amazon scraping
python L226639_4.py  # Daraz scraping
python L226639_5.py  # Goodreads scraping
```

## Project Structure
```
.
├── L226639_1.ipynb          # Task 1: Introduction notebook
├── L226639_2.ipynb          # Task 2: Advanced techniques notebook
├── L226639_3.py            # Task 3: Amazon scraping
├── L226639_4.py            # Task 4: Daraz scraping
├── L226639_5.py            # Task 5: Goodreads scraping
├── goodreads_books.csv     # Output data from Task 5
├── L226639_REPORT.pdf      # Project documentation
└── README.md               # Project overview
```