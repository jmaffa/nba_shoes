import requests
from bs4 import BeautifulSoup
import csv 
import time


def scrape_nba_shoes():
    base_url = "https://nbashoesdb.com/en/team/"
    teams = ['celtics', 'nets', 'knicks', 'sixers', 'raptors',
             'hawks', 'hornets', 'heat', 'magic', 'wizards',
             'bulls', 'cavaliers', 'pistons', 'pacers', 'bucks',
             'warriors', 'clippers', 'lakers', 'suns', 'kings',
             'mavericks', 'rockets', 'grizzlies', 'pelicans', 'spurs',
             'nuggets', 'timberwolves', 'thunder', 'blazers', 'jazz']
    players_to_exclude_after_one = {
        'Kawhi Leonard', 'Joel Embiid', 'Stephen Curry', 'LeBron James', 'Kevin Durant',
        'Jimmy Butler III', 'Nikola JokiÄ‡', 'Luka DonÄiÄ‡', 'Jayson Tatum', 'Giannis Antetokounmpo'
    }
    seen_players = set()
    base = "https://nbashoesdb.com"
    output_file = "nba_shoes.csv"

    # end_url = 'https://nbashoesdb.com/en/team/celtics'
    # response = requests.get(end_url)
    # soup = BeautifulSoup(response.text, "html.parser")
    # all_tables = soup.find_all("table")
    # players = all_tables[1]
    # player_links = soup.find_all("a", href=True)
    
    # player_urls = list(set(base + link['href'] for link in player_links if "/en/player/" in link['href']))

    with open("nba_shoes.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Team", "Player Name", "Primary Shoe Brand", "Primary Shoe Model", "List of All Shoes"])

        for team in teams:
            end_url = f"{base_url}{team}"
            response = requests.get(end_url)
            soup = BeautifulSoup(response.text, "html.parser")
            all_tables = soup.find_all("table")
            all_links = soup.find_all("a", href=True)
            player_urls = list(set(base + link['href'] for link in all_links if "/en/player/" in link['href'] and "menuaplayer" not in link.get('class', '')))
            # print(player_urls)

            for player_url in player_urls:
                print(f"Visiting {player_url}")
                player_response = requests.get(player_url)
                player_soup = BeautifulSoup(player_response.text, "html.parser")

                # this works... we need to now 
                all_headers = player_soup.find_all("h1")
                player_name = all_headers[0].text.replace("Report error", "").strip()
                # only add every player once (excludes the "Top Players" tab)
                if player_name in players_to_exclude_after_one and player_name in seen_players:
                    continue
                seen_players.add(player_name)

                team_name = player_soup.find_all("h3")[-1].text.replace(" roster","").strip()

                all_tables = player_soup.find_all("table")
                # Set defaults, like Anton Watson, if player doesn't have a shoe, then they don't have any historical data either
                primary_model = ""
                primary_brand = ""
                shoes_store = set()

                if all_tables[1]:
                    primary_shoe = all_tables[1].find_all("tr")
                    if primary_shoe:
                        # model Name for primary shoe
                        primary_model = primary_shoe[0].find("td").find_next_sibling("td").text.strip()
                        # brand Name
                        primary_brand = primary_shoe[1].find("td").find_next_sibling("td").text.strip()

                        # print("Model:", primary_model)
                        # print("Brand:", primary_brand)

                    # Historical data
                    shoe_table = all_tables[2]
                    header_row = shoe_table.find("thead").find("tr").find_all("th")
                    # protect against pages with the worng number of tables
                    if header_row[0].text == "Date":
                        all_shoes = shoe_table.find("tbody").find_all("tr")
                        
                        for shoe in all_shoes:
                            columns = shoe.find_all("td")
                    
                            # Extract brand and model
                            brand = columns[1].text.strip()
                            model = columns[2].text.replace(brand, "").strip()
                            shoes_store.add((brand, model))
                            # Convert all shoes to a readable string format
                # Write row to CSV
                writer.writerow([team_name, player_name, primary_brand, primary_model, shoes_store])
                print('Wrote', player_name)
                # print(shoes_store)
    print("CSV file saved as 'nba_shoes.csv'!")
    post_process(output_file)

    # print(player_urls)

def post_process(file_path):
    """
    Reads the CSV file, fixes encoding issues, and saves a cleaned version.
    """
    replacements = {
        "361Â°": "361°",
        "Nikola JokiÄ‡": "Nikola Jokić",
        "Luka DonÄiÄ‡": "Luka Dončić"
    }

    cleaned_file = "nba_shoes_cleaned.csv"

    with open(file_path, mode="r", encoding="utf-8") as infile, open(cleaned_file, mode="w", newline="", encoding="utf-8") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            cleaned_row = [replace_text(cell, replacements) for cell in row]
            writer.writerow(cleaned_row)

def replace_text(text, replacements):
    """
    Replaces incorrect characters in a given text.
    """
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

if __name__ == "__main__":
    start_time = time.time()

    scrape_nba_shoes()

    end_time = time.time()

    print(f"Total time taken: {end_time - start_time:.2f} seconds")


# post processing
# 361Â° => 361
# a few team names
# Dennis Schroder, Nikola Jokic, Nikola Jovic, Luka Doncic, Saric, Monte Morris, Vasilije Micic, Jonas Valanciunas, Dante Exum, D'Angelo Russell, Karlo Matkovic
# Dario Saric, Vlatko Cancar
# some 