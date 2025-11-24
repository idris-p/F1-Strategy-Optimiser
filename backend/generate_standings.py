import pandas as pd
import fastf1, datetime

fastf1.Cache.enable_cache("cache")
current_datetime = datetime.datetime.now()

# --- Standard F1 points by finishing position ---
points = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
sprint_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
sprint_points_2021 = {1: 3, 2: 2, 3: 1}

# --- DataFrames to store cumulative points ---
driver_points_df = pd.DataFrame()
constructor_points_df = pd.DataFrame()

# --- Loop through seasons and races ---
for year in range(2018, current_datetime.year + 1):
    print(f"Processing season {year}...")
    schedule = fastf1.get_event_schedule(year)
        
    driver_cumulative = {}
    constructor_cumulative = {}
    
    for _, event in schedule.iterrows():
        if event['EventFormat'] == 'testing':
            continue
        try:
            session = fastf1.get_session(year, event['EventName'], 'Race')
            session.load()
        except Exception as e:
            print(f"Failed to load {event['EventName']} {year}: {e}")
            continue
        
        results = session.results.fillna('')
        round_number = event['RoundNumber']
        race_name = event['EventName']

        # Check for half points
        half_points = False
        if year == 2021 and race_name == "Belgian Grand Prix":
            half_points = True
        
        # Determine top 10 for fastest lap eligibility
        results['PositionNumeric'] = pd.to_numeric(results['Position'], errors='coerce')

        # Now safely get top 10 finishers
        top_10 = results[results['PositionNumeric'] <= 10]['Abbreviation'].tolist()
        
        # Determine fastest lap
        fastest_lap_driver = None
        if 2019 <= year <= 2024:  # only award fastest lap points up to 2024
            try:
                fastest_lap_driver = session.laps.pick_fastest()['Driver']
            except Exception:
                fastest_lap_driver = None

        # --- Check for a sprint session and award sprint points if present ---
        sprint_results = None
        # try common sprint session names; most relevant is 'Sprint'
        for sprint_name in ['Sprint', 'SprintShootout', 'Sprint Shootout']:
            try:
                sprint_sess = fastf1.get_session(year, event['Location'], sprint_name)
                sprint_sess.load()
                sprint_results = sprint_sess.results.fillna('')
                break
            except Exception:
                sprint_results = None

        if sprint_results is not None:
            sprint_results['PositionNumeric'] = pd.to_numeric(sprint_results['Position'], errors='coerce')
            for _, srow in sprint_results.iterrows():
                spos = srow['PositionNumeric']
                if pd.isna(spos):
                    continue
                if year == 2021:
                    # 2021 sprint points to top 3 only
                    if spos <= 3:
                        d = srow['Abbreviation']
                        t = srow['TeamName']
                        sp = sprint_points_2021.get(int(spos), 0)
                        driver_cumulative[d] = driver_cumulative.get(d, 0) + sp
                        constructor_cumulative[t] = constructor_cumulative.get(t, 0) + sp
                else:
                    # award sprint points to top 8
                    if spos <= 8:
                        d = srow['Abbreviation']
                        t = srow['TeamName']
                        sp = sprint_points.get(int(spos), 0)
                        driver_cumulative[d] = driver_cumulative.get(d, 0) + sp
                        constructor_cumulative[t] = constructor_cumulative.get(t, 0) + sp

        # Update driver and constructor cumulative points from the race
        for _, row in results.iterrows():
            pos = row['PositionNumeric']
            if pd.isna(pos):
                continue 
            driver = row['Abbreviation']
            team = row['TeamName']
            
            base_points = points.get(int(pos), 0)
            
            if half_points:
                base_points *= 0.5
            
            # Add fastest lap point if eligible
            if driver == fastest_lap_driver and driver in top_10:
                base_points += 1
            
            driver_cumulative[driver] = driver_cumulative.get(driver, 0) + base_points
            constructor_cumulative[team] = constructor_cumulative.get(team, 0) + base_points

        # If it is round 5 of 2020, deduct 15 points from Racing Point
        if year == 2020 and round_number == 5:
            constructor_cumulative['Racing Point'] = constructor_cumulative.get('Racing Point', 0) - 15
        
        # Save cumulative points after this round
        driver_points_df = pd.concat([
            driver_points_df,
            pd.DataFrame({
                'Season': year,
                'Round': round_number,
                'Driver': list(driver_cumulative.keys()),
                'Points': list(driver_cumulative.values())
            })
        ], ignore_index=True)
        
        constructor_points_df = pd.concat([
            constructor_points_df,
            pd.DataFrame({
                'Season': year,
                'Round': round_number,
                'Constructor': list(constructor_cumulative.keys()),
                'Points': list(constructor_cumulative.values())
            })
        ], ignore_index=True)

# Manually insert the final standings for 2017
final_2017_driver_points = {
    'HAM': 363, 'VET': 317, 'BOT': 305, 'RAI': 205, 'RIC': 200,
    'VER': 168, 'PER': 100, 'OCO': 87, 'SAI': 54, 'HUL': 43,
    'MAS': 43, 'STR': 40, 'GRO': 28, 'MAG': 19, 'ALO': 17,
    'VAN': 13, 'PAL': 8, 'WEH': 5, 'KVY': 5
}
final_2017_constructor_points = {
    'Mercedes': 668, 'Ferrari': 522, 'Red Bull Racing': 368, 'Force India': 187,
    'Williams': 83, 'Renault': 57, 'Toro Rosso': 53, 'Haas F1 Team': 47,
    'McLaren': 30, 'Sauber': 5
}
for driver, pts in final_2017_driver_points.items():
    driver_points_df = pd.concat([
        driver_points_df,
        pd.DataFrame({
            'Season': 2017,
            'Round': 20,
            'Driver': [driver],
            'Points': [pts]
        })
    ], ignore_index=True)

for constructor, pts in final_2017_constructor_points.items():
    constructor_points_df = pd.concat([
        constructor_points_df,
        pd.DataFrame({
            'Season': 2017,
            'Round': 20,
            'Constructor': [constructor],
            'Points': [pts]
        })
    ], ignore_index=True)

# --- Sort tables ---
driver_points_df = driver_points_df.sort_values(['Season','Round','Points'], ascending=[True,True,False]).reset_index(drop=True)
constructor_points_df = constructor_points_df.sort_values(['Season','Round','Points'], ascending=[True,True,False]).reset_index(drop=True)


driver_points_df.to_csv("csv/driver_cumulative_points.csv", index=False)
constructor_points_df.to_csv("csv/constructor_cumulative_points.csv", index=False)