import pandas as pd

def load_fights(file_path: str) -> pd.DataFrame:
    """
    Load and normalize fights.csv into the Fights schema.
    """
    # Read in file
    fights_raw = pd.read_csv(file_path)

    # Duplicating to not affect the original data
    fights = fights_raw.copy()

    # Get rid of 'Bout' in each weight class to clean it
    fights['weight_class'] = fights['WEIGHTCLASS'].str.replace(" Bout", "").str.strip()

    # Parse round number
    fights['rounds_scheduled'] = fights['TIME FORMAT'].str.extract(r'(\d+) Rnd')[0].astype(float)

    # Asked ChatGPT to easily parse the seconds out of the file
    # Parse fight time into seconds
    def time_to_seconds(t):
        if pd.isna(t) or t.strip() == "":
            return None
        try:
            m, s = t.split(":")
            return int(m) * 60 + int(s)
        except Exception:
            return None

    # Save info to df
    fights['round_finished'] = fights['ROUND']
    fights['time_finished_sec'] = fights['TIME'].apply(time_to_seconds)

    fights_clean = fights[[
        'EVENT', 'BOUT', 'weight_class', 'METHOD', 'round_finished', 'time_finished_sec', 'REFEREE'
    ]]

    return fights_clean


if __name__ == "__main__":
    df = load_fights("data/fights.csv")
    
    # for testing purposes
    print(df.head(20))
