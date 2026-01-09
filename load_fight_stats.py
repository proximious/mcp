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
    if t in ("---", "0:00", 0, 0.0):
        return 0
    t_str = str(t)
    if ":" not in t_str:
        return 0
    m, s = t_str.split(":")
    return int(m) * 60 + int(s)


def load_fight_stats(file_path: str) -> pd.DataFrame:
    """
    Load fight_stats.csv into the Fighter Fight Stats schema.
    """
    stats_raw = pd.read_csv(file_path)

    df = stats_raw.copy()

    # I asked ChatGPT to extract the values from each of the cols to calculate the percentages
    # Split 'x of y' stats into landed and attempted
    cols = ['SIG STR', 'TOTAL STR', 'TD', 'HEAD', 'BODY', 'LEG', 'DISTANCE', 'CLINCH', 'GROUND']
    for col in cols:
        df[col + '_landed'], df[col + '_attempted'] = zip(*df[col].map(parse_stat))

    # Convert numeric columns (used ChatGPT to get most of the bug fixes from these lines)
    df['KD'] = pd.to_numeric(df['KD'], errors='coerce').fillna(0)
    df['TD_landed'] = pd.to_numeric(df['TD_landed'], errors='coerce').fillna(0)
    df['TD_attempted'] = pd.to_numeric(df['TD_attempted'], errors='coerce').fillna(0)
    df['CTRL'] = df['CTRL'].fillna('0:00').apply(time_to_seconds)
    df['SIG STR_attempted'] = df['SIG STR_attempted'].apply(lambda x: int(str(x).split(" of ")[0]) if x != '---' else 0)
    df['SIG STR_landed'] = df['SIG STR_landed'].apply(lambda x: int(str(x).split(" of ")[0]) if x != '---' else 0)
    df['TOTAL STR_landed'] = df['TOTAL STR_landed'].apply(lambda x: int(str(x).split(" of ")[0]) if x != '---' else 0)
    df['SUB ATT'] = pd.to_numeric(df['SUB ATT'].replace('---', 0), errors='coerce').fillna(0)
    df['DISTANCE'] = pd.to_numeric(df['DISTANCE'].replace('---', 0).str.replace('%', '', regex=False), errors='coerce').fillna(0)

    # Save info to df
    df_clean = df[[
        'EVENT', 'BOUT', 'FIGHTER', 'KD',
        'SIG STR_landed', 'SIG STR_attempted',
        'TOTAL STR_landed', 'TOTAL STR_attempted',
        'TD_landed', 'TD_attempted', 'SUB ATT',
        'CTRL', 'DISTANCE'
    ]]

    return df_clean


if __name__ == "__main__":
    df = load_fight_stats("data/fight_stats.csv")
    
    # for testing purposes
    print(df.head(20))
