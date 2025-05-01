import requests
from bs4 import BeautifulSoup
import csv 
import time
import argparse
import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# COMMENT IN FOR RESCRAPE
OUTPUT_FILE = "kix_stats_rescraped.csv"
# COMMENT IN FOR NORMAL
# OUTPUT_FILE = "kix_stats.csv"
CACHED_FILE = "kixstats.html"
CUTOFF_DATE = datetime.strptime("2023-10-24", "%Y-%m-%d")
RESCRAPE_URLS = [
    "https://kixstats.com/kickstats/nike-book-1-31",
    "https://kixstats.com/kickstats/adidas-dame-9-13",
    "https://kixstats.com/kickstats/adidas-harden-vol--4-58",
    "https://kixstats.com/kickstats/adidas-adizero-select-80",
    "https://kixstats.com/kickstats/air-jordan-38-low-18",
    "https://kixstats.com/kickstats/jordan-why-not--zer0-4-53",
    "https://kixstats.com/kickstats/puma-mb-02-66",
    "https://kixstats.com/kickstats/anta-KT-10-basketball-shoes",
    "https://kixstats.com/kickstats/under-armour-curry-1-low-flotro-47",
    "https://kixstats.com/kickstats/converse-all-star-bb-shift-67"
]

def safe_get(driver, url, timeout=30, retries=1):
    driver.set_page_load_timeout(timeout)

    for attempt in range(retries + 1):  # retry count = retries + 1 total tries
        try:
            driver.get(url)
            return True  # Success!
        except Exception as e:
            # print(f"⚠️ Attempt {attempt+1}: Failed to load {url}: {e}")
            logging.error(f"Attempt {attempt+1}: Failed to load {url}: {e}")
            if attempt == retries:
                logging.error(f"Giving up on {url} after {retries+1} attempts.")
                # print(f"❌ Giving up on {url} after {retries+1} attempts.")
                return False
            time.sleep(2)  # Small wait before retrying

def is_before_cutoff(driver):
    # After each click and small wait:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find the stats table and all rows
    stats_table = soup.find(id="stats").find("table")
    rows = stats_table.find_all("tr")

    # Find the oldest date currently visible
    dates = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 1:
            continue
        date_text = cols[0].text.strip()
        try:
            row_date = datetime.strptime(date_text, "%Y-%m-%d")
            dates.append(row_date)
        except ValueError:
            continue

    if dates:
        oldest_date = min(dates)
        print(oldest_date)
        if oldest_date < CUTOFF_DATE:
            print("Reached old season, stopping clicking.")
            return True
    return False


def write_base_html_to_cache():
    base_html = ""
    # Mimic browser headers
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Loop through all ct values
    for ct in range(4, 68):  # Based on ct <= 67
        response = requests.post("https://kixstats.com/brandsajax", data={"ct": ct}, headers=headers)
        
        if response.status_code == 200:
            base_html += response.text
    else:
        print(f"Failed to fetch ct={ct}")
    
    with open(CACHED_FILE, "w", encoding="utf-8") as f:
        f.write(response.text)

    return base_html


def open_all_shoe_stats(url, csv_writer):
    
    # For Logging purposes
    row_counter = 0
    show_more_counter = 0

    options = Options()
    
    options.add_argument("--headless=new") 
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # url = "https://kixstats.com/kickstats/nike-book-1-31"
    
    if not safe_get(driver, url, timeout=20, retries=1):
        driver.quit()
        return  # Skip this shoe safely
    wait = WebDriverWait(driver, 10)
    

    while True:
        try:
            stats_div = driver.find_element(By.ID, "stats")

            # Find the button only inside the stats div
            show_more_button = stats_div.find_element(By.XPATH, ".//a[contains(text(), 'Show more')]")
            
            # Wait for *that specific button* to be clickable
            wait.until(EC.element_to_be_clickable(show_more_button))

            show_more_button.click()

            show_more_counter+=1
            
            if (show_more_counter % 10 == 0):
                print(f"Pressing show more {show_more_counter} times")
            
            # Optional tiny wait to be safe
            time.sleep(0.2)
            # check for date cutoff every 10 or every one once you are above a certain threshold
            if show_more_counter > 250 or show_more_counter % 10 == 0:
                if is_before_cutoff(driver):
                    break


        except (NoSuchElementException, ElementClickInterceptedException):
            print("No more 'Show more' buttons.")
            break
        except StaleElementReferenceException:
            print("Got stale element! Trying again...")
            continue
        except Exception as e:
            # print(f"Unexpected error: {e}")
            logging.error(f"Unexpected error on {url}: {e}")
            break


    try: 
        html = driver.page_source
    except Exception as e:
        logging.error(f"Unexpected error getting page source on {url}: {e}")
    soup = BeautifulSoup(html, "html.parser")
    # Get shoe base name
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    description = meta_tag['content']
    # Remove "kicks statistics" from the end
    shoe_name = description.replace("kicks statistics", "").strip()

    # find the table
    stats_table = soup.find(id="stats").find("table")

    # parse the rows, maybe time box it in the past two seasons
    rows = stats_table.find_all("tr")
    for row in rows:
        # Date check before 10-24-23 which is the start of the last two seasons.
        cols = row.find_all("td")
        if len(cols) < 9:
            continue  # Skip incomplete rows just in case
        date_str = cols[0].text.strip()
        try:
            row_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue  # Skip rows with bad dates
        # Compare dates
        if row_date < CUTOFF_DATE:
            break  # Skip anything on or before 2023-10-24

        player_col = cols[1]
        shoe_img = player_col.find("img")
        colorway = shoe_img["alt"].strip() if shoe_img else "Unknown Shoe"
        player_name = player_col.get_text(strip=True)

        minutes = cols[3].text.strip()
        points = cols[4].text.strip()
        rebounds = cols[5].text.strip()
        assists = cols[6].text.strip()
        steals = cols[7].text.strip()
        blocks = cols[8].text.strip()

        row_counter+=1
        csv_writer.writerow([shoe_name, colorway, date_str, player_name, minutes, points, rebounds, assists, steals, blocks])

    logging.info(f"Wrote {row_counter} rows for {shoe_name}")
    driver.quit()
def scrape_kix_stats(base_html):
    base_url = "https://kixstats.com/brands"
    
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        if not base_html:
            base_html = write_base_html_to_cache()

        # Write the header row 
        writer = csv.writer(file)
        writer.writerow(["Shoe", "Colorway", "Date", "Player", "Min", "Points", "Rebounds", "Assists", "Steals", "Blocks"])

        soup = BeautifulSoup(base_html, "html.parser")
        # find brands
        # brands = soup.find(id="brands")

        shoes = soup.find_all(class_="player-name")
        # COMMENT IN FOR RESCRAPE
        shoe_links = RESCRAPE_URLS
        # COMMENT IN FOR NORMAL
        # shoe_links = [div.find('a') for div in shoes]
        
        visited_links = set()
        for shoe_link in shoe_links:
            # COMMENT IN FOR RESCRAPE
            href = shoe_link
            # COMMENT IN FOR NORMAL
            # href = shoe_link['href']
            if href in visited_links or "brandstats" in href or "kickstats" not in href:
                continue
            try:
                print(f"Visiting: {href}")
                start_time = time.time()
                open_all_shoe_stats(href, writer)
                end_time = time.time()
                print(f"Spent: {end_time - start_time:.2f} seconds at {href}")
                visited_links.add(href)
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to fetch {href}: {e}")
            


if __name__ == "__main__":
    logging.basicConfig(
        filename='kix_scraper_errors.log',  # File where logs will be saved
        level=logging.INFO,                 # Log INFO, WARNING, ERROR levels
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", action="store_true")
    args = parser.parse_args()

    base_html = ""
    if args.cache and os.path.exists(CACHED_FILE):
        with open(CACHED_FILE, "r", encoding="utf-8") as f:
            base_html = f.read()
    start_time = time.time()

    # open_all_shoe_stats()
    scrape_kix_stats(base_html)

    end_time = time.time()

    print(f"Total time taken: {end_time - start_time:.2f} seconds")