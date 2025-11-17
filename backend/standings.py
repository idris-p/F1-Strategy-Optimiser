import pandas as pd

# Load the driver and constructor standings from the CSV files
driver_points_df = pd.read_csv('driver_cumulative_points.csv')
constructor_points_df = pd.read_csv('constructor_cumulative_points.csv')

# Create helper functions to get points after any round
def get_driver_points(season, round_number, driver_abbr):
    row = driver_points_df[
        (driver_points_df['Season'] == season) &
        (driver_points_df['Round'] == round_number) &
        (driver_points_df['Driver'] == driver_abbr)
    ]
    if not row.empty:
        return row['Points'].values[0]
    return None

def get_constructor_points(season, round_number, constructor_name):
    row = constructor_points_df[
        (constructor_points_df['Season'] == season) &
        (constructor_points_df['Round'] == round_number) &
        (constructor_points_df['Constructor'] == constructor_name)
    ]
    if not row.empty:
        return row['Points'].values[0]
    return None

print(get_driver_points(2021, 21, 'VER'))
print(get_constructor_points(2021, 10, 'Red Bull Racing'))