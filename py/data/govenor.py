from dataclasses import dataclass

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

    def difference(self, other):
        """
        Computes the stat difference between the same governor at two difference points in time.
        """
        assert self.gov_id == other.gov_id
        return Governor(self.gov_id, other.t4_kills - self.t4_kills, other.t5_kills - self.t5_kills, other.deads - self.deads, self.power)

    def as_csv_row(self):
        return [str(self.gov_id), str(self.t4_kills), str(self.t5_kills), str(self.deads), str(self.power)]
