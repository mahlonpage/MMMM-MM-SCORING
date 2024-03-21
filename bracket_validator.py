import os
import pandas as pd
from mapping import ROSETTA_STONE, GAMES

def seed_checker(df, games, seeds):
    #games = [0, 8, 16, 24]
    df = df.map(lambda x: x[1])
    # Extract the column index from the game name
    for game in games:
        # Check if the number in each row is either 1 or 16
        info = df.iloc[:, game]

        valid_numbers = info.isin(seeds)

        # Check if any value is False (indicating invalid entry)
        if not valid_numbers.all():
            print(f"Error in {game} with seeding")

def letter_checker(df, games, letters):
    df = df.map(lambda x: x[0])

    for game in games:
        info = df.iloc[:, game]

        valid_letters = info.isin(letters)

        if not valid_letters.all():
            print(f"Error in {game} with lettering")

def cant_pick_unpicked_past(df, goal, feed1, feed2):
    for index, row in df.iterrows():
        # Check if column A is not equivalent to either column B or column C
        if row.iloc[goal] != row.iloc[feed1] and row.iloc[goal] != row.iloc[feed2]:
            print(f"There's a mistake in row {index} with game {goal}: {row.iloc[goal]} != {row.iloc[feed1]} or {row.iloc[feed2]}")

def all_checks(df):
    # First round correct seed wins
    seed_checker(df, [0,8,16,24], [1,16])
    seed_checker(df, [1,9,17,25], [8,9])
    seed_checker(df, [2,10,18,26], [5,12])
    seed_checker(df, [3,11,19,27], [4,13])
    seed_checker(df, [4,12,20,28], [6,11])
    seed_checker(df, [5,13,21,29], [3,14])
    seed_checker(df, [6,14,22,30], [7,10])
    seed_checker(df, [7,15,23,31], [2,15])

    # Second round correct seed wins
    seed_checker(df, [32,36,40,44], [1,16,8,9])
    seed_checker(df, [33,37,41,45], [5,12,4,13])
    seed_checker(df, [34,38,42,46], [6,11,3,14])
    seed_checker(df, [35,39,43,47], [7,10,2,15])

    # Third round correct seed wins
    seed_checker(df, [48,50,52,54], [1,16,8,9,5,12,4,13])
    seed_checker(df, [49,51,53,55], [6,11,3,14,7,10,2,15])

    # Fourth round correct seed wins
    seed_checker(df, [56,57,58,59,60,61,62], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

    # Proper lettering
    letter_checker(df, [0,1,2,3,4,5,6,7,32,33,34,35,48,49,56], ["E"])
    letter_checker(df, [8,9,10,11,12,13,14,15,36,37,38,39,50,51,57], ["W"])
    letter_checker(df, [16,17,18,19,20,21,22,23,40,41,42,43,52,53,58], ["S"])
    letter_checker(df, [24,25,26,27,28,29,30,31,44,45,46,47,54,55,59], ["M"])
    letter_checker(df, [60], ["E", "W"])
    letter_checker(df, [61], ["S", "M"])
    letter_checker(df, [62], ["E", "S", "M", "W"])

    # Second round comes from first
    cant_pick_unpicked_past(df,32,0,1)
    cant_pick_unpicked_past(df,33,2,3)
    cant_pick_unpicked_past(df,34,4,5)
    cant_pick_unpicked_past(df,35,6,7)
    cant_pick_unpicked_past(df,36,8,9)
    cant_pick_unpicked_past(df,37,10,11)
    cant_pick_unpicked_past(df,38,12,13)
    cant_pick_unpicked_past(df,39,14,15)
    cant_pick_unpicked_past(df,40,16,17)
    cant_pick_unpicked_past(df,41,18,19)
    cant_pick_unpicked_past(df,42,20,21)
    cant_pick_unpicked_past(df,43,22,23)
    cant_pick_unpicked_past(df,44,24,25)
    cant_pick_unpicked_past(df,45,26,27)
    cant_pick_unpicked_past(df,46,28,29)
    cant_pick_unpicked_past(df,47,30,31)

    # Third round comes from second
    cant_pick_unpicked_past(df,48,32,33)
    cant_pick_unpicked_past(df,49,34,35)
    cant_pick_unpicked_past(df,50,36,37)
    cant_pick_unpicked_past(df,51,38,39)
    cant_pick_unpicked_past(df,52,40,41)
    cant_pick_unpicked_past(df,53,42,43)
    cant_pick_unpicked_past(df,54,44,45)
    cant_pick_unpicked_past(df,55,46,47)

    # Fourth round comes from third
    cant_pick_unpicked_past(df,56,48,49)
    cant_pick_unpicked_past(df,57,50,51)
    cant_pick_unpicked_past(df,58,52,53)
    cant_pick_unpicked_past(df,59,54,55)

    # Fifth round comes from fourth
    cant_pick_unpicked_past(df,60,56,57)
    cant_pick_unpicked_past(df,61,58,59)

    # Sixth round comes from fifth
    cant_pick_unpicked_past(df,62,60,61)

def load_df():
    folder_path = './brackets'

    data = []

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  # Ensure we're only reading text files
            # Skip the best and worst files
            if filename == "BEST SEEDS.txt" or filename ==  "WORST SEEDS.txt":
                continue

            file_path = os.path.join(folder_path, filename)

            # Read each line from the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Check if the file has exactly 63 lines
            if len(lines) != 63:
                print(f"Skipping {filename}. Expected 63 lines, found {len(lines)}.")
                continue

            # Extract letter and number pairs from each line
            file_data = []
            for line in lines:
                letter, number = line.strip()[:1], line.strip()[1:]
                file_data.append((letter, int(number)))

            # Append file data to the main list
            data.append(file_data)

    df = pd.DataFrame(data, columns=GAMES)

    return df

def print_stats(df):
    for col in df.columns:
        # Get unique values and their counts for the current column
        value_counts = df[col].value_counts()

        # Print column name
        print(f"{col}:")

        # Print distinct entries and their counts
        for value, count in value_counts.items():
            seed = str(value[1])
            if len(seed) == 1: seed = " " + seed

            num_picks = str(count)
            if len(num_picks) == 1: num_picks = " " + num_picks
            print(f"\t[{seed}] {ROSETTA_STONE[value]} : {num_picks}\t({round((count / sum(value_counts) * 100), 3)}%)")

def main():
    df = load_df()
    all_checks(df)
    #print_stats(df)

if __name__ == "__main__":
    main()