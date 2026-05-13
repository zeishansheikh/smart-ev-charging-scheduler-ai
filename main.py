from scheduler import EVScheduler
from ev_data import vehicles


def show_vehicle_data():

    print("========== EV VEHICLE DATA ==========")

    for ev, data in vehicles.items():
        print(
            f"{ev} --> Battery Needed: {data['battery_needed']} kWh | Preferred Slot: {data['preferred_slot']}"
        )


show_vehicle_data()

scheduler = EVScheduler()

result = scheduler.solve()

if result:
    scheduler.display_schedule()
else:
    print("No valid charging schedule found.")