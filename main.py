from mcp.server.fastmcp import FastMCP
import pandas as pd
from load_fighters import load_fighters
from load_fights import load_fights
from load_fight_stats import load_fight_stats

# Load in cleaned CSVs using scripts
fighters_df = load_fighters("data/fighters.csv")
fights_df = load_fights("data/fights.csv")
fight_stats_df = load_fight_stats("data/fight_stats.csv")

mcp = FastMCP("mma-analytics-ufc", json_response=True)

# Helper to get stats
def get_fighter_stats(name: str):
    df = fight_stats_df[fight_stats_df['FIGHTER'].str.lower() == name.lower()].copy()
    if df.empty:
        return None

    # Combine into a single dict to make it look prettier
    return {
        "KD": df['KD'].sum(),
        "TD_landed": df['TD_landed'].sum(),
        "TD_attempted": df['TD_attempted'].sum(),
        "CTRL": df['CTRL'].sum(),
        "SIG STR PCT": df['SIG STR_landed'].sum() / df['SIG STR_attempted'].sum(),
        "TOTAL STR_landed" : df['TOTAL STR_landed'].sum(),
        "SUB ATT": df['SUB ATT'].sum(),
        "DISTANCE": df['DISTANCE'].sum()
    }

# Helper logic for summaries
def compute_fighter_summary(fighter_name: str) -> dict:
    """
    Get the fighter's basic summary
    """
    stats = get_fighter_stats(fighter_name)
    if stats is None or stats.empty:
        return {"error": f"{fighter_name} not found"}

    return {    
        "Name": fighter_name,
        "Total fights": len(stats),
        "Significant strike percent": stats['SIG STR PCT'],
        "Takedown percent" : stats['TD_landed'] / stats['TD_attempted'],
        'Knockdowns' : stats['KD'],
        'Control Time (seconds)' : stats['CTRL']
    }

# These functions with the @mcp.tool() header are the tools we can call from the client side
@mcp.tool()
def fighter_summary(fighter_name: str) -> dict:
    """
    Returning the formatted fighter summary
    """
    return compute_fighter_summary(fighter_name)

@mcp.tool()
def compare_fighters(fighter1: str, fighter2: str) -> dict:
    """
    Returning the formatted fighter summary for two fighters
    """
    return {
        fighter1: compute_fighter_summary(fighter1),
        fighter2: compute_fighter_summary(fighter2),
    }

@mcp.tool()
def calculate_betting_odds(fighter1_name: str, fighter2_name: str) -> dict:
    """
    I asked ChatGPT to make a simple method to calculate betting odds and it
    gave me a basic frame that I built upon.

    fighter1 and fighter2 are dict keys

    From fight stats:
    - SIG STR PCT
    - KD
    - TD_landed
    - CTRL
    - SUB_ATT
    - GROUND
    - DISTANCE
    """
    # Get fighter info
    fighter1 = get_fighter_stats(fighter1_name)
    fighter2 = get_fighter_stats(fighter2_name)

    # The favored fighter will have a higher number
    # Base odds
    prob = 0.50
    # Fighter's edge
    edge = 0.0
    
    # Striking accuracy
    acc_diff = fighter1['SIG STR PCT'] - fighter2['SIG STR PCT']
    if acc_diff > 5:
        edge += 0.05
    elif acc_diff < -5:
        edge -= 0.05

    # Knockdowns
    kd_diff = fighter1["KD"] - fighter2["KD"]
    if kd_diff >= 0.5:
        edge += 0.05
    elif kd_diff <= -0.5:
        edge -= 0.05

    # Grappling control 
    ctrl_diff = fighter1["CTRL"] - fighter2["CTRL"]
    td_diff = fighter1["TD_landed"] - fighter2["TD_landed"]

    if ctrl_diff > 60 or td_diff >= 1:
        edge += 0.05
    elif ctrl_diff < -60 or td_diff <= -1:
        edge -= 0.05

    # 4. Strike volume edge (pressure / pace)
    vol_diff = fighter1["TOTAL STR_landed"] - fighter2["TOTAL STR_landed"]
    if vol_diff >= 10:
        edge += 0.03
    elif vol_diff <= -10:
        edge -= 0.03

    # 5. Submission threat
    sub_diff = fighter1["SUB ATT"] - fighter2["SUB ATT"]
    if sub_diff >= 1:
        edge += 0.03
    elif sub_diff <= -1:
        edge -= 0.03

    # 6. Distance preference
    distance_diff = fighter1["DISTANCE"] - fighter2["DISTANCE"]
    if distance_diff >= 0.10:
        edge += 0.02
    elif distance_diff <= -0.10:
        edge -= 0.02

    # Creating an edge for each fighter
    f1_edge = prob + edge
    f2_edge = prob - edge * 0.85

    return {
        fighter1_name: probability_to_odds(f1_edge),
        fighter2_name: probability_to_odds(f2_edge)
    }


# Helper methods
def probability_to_odds(prob: float) -> int:
    if prob == 0.5:
        return 100

    if prob > 0.5:
        return int(-108 * prob / (1 - prob))
    else:
        return int(108 * (1 - prob) / prob)


# Asked ChatGPT to make this method
def ctrl_to_seconds(ctrl):
    if ctrl in ("---", "0:00", 0, 0.0):
        return 0
    ctrl_str = str(ctrl)
    if ":" not in ctrl_str:
        return 0
    m, s = ctrl_str.split(":")
    return int(m) * 60 + int(s)



if __name__ == "__main__":
    mcp.run(transport="streamable-http")