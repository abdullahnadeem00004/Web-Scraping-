from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

browser_options = webdriver.ChromeOptions()
browser_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=browser_options)
waiter = WebDriverWait(driver, 20)

driver.get("https://www.topuniversities.com/")

try:
    cookie_accept = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.agree-button"))
    )
    cookie_accept.click()
    print("Cookies accepted")
except:
    print("No cookie popup found")

ranking_link = waiter.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.field--name-field-hp-ranking-cta a[href='/world-university-rankings']"))
)
driver.execute_script("arguments[0].click();", ranking_link)

time.sleep(3)
try:
    survey_option = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#edit-role-other")))
    driver.execute_script("arguments[0].click();", survey_option)
    submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Submit']")
    driver.execute_script("arguments[0].removeAttribute('disabled')", submit_btn)
    driver.execute_script("arguments[0].click();", submit_btn)
    print("Survey dismissed")
    time.sleep(3)
except:
    print("No survey popup appeared")

records = []
scraped_count = 0

while scraped_count < 50:
    uni_cards = waiter.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.new-ranking-cards.normal-row")
    ))

    for block in uni_cards:
        try:
            rank = block.find_element(By.CSS_SELECTOR, ".rank-no").text.strip()
        except:
            rank = None
        try:
            score = block.find_element(By.CSS_SELECTOR, ".rank-score").text.strip()
        except:
            score = None
        try:
            uni_name = block.find_element(By.CSS_SELECTOR, "a.uni-link").text.strip()
        except:
            uni_name = None
        try:
            location = block.find_element(By.CSS_SELECTOR, ".location").text.strip()
        except:
            location = None
        try:
            subject_rank = block.find_element(By.CSS_SELECTOR, ".indicators-container .rank").text.strip()
        except:
            subject_rank = None

        metrics = {}
        details = block.find_elements(By.CSS_SELECTOR, ".new-rankings-indicator-container")
        for d in details:
            try:
                metric_name = d.find_element(By.CSS_SELECTOR, "h2").text.strip()
                metric_val = d.find_element(By.CSS_SELECTOR, ".new-rankings-ind-val").text.strip()
                metrics[metric_name] = metric_val
            except:
                continue

        uni_info = {
            "Rank": rank,
            "University": uni_name,
            "Location": location,
            "Overall Score": score,
            "Subject Ranking": subject_rank
        }
        uni_info.update(metrics)
        records.append(uni_info)
        scraped_count += 1
        if scraped_count >= 50:
            break

    if scraped_count < 50:
        try:
            nxt_btn = driver.find_element(By.CSS_SELECTOR, "a.page-link.next")
            driver.execute_script("arguments[0].click();", nxt_btn)
            time.sleep(5)
        except:
            print("No next page button found")
            break

df = pd.DataFrame(records)
df["Country"] = df["Location"].apply(lambda x: x.split(",")[-1].strip() if x else None)
df["Overall Score"] = pd.to_numeric(df["Overall Score"], errors='coerce')

country_summary = df.groupby("Country").agg(
    University_Count=("University", "count"),
    Average_Score=("Overall Score", "mean")
).reset_index()

region_map = {
    "United States": "North America",
    "United Kingdom": "Europe",
    "China": "Asia",
    "Germany": "Europe",
    "Canada": "North America",
    "Australia": "Oceania",
    "Japan": "Asia",
    "Switzerland": "Europe",
    "Singapore": "Asia",
    "Hong Kong SAR": "Asia",
    "France": "Europe",
    "South Korea": "Asia",
    "Netherlands": "Europe",
}
df["Region"] = df["Country"].map(region_map)
region_summary = df.groupby("Region").agg(
    University_Count=("University", "count"),
    Average_Score=("Overall Score", "mean")
).reset_index()

print("\nTop 50 Universities Sample:\n", df.head())
print("\nUniversities per Country (with Average Scores):\n", country_summary)
print("\nUniversities per Region (with Average Scores):\n", region_summary)

df.to_csv("qs_top50.csv", index=False)
country_summary.to_csv("qs_country_summary.csv", index=False)
region_summary.to_csv("qs_region_summary.csv", index=False)

driver.quit()
