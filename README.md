# Web Scraping Assignment

This repository contains web scraping scripts for various e-commerce and book platforms using Selenium WebDriver.

## Tasks

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

## Requirements
- Python 3.x
- Selenium WebDriver
- Chrome WebDriver
- pandas
- numpy

## Setup
1. Install required Python packages:
```bash
pip install selenium pandas numpy
```

2. Download ChromeDriver matching your Chrome version

3. Place ChromeDriver in the project directory

## Running the Scripts
Each script can be run independently:
```bash
python L226639_3.py  # Amazon scraping
python L226639_4.py  # Daraz scraping
python L226639_5.py  # Goodreads scraping
```