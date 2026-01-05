import pandas as pd

def load_fighters(file_path: str) -> pd.DataFrame:
    """
    Load and normalize fighters.csv into the Fighters schema (schema.md).
    """
    fighters_raw = pd.read_csv(file_path)

    # Asked ChatGPT to turn height from feet + inches to just inches
    # Clean height, reach, weight
    def parse_inches(val):
        if pd.isna(val) or val.strip() in ["--", ""]:
            return None
        if "'" in val:
            feet, inches = val.split("'")
            return int(feet) * 12 + int(inches.replace('"', '').strip())
        return None

    def parse_weight(val):
        if pd.isna(val) or val.strip() in ["--", ""]:
            return None
        return int(val.strip().replace(" lbs.", ""))

    fighters = fighters_raw.copy()
    fighters['height_in'] = fighters['HEIGHT'].apply(parse_inches)
    fighters['reach_in'] = fighters['REACH'].apply(parse_inches)
    fighters['weight_lbs'] = fighters['WEIGHT'].apply(parse_weight)

    # Combine names
    fighters['name'] = fighters['FIGHTER']

    # Parse DOB
    fighters['birth_date'] = pd.to_datetime(fighters['DOB'], errors='coerce')

    # Stance
    # Either Orthodox, Southpaw, or Switch
    # if none are provided, replace with NaN
    fighters['stance'] = fighters['STANCE'].replace({"": None})

    # Save info to df
    fighters_clean = fighters[[
        'name', 'height_in', 'weight_lbs', 'reach_in', 'stance', 'birth_date'
    ]]

    return fighters_clean


if __name__ == "__main__":
    df = load_fighters("data/fighters.csv")
    
    # for testing purposes
    print(df.head(20))
