from argparse import ArgumentParser
from pathlib import Path
from csv import reader, writer
from typing import List, Tuple, Set
import os


from govenor import Governor


def parse_csv(path: Path) -> List[Governor]:
    """
    Parses the csv located at path and returns a list of govenors.


    The csv is expected to be in the format of [gov_id, power, t4_kills, t5_kills, deads]
    """
    if not path.exists():
        raise Exception("The given path must exist in order to parse it")

    players = []

    with path.open() as file:
        csv_reader = reader(file)

        for row in csv_reader:
            # Each row is read in as a list of strings
            # in the format [gov_id, power, t4_kills, t5_kills, deads]
            assert len(row) == 5

            def no_comma(string):
                return string.replace(",", "")

            gov = Governor(
                gov_id=float(no_comma(row[0])),
                t4_kills=float(no_comma(row[2])),
                t5_kills=float(no_comma(row[3])),
                deads=float(no_comma(row[4])),
                power=float(no_comma(row[1])),
            )
            players.append(gov)

    return players


def calculate_difference(
    before: List[Governor], after: List[Governor]
) -> Tuple[List[Governor], Set[float]]:
    """
    Calculates the difference between two govenors.

    Returns a list of the difference between the stats from the govenors in the before
    list and the govenors in the after list. Also returns a list of the govenors ids that
    are only contained in one list.
    """
    if len(before) != len(after):
        print(
            "The length of the two csv's is not the same, some govemors will be skipped"
        )

    difference = []

    # Get a set of the govenor ids so we can preform a set intersection / difference
    before_ids = set([gov.gov_id for gov in before])
    after_ids = set([gov.gov_id for gov in after])

    # First compute the set difference to see who we can not find
    not_found = before_ids.symmetric_difference(after_ids)

    # Compute the set intersection so we know who to look for
    intersection = before_ids.intersection(after_ids)

    # Make sure we have everyone
    assert len(before) + len(after) == (len(intersection) * 2) + len(not_found)

    def get_gov(gov_list, id):
        for g in gov_list:
            if id == g.gov_id:
                return g
        raise Exception("Goveneor must be found")

    for id in intersection:
        prev = get_gov(before, id)
        latter = get_gov(after, id)

        difference.append(prev.difference(latter))

    return difference, not_found


def main():
    parser = ArgumentParser(description="Process some csv files.")

    # Add the csv file of the first and last scan
    parser.add_argument(
        "--before",
        help="A csv containing the data from the first scan",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--after",
        help="A csv containing the data from the last scan",
        type=Path,
        required=True,
    )

    # Parse the arguments
    args = parser.parse_args()

    before_players = parse_csv(args.before)
    after_players = parse_csv(args.after)

    difference, not_found = calculate_difference(before_players, after_players)

    cwd = os.getcwd()
    
    # Write the difference to a csv
    with open(Path(cwd) / 'output.csv', 'w', newline='') as file:
        csv_writer = writer(file)
        
        # Wrie the headerss
        csv_writer.writerow(['Governor ID', 'T4 Kills', 'T5 Kills', 'Deads', 'Power'])

        for player in difference:
            csv_writer.writerow(player.as_csv_row())

    return 0


if __name__ == "__main__":
    main()
