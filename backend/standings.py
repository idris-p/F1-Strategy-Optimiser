import pandas as pd

# Load the driver and constructor standings from the CSV files
driver_points_df = pd.read_csv('csv/driver_cumulative_points.csv')
constructor_points_df = pd.read_csv('csv/constructor_cumulative_points.csv')

# Create helper functions to get points after any round
def get_driver_points(season, round_number, driver_abbr):
    if round_number != -1:
        row = driver_points_df[
            (driver_points_df['Season'] == season) &
            (driver_points_df['Round'] == round_number) &
            (driver_points_df['Driver'] == driver_abbr)
        ]
    else: # Get points of final standing of current season
        max_round = driver_points_df[driver_points_df['Season'] == season]['Round'].max()
        row = driver_points_df[
            (driver_points_df['Season'] == season) &
            (driver_points_df['Round'] == max_round) &
            (driver_points_df['Driver'] == driver_abbr)
        ]
    if not row.empty:
        return row['Points'].values[0]
    return None

def get_constructor_points(season, round_number, constructor_name):
    if round_number != -1:
        row = constructor_points_df[
            (constructor_points_df['Season'] == season) &
            (constructor_points_df['Round'] == round_number) &
            (constructor_points_df['Constructor'] == constructor_name)
        ]
    else: # Get points of final standing of current season
        max_round = constructor_points_df[constructor_points_df['Season'] == season]['Round'].max()
        row = constructor_points_df[
            (constructor_points_df['Season'] == season) &
            (constructor_points_df['Round'] == max_round) &
            (constructor_points_df['Constructor'] == constructor_name)
        ]
    if not row.empty:
        return row['Points'].values[0]
    return None

def get_rounds_in_season(season):
    if season == 2017:
        return 20
    rounds = driver_points_df[driver_points_df['Season'] == season]['Round'].unique()
    return len(rounds)

if __name__ == "__main__":
    print(get_rounds_in_season(2020))