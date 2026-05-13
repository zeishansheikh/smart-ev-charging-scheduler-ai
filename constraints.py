
from ev_data import vehicles, max_power_per_slot


def check_power_constraint(schedule):
    """
    Ensure total power in each slot does not exceed limit.
    """

    slot_usage = {
        "Morning": 0,
        "Afternoon": 0,
        "Evening": 0
    }

    for ev, data in schedule.items():
        slot = data["slot"]
        power = vehicles[ev]["battery_needed"]

        slot_usage[slot] += power

    for slot, total_power in slot_usage.items():
        if total_power > max_power_per_slot[slot]:
            return False

    return True


def check_unique_charger(schedule):
    """
    Prevent same charger from being used in same slot.
    """

    used = set()

    for ev, data in schedule.items():
        key = (data["slot"], data["charger"])

        if key in used:
            return False

        used.add(key)

    return True