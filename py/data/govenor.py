from dataclasses import dataclass
from math import floor

def compute_score(gov) -> float:
    return gov.t4_kills + gov.t5_kills + (gov.deads * 10)

def compute_troops_to_delete(score: float, requirements: float) -> float:
    if score >= requirements:
        return 0

    # Floor the result as people can't delete .5 troops. Be nice and give them the extra troop
    # Deads are worth 10x kills and score is in kills so convert back
    return floor((requirements - score) / 10)

def get_requirements(power: float) -> float:
    if power >= 200000000:
        # 5M deads and 37.5M kills
        return 87500000
    elif power >= 150000000:
        # 4M deads and 33M kills
        return 73000000
    elif power >= 125000000:
        # 3M deads and 30M kills
        return 60000000
    elif power >= 100000000:
        # 2.2M deads and 22M kills
        return 44000000
    elif power >= 90000000:
        # 1.8M deads and 18M kills
        return 36000000
    elif power >= 80000000:
        # 1.35M deads and 16M kills
        return 29500000
    elif power >= 70000000:
        # 1M deads and 7.5M kills
        return 17500000
    elif power >= 60000000:
        # 800k deads and 4.5M kills
        return 12500000
    elif power >= 50000000:
        # 700k deads and 2.75M kills
        return 9750000
    else:
        # Under 50M has no requirements
        return 0


@dataclass
class Governor:
    """
    Class that holds the statistics of a player at any given point in time.

    A govenor is hashsed based upon their governor id.

    Attributes:
        gov_id: A float representing the user's governor ID. This ID is unique to every user.
        t4_kills: A float representing the user's total T4 kills.
        t5_kills: A float representing the user's total T5 kills.
        deads: A float representing the user's total deads.
        power: A float representing the user's total power.
    """

    gov_id: float = 0
    t4_kills: float = 0
    t5_kills: float = 0
    deads: float = 0
    power: float = 0
    name: str = ""

    @staticmethod
    def same(first, other) -> bool:
        return first.gov_id == other.gov_id

    def __add__(self, other):
        return Governor(self.gov_id, self.t4_kills + other.t4_kills, self.t5_kills + other.t5_kills, self.deads + other.deads, self.power, self.name)

    def difference(self, other):
        """
        Computes the stat difference between the same governor at two difference points in time.
        """
        assert self.gov_id == other.gov_id

        # Use other.name and self.power as we want the most recent name and we want the registration power of the person
        return Governor(
            self.gov_id,
            other.t4_kills - self.t4_kills,
            other.t5_kills - self.t5_kills,
            other.deads - self.deads,
            self.power,
            other.name,
        )

    @staticmethod
    def csv_headers():
        return [
            "Governor ID",
            "Name",
            "Power",
            "T4 Kills",
            "T5 Kills",
            "Deads",
            "Total Score",
            "Requirements",
            "Troops to delete",
        ]

    def as_csv_row(self):
        score = compute_score(self)
        requirements = get_requirements(self.power)
        return [
            str(self.gov_id),
            self.name,
            str(self.power),
            str(self.t4_kills),
            str(self.t5_kills),
            str(self.deads),
            str(score),
            str(requirements),
            str(compute_troops_to_delete(score, requirements)),
        ]
