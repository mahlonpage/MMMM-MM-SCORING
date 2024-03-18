import os

FOLDER_PATH = "./brackets"
SEEDS = {}

# Increment scoring based on tournament depth
def get_round_value(game_number):
    if game_number < 32: return 1
    if game_number < 48: return 2
    if game_number < 56: return 4
    if game_number < 60: return 8
    if game_number < 62: return 16
    if game_number < 63: return 32

# Error if the bracket is invalid.
def validate_bracket(bracket):
    for pick in bracket:
        if pick[0] not in {"E", "S", "W", "M"}:
            print(f"{pick} is invalid.")
        if get_seed(pick) > 16 or get_seed(pick) < 1:
            print(f"{pick} is invalid. {get_seed(pick)}")

def get_seed(pick):
    return int(pick[1:])

# Calculates the score for a bracket
def score_bracket(predicted_results, actual_results):
    score = 0
    for i, (pick, result) in enumerate(zip(predicted_results, actual_results)):
        if pick == result:
            score += get_seed(pick) * get_round_value(i)
    return score

# Get all the bracket files from folder.
def get_bracket_files():
    files = [f for f in os.listdir(FOLDER_PATH) if f.endswith('.txt')]
    return files

# Read in a bracket from file.
def read_bracket_from_file(file_path):
    with open(file_path, 'r') as file:
        bracket_data = [line.strip() for line in file]
    return bracket_data

# Score all brackets and print results so far.
def main():
    files = get_bracket_files()
    brackets = []

    for file in files:
        file_path = os.path.join(FOLDER_PATH, file)
        bracket_data = read_bracket_from_file(file_path)
        name = file[:-4]

        # Validate bracket
        validate_bracket(bracket_data)

        brackets.append((name, bracket_data))

    actual_results = read_bracket_from_file("true_bracket.txt")

    # Score brackets
    scored_brackets = []
    for name, cur_bracket_data in brackets:
        score = score_bracket(cur_bracket_data, actual_results)
        scored_brackets.append((name, score))

    # Print winners in order with scores
    scored_brackets.sort(key=lambda x: x[1], reverse=True)
    for file, score in scored_brackets:
        print(f"{file}: {score}")

if __name__ == "__main__":
    main()