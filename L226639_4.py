from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import re
import numpy as np

query = input("Search product: ") or "iPhone 15"

opt = Options()
opt.add_argument("--start-maximized")
svc = Service("chromedriver.exe")
driver = webdriver.Chrome(service=svc, options=opt)

driver.get("https://www.daraz.pk/")

search_input = driver.find_element(By.NAME, "q")
search_input.send_keys(query)
search_input.send_keys(Keys.RETURN)
time.sleep(10)  

prev_height = driver.execute_script("return document.body.scrollHeight")
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:
        break
    prev_height = new_height

names, costs, vendors, stars, shipping = [], [], [], [], []

selectors = [
    "div.box--pRqdD",  
    "div[data-qa-locator='product-item']", 
    "div.gridItem--Yd0sa",  
    "div.Bm3ON" 
]

elements = []
product_urls = []

for selector in selectors:
    elements = driver.find_elements(By.CSS_SELECTOR, selector)
    if elements:
        print(f"Found {len(elements)} products using selector: {selector}")
        break

elements = elements[:20]  # Limit to first 20 results

# First pass: collect URLs and basic info
for el in elements:
    try:
        # Get product URL
        url = el.find_element(By.CSS_SELECTOR, "a[href*='/products/']").get_attribute("href")
        product_urls.append(url)
    except:
        product_urls.append(None)

# Second pass: visit each product page and collect detailed info
for idx, el in enumerate(elements):
    # Product name
    try:
        name = el.find_element(By.CSS_SELECTOR, "div[data-qa-locator='product-name']").text
    except:
        try:
            name = el.find_element(By.CSS_SELECTOR, "div.title--wFj93 a").get_attribute("title")
        except:
            try:
                # Try finding any anchor tag with title attribute
                name = el.find_element(By.CSS_SELECTOR, "a[title]").get_attribute("title")
            except:
                name = None

    # Price
    price_selectors = [
        "div.price--NVB62",
        "span.currency--GVKjl",
        "div[data-qa-locator='product-price']",
        "span.ooOxS"
    ]
    
    cost = None
    for selector in price_selectors:
        try:
            cost = el.find_element(By.CSS_SELECTOR, selector).text
            if cost:
                break
        except:
            continue

    # Seller name will be obtained from product page

    # Visit product page once to get all details (rating, seller, delivery)
    star = None
    vendor = None
    ship = None
    
    if product_urls[idx]:
        try:
            # Visit product page
            driver.execute_script("window.open('');")  # Open new tab
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(product_urls[idx])
            time.sleep(3)  # Wait for page to load
            
            # Get rating
            try:
                # Look for star images in rating section
                star_container = driver.find_element(By.CSS_SELECTOR, "div.pdp-review-summary__stars")
                filled_stars = len(star_container.find_elements(By.CSS_SELECTOR, "img.star"))
                star = str(filled_stars) if filled_stars > 0 else "No Ratings"
                
                # Also look for number of reviews
                reviews = driver.find_element(By.CSS_SELECTOR, "a.pdp-review-summary__link").text
                if reviews:
                    star = f"{star} ({reviews})"
            except:
                star = "No Ratings"
                
            # Get seller information
            try:
                seller_name = driver.find_element(By.CSS_SELECTOR, "div.seller-name__detail a.seller-name__detail-name").text
                # Try to get seller ratings
                try:
                    positive_rating = driver.find_element(By.CSS_SELECTOR, "div.seller-info-value.rating-positive").text
                    ship_time = driver.find_element(By.CSS_SELECTOR, "div.info-content:nth-child(2) .seller-info-value").text
                    vendor = f"{seller_name} (Positive: {positive_rating}, Ship on Time: {ship_time})"
                except:
                    vendor = seller_name
            except:
                vendor = None
                
            # Get delivery information
            try:
                delivery_info = []
                
                # Get standard delivery details
                standard_delivery = driver.find_element(By.CSS_SELECTOR, "div.delivery-option-item_type_standard")
                
                # Get delivery time
                try:
                    delivery_time = standard_delivery.find_element(By.CSS_SELECTOR, "div.delivery-option-item__time").text
                    delivery_info.append(delivery_time)
                except: pass
                
                # Get shipping fee
                try:
                    shipping_fee = standard_delivery.find_element(By.CSS_SELECTOR, "div.delivery-option-item__shipping-fee").text
                    if shipping_fee:
                        delivery_info.append(f"Fee: {shipping_fee}")
                except: pass
                
                # Check for Cash on Delivery
                try:
                    if driver.find_element(By.CSS_SELECTOR, "div.delivery-option-item_type_COD"):
                        delivery_info.append("COD Available")
                except: pass
                
                # Get shipping promotion
                try:
                    promotion = driver.find_element(By.CSS_SELECTOR, "div.delivery-option-item__promotion").text
                    if promotion:
                        delivery_info.append(f"Promo: {promotion}")
                except: pass
                
                ship = " | ".join(delivery_info) if delivery_info else None
                
            except Exception as e:
                print(f"Error getting delivery info: {str(e)}")
                ship = None
            
            # Close tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(f"Error processing product {idx + 1}: {str(e)}")
            star = None
            vendor = None
            ship = None

    # Delivery information will be obtained from product page

    names.append(name)
    costs.append(cost)
    vendors.append(vendor)
    stars.append(star)
    shipping.append(ship)

driver.quit()

df = pd.DataFrame({
    "Title": names,
    "Price": costs,
    "Seller": vendors,
    "Rating": stars,
    "Delivery": shipping
})

# Set display options for better readability
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("\nFirst 20 Results:")
if len(df) > 0:
    print(df.head(20).to_string())
else:
    print("No results found. Trying alternative selectors...")

# Save to CSV
df.to_csv("output_t4.csv", index=False)

def parse_price(x):
    if pd.isna(x):
        return np.nan
    txt = re.sub(r'[^\d.]', '', str(x))
    if txt == "":
        return np.nan
    try:
        return float(txt)
    except:
        return np.nan

df['PriceValue'] = df['Price'].apply(parse_price)

def parse_rating(x):
    if pd.isna(x):
        return np.nan
    # Handle both numeric strings and star counts
    try:
        # First try to find decimal numbers (e.g. "4.5")
        vals = re.findall(r"[\d.]+", str(x))
        if vals:
            rating = float(vals[0])
            # Validate rating is in reasonable range
            if 0 <= rating <= 5:
                return rating
        # If no valid decimal found, try counting stars
        stars = str(x).count('★')
        if stars > 0 and stars <= 5:
            return float(stars)
    except:
        pass
    return np.nan

df['RatingValue'] = df['Rating'].apply(parse_rating)

if df['PriceValue'].dropna().empty:
    print("\nNo valid prices parsed.")
else:
    # Calculate price statistics
    min_price = df['PriceValue'].min()
    max_price = df['PriceValue'].max()
    avg_price = df['PriceValue'].mean()
    
    print("\nPrice Analysis:")
    print(f"Minimum Price: Rs. {min_price:,.0f}")
    print(f"Maximum Price: Rs. {max_price:,.0f}")
    print(f"Average Price: Rs. {avg_price:,.0f}")
    
    # Define price ranges for comparison
    price_threshold = min_price * 1.15  
    
    # Filter products within reasonable price range
    reasonable_prices = df[df['PriceValue'] <= price_threshold].copy()
    
    if len(reasonable_prices) > 0:
        # Sort by rating (descending) and price (ascending)
        reasonable_prices['RatingValue'] = reasonable_prices['RatingValue'].fillna(0)
        reasonable_prices = reasonable_prices.sort_values(['RatingValue', 'PriceValue'], 
                                                        ascending=[False, True])
        
        print("\nBest Deals (considering both price and rating):")
        print("\nTop 3 Best Value Deals:")
        print(reasonable_prices[['Title', 'Price', 'Seller', 'Rating', 'Delivery']].head(3).to_string())
        
        # Show absolute cheapest option regardless of rating
        cheapest = df.nsmallest(1, 'PriceValue')
        if not cheapest.equals(reasonable_prices.head(1)):
            print("\nCheapest Option (regardless of rating):")
            print(cheapest[['Title', 'Price', 'Seller', 'Rating', 'Delivery']].to_string())
        
        # Show highest rated option within reasonable price range
        highest_rated = reasonable_prices.nlargest(1, 'RatingValue')
        if not highest_rated.equals(reasonable_prices.head(1)):
            print("\nHighest Rated Option (within reasonable price range):")
            print(highest_rated[['Title', 'Price', 'Seller', 'Rating', 'Delivery']].to_string())
        
    else:
        print("\nNo products found within reasonable price range.")