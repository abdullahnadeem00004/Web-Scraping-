from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")
drv = webdriver.Chrome(options=opt)
waiter = WebDriverWait(drv, 10)

root = "https://www.goodreads.com"

def grab_book(link):
    drv.get(link)
    time.sleep(2)

    try:
        ttl = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[data-testid="bookTitle"]'))).text
    except:
        ttl = "Not Available"

    try:
        auth = drv.find_element(By.CSS_SELECTOR, 'span[data-testid="name"]').text
    except:
        auth = "Not Available"

    try:
        rate = drv.find_element(By.CSS_SELECTOR, 'div.RatingStatistics__rating').text
    except:
        rate = "Not Available"

    try:
        revs = drv.find_element(By.CSS_SELECTOR, 'span[data-testid="reviewsCount"]').text
    except:
        revs = "Not Available"

    try:
        pub = drv.find_element(By.CSS_SELECTOR, 'p[data-testid="publicationInfo"]').text
    except:
        pub = "Not Available"

    return {
        "Title": ttl,
        "Author": auth,
        "Rating": rate,
        "Reviews": revs,
        "Publication Date": pub,
        "URL": link
    }

def grab_genre(cat, lim=10):
    print(f"\nCollecting genre: {cat}")
    drv.get(f"{root}/genres/{cat}")
    time.sleep(3)

    prev = drv.execute_script("return document.body.scrollHeight")
    for _ in range(5):
        drv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new = drv.execute_script("return document.body.scrollHeight")
        if new == prev:
            break
        prev = new

    items = drv.find_elements(By.CSS_SELECTOR, 'div.coverWrapper a')
    links = [i.get_attribute("href") for i in items[:lim]]
    print(f"Got {len(links)} books in {cat}")

    collected = []
    for lnk in links:
        rec = grab_book(lnk)
        rec["Genre"] = cat
        print(f"Done: {rec['Title']} ({cat})")
        collected.append(rec)

    return collected

book_data = []
for category in ["fiction", "science"]:
    book_data.extend(grab_genre(category, lim=10))

df = pd.DataFrame(book_data)
# Convert ratings to numeric and clean reviews count
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Reviews_Count"] = df["Reviews"].str.extract("(\d+,?\d*)").replace(",", "", regex=True).astype(float)

# Comprehensive genre analysis
print("\n=== Genre Analysis ===")
analysis = df.groupby("Genre").agg({
    "Rating": ["mean", "min", "max", "count"],
    "Reviews_Count": ["mean", "sum"],
}).round(2)

analysis.columns = ["Avg Rating", "Min Rating", "Max Rating", "Books Count", "Avg Reviews", "Total Reviews"]
print("\nDetailed Statistics by Genre:")
print(analysis)

# Identify top genre
top_genre = analysis["Avg Rating"].idxmax()
print(f"\nTop Rated Genre: {top_genre}")
print(f"Average Rating: {analysis.loc[top_genre, 'Avg Rating']:.2f}")
print(f"Number of Books: {analysis.loc[top_genre, 'Books Count']:.0f}")
print(f"Total Reviews: {analysis.loc[top_genre, 'Total Reviews']:,.0f}")

# Show top 3 books in each genre
print("\n=== Top 3 Books by Genre ===")
for genre in df["Genre"].unique():
    genre_df = df[df["Genre"] == genre].nlargest(3, "Rating")
    print(f"\n{genre.upper()}:")
    for _, book in genre_df.iterrows():
        print(f"- {book['Title']} by {book['Author']}")
        print(f"  Rating: {book['Rating']} ({book['Reviews']})")

# Save to CSV with proper formatting
df.to_csv("output_5.csv", index=False)
print("\nData saved to output_5.csv")
drv.quit()
