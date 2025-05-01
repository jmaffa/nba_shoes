import pandas as pd
from datetime import datetime

# Cleaning Tasks
# Remove the bad shoes rows
# Append the new ones (just merge CSVs)
# Add seasons

SHOES_TO_DELETE = [
    "Nike Book 1",
    "adidas Dame 9",
    "adidas Harden Vol. 4",
    "Air Jordan 38 Low",
    "Jordan Why Not? Zer0.4",
    "Puma MB.02",
    "Anta KT 10",
    "Under Armour Curry 1 Low FloTro",
    "Converse All Star BB Shift"
]

FULL_CSV = "kix_stats.csv"
APPENDING_CSV = "kix_stats_rescraped.csv"
OUTPUT_CSV = "kix_stats_cleaned.csv"
def delete_malformed_from_original():
    og_df = pd.read_csv(FULL_CSV)
    remove_malformed_df = og_df[~og_df['Shoe'].isin(SHOES_TO_DELETE)]
    # remove_malformed_df.to_csv(OUTPUT_CSV, index=False)

    print(f"New DF has {len(og_df)- len(remove_malformed_df)} fewer rows than original.")
    return remove_malformed_df
def merge_csvs(df1, df2):
    df2.columns = df1.columns
    combined_df = pd.concat([df1, df2], ignore_index=True)
    return combined_df
    pass

def add_seasons(seasonless_df):
    # add a new column with categorical data
    # S23-24, P23-24, S24-25, P24-25, N/A
    
    season_map = {
        "S23-24" : ["2023-10-24", "2024-04-14"],
        "P23-24" : ["2024-04-20", "2024-05-30"],
        "S24-25" : ["2024-10-22", "2025-04-13"],
        "P24-25" : ["2025-04-19", "2025-05-01"]
    }
    season_ranges = {season: [datetime.strptime(start, "%Y-%m-%d"), datetime.strptime(end, "%Y-%m-%d")] 
                 for season, (start, end) in season_map.items()}
    
    def assign_season(date_str):
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            for season, (start, end) in season_ranges.items():
                if start <= date <= end:
                    return season
            return "N/A"  # If it doesn't fit any season
        except Exception as e:
            return "N/A"  # If date parsing fails
    seasonless_df['Season'] = seasonless_df['Date'].apply(assign_season)

    return seasonless_df

def add_brands(df):
    brand_map = {
        "361" : "361",
        "741" : "741",
        "adidas" : "adidas",
        "Air Jordan" : "Nike",
        "AND1" : "AND1",
        "Anta" : "Anta",
        "asics" : "Asics",
        "Converse" : "Converse",
        "Creative Control" : "Creative Control",
        "Crossover Culture" : "Crossover Culture",
        "Curry" : "Under Armour",
        "ETHICS": "Ethics",
        "Holo": "HOLO",
        "Jordan": "Nike",
        "Judah" : "Unitas",
        "Li-Ning" : "Li-Ning",
        "Moolah" : "Moolah",
        "New Balance" : "New Balance",
        "Nike" : "Nike",
        "Oatica" : "Oatica Wave",
        "Peak" : "Peak",
        "Puma" : "Puma",
        "Qiaodan" : "Qiaodan",
        "Reebok" : "Reebok",
        "Rigorer" : "Rigorer",
        "Serious Player Only": "Serious Player Only",
        "Skechers" : "Skechers",
        "Stria" : "Stria",
        "Tarmak" : "Tarmak",
        "Under Armor" : "Under Armour",
        "Under Armour" : "Under Armour",
        "Xero" : "Xero",
        "Xtep" : "Xtep"
    }
    def find_brand(shoe_name):
        for key, brand in brand_map.items():
            if key in shoe_name:
                return brand
        return "N/A"
    df["Brand"] = df['Shoe'].apply(find_brand)
    return df

def add_stars(df):
    # Data gotten from https://www.espn.com/espn/feature/story/_/id/39771146/sneakerhead-guide-every-nba-wnba-signature-sneaker-history
    star_map = {
        "361 AG" : "Aaron Gordon",
        "361 Joker" : "Nikola Jokic",
        "361 DVD" : "Spencer Dinwiddie",
        "741 Performance Rover" : "Jaylen Brown",
        "adidas AE" : "Anthony Edwards",
        "adidas D Rose" : "Derrick Rose",
        "adidas D.O.N." : "Donovan Mitchell",
        "adidas Dame" : "Damian Lillard",
        'adidas Harden': "James Harden",
        "adidas T-MAC" : "Tracy McGrady",
        "adidas TMAC" : "Tracy McGrady",
        "adidas Trae" : "Trae Young",
        "Air Jordan" : "Michael Jordan",
        "Anta GH" : "Gordon Hayward",
        "Anta Gordon Hayward": "Gordon Hayward",
        "Anta KAI" : "Kyrie Irving",
        "Anta KT" : "Klay Thompson",
        "Converse SHAI" : "Shai Gilgeous-Alexander",
        "Creative Control" : "Sydney Colson",
        "Curry Fox 1": "De'Aaron Fox",
        "Curry" : "Stephen Curry",
        "ETHICS LG" : "Langston Galloway",
        "Holo IO" : "Isaac Okoro",
        "Jordan CP3" : "Chris Paul",
        "Jordan Luka" : "Luka Doncic",
        "Jordan Melo" : "Carmelo Anthony",
        "Jordan Tatum" : "Jayson Tatum",
        "Jordan Westbrook" : "Russell Westbrook",
        "Jordan Why Not": "Russell Westbrook",
        "Jordan Zion": "Zion Williamson",
        "Li-Ning CJ" : "CJ McCollum",
        "Li-Ning DL" : "D'Angelo Russell",
        "Li-Ning JB" : "Jimmy Butler",
        "Li-Ning Wade" : "Dwayne Wade",
        "Li-Ning Way of Wade" : "Dwayne Wade",
        "New Balance Kawhi": "Kawhi Leonard",
        "Nike Air Penny" : "Penny Hardaway",
        "LeBron 1" : "LeBron James",
        "Nike Book" : "Devin Booker",
        "Nike Freak" : "Giannis Antetokounmpo",
        "Nike Giannis" : "Giannis Antetokounmpo",
        "Lebron" : "LeBron James",
        "Nike JA" : "Ja Morant",
        "Nike KD" : "Kevin Durant",
        "Nike Kobe" : "Kobe Bryant",
        "Nike Kyrie" : "Kyrie Irving",
        "Nike LeBron" : "LeBron James",
        "Nike Mamba" : "Kobe Bryant",
        "Nike PG" : "Paul George",
        "Nike Sabrina" : "Sabrina Ionescu",
        "Nike Zoom Freak" : "Giannis Antetokounmpo",
        "Nike Zoom LeBron" : "LeBron James",
        "Nike Zoom KD": "Kevin Durant",
        "Peak AW" : "Andrew Wiggins",
        "Peak Delly" : "Matthew Dellavedova",
        "Puma Clyde" : "Clyde Frazier",
        "Puma MB" : "LaMelo Ball",
        "Puma Scoot" : "Scoot Henderson",
        "Puma Stewie" : "Breanna Stewart",
        "Reebok Answer" : "Allen Iverson",
        "Reebok Solution" : "Allen Iverson",
        "Rigorer AR": "Austin Reaves",
        "Under Armour Curry" : "Stephen Curry",
        "Under Armour Embiid" : "Joel Embiid",
    }
    def find_star(shoe_name):
        for key, star in star_map.items():
            if key in shoe_name:
                return star
        return "N/A"
    
    df['Signature_Star'] = df['Shoe'].apply(find_star)
    return df

def clean_kix_stats():
    remove_malformed_df = delete_malformed_from_original()
    rescraped_df = pd.read_csv(APPENDING_CSV, skiprows=1, header=None)
    combined_df = merge_csvs(remove_malformed_df,rescraped_df)
    with_seasons_df = add_seasons(combined_df)
    with_stars_df = add_stars(with_seasons_df)
    with_brands_df = add_brands(with_stars_df)
    with_brands_df.to_csv(OUTPUT_CSV, index=False)

    pass

if __name__ == "__main__":
    clean_kix_stats()