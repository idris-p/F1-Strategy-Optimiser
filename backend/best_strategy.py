import pandas as pd

strategy_ratings_df = pd.read_csv('csv/strategy_ratings.csv')

def get_best_strategy(season, grand_prix):
    gp = f"{grand_prix} {season}"
    print(gp)

    gp_data = strategy_ratings_df[strategy_ratings_df['GrandPrix'] == gp]
    if gp_data.empty:
        return None
    
    gp_data = gp_data.sort_values(
        by=['AvgOverperformance', 'AvgFinishPosition'],
        ascending=[False, True]
    )

    return gp_data.iloc[0]['Strategy']

if __name__ == "__main__":
    print(get_best_strategy(2018, 'Australian Grand Prix'))