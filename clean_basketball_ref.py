import pandas as pd

S23_24_RAW = "basketball-ref/23-24-advancedstats-raw.csv"
S24_25_RAW = "basketball-ref/24-25-advancedstats-raw.csv"
S23_24_OUT = "basketball-ref/23-24-advancedstats-cleaned.csv"
S24_25_OUT = "basketball-ref/24-25-advancedstats-cleaned.csv"
def clean_basketball_ref():
    s23_24_df = pd.read_csv(S23_24_RAW)
    s24_25_df = pd.read_csv(S24_25_RAW)
    # Need to clean superstar names so they match
    name_to_clean = {
        "Nikola Jokić" : "Nikola Jokic",
        "Luka Dončić" : "Luka Doncic",
        "Kristaps Porziņģis" : "Kristaps Porzingis",
        "Alperen Şengün" : "Alperen Sengun",
        "Jonas Valančiūnas": "Jonas Valanciunas",
        "Jusuf Nurkić" : "Jusuf Nurkic",
        "Nikola Vučević" : "Nikola Vucevic",
        "Bogdan Bogdanović" : "Bogdan Bogdanovic"
    }

    def fix_name(player_name):
        for key, player in name_to_clean.items():
            if key in player_name:
                return player
        return player_name
    
    s23_24_df['Player'] = s23_24_df['Player'].apply(fix_name)
    s24_25_df['Player'] = s24_25_df['Player'].apply(fix_name)

    s23_24_df.to_csv(S23_24_OUT)
    s24_25_df.to_csv(S24_25_OUT)
    pass
if __name__ == "__main__":
    clean_basketball_ref()