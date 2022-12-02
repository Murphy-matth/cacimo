from argparse import ArgumentParser
from pathlib import Path
from csv import reader, writer
from typing import List, Tuple, Set
import os


from govenor import Governor
from govenor import compute_deads, compute_kills


def parse_csv(path: Path) -> List[Governor]:
    """
    Parses the csv located at path and returns a list of govenors.


    The csv is expected to be in the format of [gov_id, power, t4_kills, t5_kills, deads]
    """
    if not path.exists():
        raise Exception("The given path must exist in order to parse it")

    players = []

    with path.open(encoding="utf-8") as file:
        csv_reader = reader(file)

        first = True
        for row in csv_reader:
            if first:
                first = False
                continue

            def no_comma(string):
                return string.replace(",", "")

            gov = Governor(
                gov_id=float(no_comma(row[0])),
                power=float(no_comma(row[2])),
                name=row[1],
            )
            players.append(gov)

    return players
        
def main():
    parser = ArgumentParser(description="Process some csv files.")

    # Add the csv file of the first and last scans
    parser.add_argument(
        "--stats",
        help="CSV containing the stats of the govenor's to calculate the requirements for.",
        type=Path,
        required=True,
    )

    # Add the output path
    parser.add_argument(
        "--output",
        help="Where to write the output csv to",
        type=Path,
        required=True,
    )

    # Parse the arguments
    args = parser.parse_args()

    # Parse all of the csv's
    players = parse_csv(args.stats)
 
    # Write the difference to a csv
    cwd = os.getcwd()
    with open(args.output, "w", newline="", encoding="utf-8") as file:
        csv_writer = writer(file)

        # Wrie the headerss
        csv_writer.writerow([
            "Governor ID",
            "Name",
            "Power",
            "Dead Requirements",
            "Kill Requirements",
        ])

        for player in players:
            deads = compute_deads(player.power)
            kills = compute_kills(player.power)
            csv_writer.writerow([
                str(player.gov_id),
                player.name,
                str(player.power),
                str(deads),
                str(kills),
            ])

    return 0


if __name__ == "__main__":
    main()
