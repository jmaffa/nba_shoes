import requests
from bs4 import BeautifulSoup
import csv 
import time


def scrape_kix_stats():
    base_url = "https://kixstats.com/brands"
    output_file = "kix_stats.csv"

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:

        all_html = ""

        # Mimic browser headers
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Loop through all ct values
        for ct in range(4, 68):  # Based on ct <= 67
            response = requests.post("https://kixstats.com/brandsajax", data={"ct": ct}, headers=headers)
            
            if response.status_code == 200:
                all_html += response.text
        else:
            print(f"Failed to fetch ct={ct}")
        print(all_html)



        # base_response = requests.get(base_url)
        soup = BeautifulSoup()
        # if base_response.status_code == 200:
        #     soup = BeautifulSoup(base_response.text, "html.parser")
        #     print(soup)
        # print(base_response)



if __name__ == "__main__":
    start_time = time.time()

    scrape_kix_stats()

    end_time = time.time()

    print(f"Total time taken: {end_time - start_time:.2f} seconds")