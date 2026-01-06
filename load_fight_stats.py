import pandas as pd

# Helper methods

def parse_stat(val: str):
    """
    Convert 'x of y' to int x and int y
    This is used in cases when finding number of strikes, takedowns, submissions, etc.
    """
    if pd.isna(val) or val.strip() in ["---", "--"]:
        return 0, 0
    try:
        parts = val.split(" of ")
        return int(parts[0]), int(parts[1])
    except Exception:
        return 0, 0


def time_to_seconds(t):
    """
    Asked ChatGPT to easily parse the seconds out of the file
    Parse fight time into seconds
    """
    if pd.isna(t) or t.strip() == "":
        return None
    try:
        m, s = t.split(":")
        return int(m) * 60 + int(s)
    except Exception:
        return None


def load_fight_stats(file_path: str) -> pd.DataFrame:
    """
    Load fight_stats.csv into the Fighter Fight Stats schema.
    """
    stats_raw = pd.read_csv(file_path)

    df = stats_raw.copy()

    # Split 'x of y' stats into landed and attempted
    cols = ['SIG STR', 'TOTAL STR', 'TD', 'HEAD', 'BODY', 'LEG', 'DISTANCE', 'CLINCH', 'GROUND']
    for col in cols:
        df[col + '_landed'], df[col + '_attempted'] = zip(*df[col].map(parse_stat))

    # Turn KnockDowns to integer instead of float
    df['KD'] = df['KD'].fillna(0).astype(int)

    # Calculate Sig. Striking %
    df['SIG STR PCT'] = df['SIG STR PCT'].replace('---', '0').str.replace("%","").astype(float)

    # Submissions
    df['SUB ATT'] = df['SUB ATT'].replace('---', '0').fillna(0).astype(int)

    # Control time
    df['CTRL'] = df['CTRL'].apply(time_to_seconds)

    # Save info to df
    df_clean = df[[
        'EVENT', 'BOUT', 'FIGHTER', 'KD',
        'SIG STR_landed', 'SIG STR_attempted',
        'TOTAL STR_landed', 'TOTAL STR_attempted',
        'TD_landed', 'TD_attempted', 'SUB ATT',
        'CTRL'
    ]]

    return df_clean


if __name__ == "__main__":
    df = load_fight_stats("data/fight_stats.csv")
    
    # for testing purposes
    print(df.head(20))
