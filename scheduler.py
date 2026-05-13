from ev_data import vehicles, slots, chargers
from constraints import check_power_constraint, check_unique_charger


class EVScheduler:

    def __init__(self):
        self.vehicles = list(vehicles.keys())
        self.schedule = {}

    def is_valid(self):
        return (
            check_power_constraint(self.schedule)
            and check_unique_charger(self.schedule)
        )

    def solve(self, index=0):

        if index == len(self.vehicles):
            return True

        current_ev = self.vehicles[index]

        for slot in slots:
            for charger in chargers:

                self.schedule[current_ev] = {
                    "slot": slot,
                    "charger": charger
                }

                if self.is_valid():
                    if self.solve(index + 1):
                        return True

                del self.schedule[current_ev]

        return False

    def display_schedule(self):

        print("\n========== FINAL EV CHARGING SCHEDULE ==========")

        for ev, data in self.schedule.items():
            print(
                f"{ev} --> Slot: {data['slot']} | Charger: {data['charger']}"
            )