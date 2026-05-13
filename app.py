import streamlit as st
import pandas as pd
from scheduler import EVScheduler
import ev_data

# Set page config for a premium wide layout
st.set_page_config(page_title="Smart EV Scheduler AI", page_icon="⚡", layout="wide")

# Custom CSS for a premium dark mode aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #00E676;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #69F0AE;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #333;
        padding-bottom: 5px;
    }
    .metric-card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        text-align: center;
        border-top: 4px solid #00E676;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00C853 0%, #B2FF59 100%);
        color: #121212;
        font-size: 18px;
        font-weight: 900;
        border-radius: 8px;
        padding: 12px 24px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 200, 83, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 200, 83, 0.6);
        color: #000;
    }
    .schedule-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 6px solid #00E676;
        background: linear-gradient(145deg, #262730, #1e1e24);
        box-shadow: 2px 4px 10px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    .schedule-card:hover {
        transform: scale(1.02);
    }
    .ev-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #fff;
    }
    .ev-detail {
        font-size: 1rem;
        color: #B0BEC5;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ Smart EV Scheduler AI</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #B0BEC5; font-size: 1.2rem;'>Intelligent Charging Optimization & Constraint Satisfaction</p>", unsafe_allow_html=True)
st.markdown("---")

# Tabs configuration
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard & Data", "⚙️ Constraints Settings", "🚀 AI Scheduler", "⏱️ Find Free Slot"])

with tab1:
    st.markdown('<div class="sub-header">Current Vehicle Data</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Convert vehicle data to DataFrame for an elegant table view
        df_vehicles = pd.DataFrame.from_dict(ev_data.vehicles, orient='index')
        df_vehicles.index.name = "Vehicle ID"
        df_vehicles.rename(columns={"battery_needed": "Battery Needed (kWh)", "preferred_slot": "Preferred Slot"}, inplace=True)
        st.dataframe(df_vehicles, use_container_width=True)
    
    with col2:
        st.info("💡 The AI Scheduler acts as a constraint satisfaction engine. It will assign each vehicle to an available charger and time slot without exceeding the grid limits.")
        st.metric(label="Total Vehicles to Charge", value=len(ev_data.vehicles))
        st.metric(label="Total Chargers Available", value=len(ev_data.chargers))
        
    st.markdown('<div class="sub-header">Available Time Slots & Grid Power Limits</div>', unsafe_allow_html=True)
    df_power = pd.DataFrame(list(ev_data.max_power_per_slot.items()), columns=["Time Slot", "Max Power Limit (kWh)"])
    st.dataframe(df_power, hide_index=True, use_container_width=True)

with tab2:
    st.markdown('<div class="sub-header">Edit Dynamic Grid Constraints</div>', unsafe_allow_html=True)
    st.write("Modify the maximum power allowed per time slot to simulate varying grid capacities. (Changes apply to the current session)")
    
    col_m, col_a, col_e = st.columns(3)
    with col_m:
        ev_data.max_power_per_slot["Morning"] = st.number_input("🌅 Morning Limit (kWh)", value=ev_data.max_power_per_slot["Morning"], step=5)
    with col_a:
        ev_data.max_power_per_slot["Afternoon"] = st.number_input("☀️ Afternoon Limit (kWh)", value=ev_data.max_power_per_slot["Afternoon"], step=5)
    with col_e:
        ev_data.max_power_per_slot["Evening"] = st.number_input("🌙 Evening Limit (kWh)", value=ev_data.max_power_per_slot["Evening"], step=5)
        
    st.success("✅ Constraints are actively synchronized with the scheduling engine.")

with tab3:
    st.markdown('<div class="sub-header">Generate Optimal Charging Schedule</div>', unsafe_allow_html=True)
    
    # Center the button
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        run_engine = st.button("🧠 Run AI Scheduling Engine", use_container_width=True)
    
    if run_engine:
        with st.spinner("Calculating optimal schedule using backtracking constraint satisfaction..."):
            scheduler = EVScheduler()
            result = scheduler.solve()
            
            if result:
                st.balloons()
                st.success("✅ Optimal Schedule Successfully Generated!")
                
                # Group by Slot for a stunning timeline presentation
                schedule_df = pd.DataFrame.from_dict(scheduler.schedule, orient='index').reset_index()
                schedule_df.columns = ['Vehicle', 'Slot', 'Charger']
                
                slots = ev_data.slots
                cols = st.columns(len(slots))
                
                for i, slot in enumerate(slots):
                    with cols[i]:
                        st.markdown(f"<h3 style='text-align: center; color: #00E676;'>{slot}</h3>", unsafe_allow_html=True)
                        slot_data = schedule_df[schedule_df['Slot'] == slot]
                        if slot_data.empty:
                            st.info("No vehicles scheduled.")
                        else:
                            for _, row in slot_data.iterrows():
                                vehicle_name = row['Vehicle']
                                battery = ev_data.vehicles[vehicle_name]['battery_needed']
                                charger = row['Charger']
                                st.markdown(f"""
                                <div class="schedule-card">
                                    <div class="ev-title">🚗 {vehicle_name}</div>
                                    <div class="ev-detail">🔋 {battery} kWh</div>
                                    <div class="ev-detail">🔌 Assigned: {charger}</div>
                                </div>
                                """, unsafe_allow_html=True)
                
                st.markdown('<div class="sub-header">Raw Schedule Data</div>', unsafe_allow_html=True)
                st.dataframe(schedule_df, hide_index=True, use_container_width=True)
            else:
                st.error("❌ No valid schedule found. Grid constraints violated or insufficient chargers. Try increasing power limits in the 'Constraints Settings' tab.")

with tab4:
    st.markdown('<div class="sub-header">Find a Free Slot (Zero Wait Time)</div>', unsafe_allow_html=True)
    st.write("Enter your car name and battery requirement to instantly find out when a charger is free for you.")
    
    col_name, col_bat = st.columns(2)
    with col_name:
        new_car_name = st.text_input("Car Name (e.g., EV5)")
    with col_bat:
        new_bat = st.number_input("Battery Needed (kWh)", min_value=1, value=20)
        
    if st.button("Check Availability", use_container_width=True):
        if not new_car_name:
            st.warning("Please enter a Car Name.")
        else:
            with st.spinner("Analyzing current schedule..."):
                scheduler = EVScheduler()
                result = scheduler.solve()
                
                if result:
                    # Calculate used power and chargers per slot
                    slot_usage = {s: 0 for s in ev_data.slots}
                    chargers_used = {s: 0 for s in ev_data.slots}
                    
                    for ev, data in scheduler.schedule.items():
                        slot = data['slot']
                        power = ev_data.vehicles[ev]['battery_needed']
                        slot_usage[slot] += power
                        chargers_used[slot] += 1
                        
                    # Find available slots for the new car
                    available_slots = []
                    for slot in ev_data.slots:
                        rem_power = ev_data.max_power_per_slot[slot] - slot_usage[slot]
                        rem_chargers = len(ev_data.chargers) - chargers_used[slot]
                        
                        if rem_power >= new_bat and rem_chargers > 0:
                            available_slots.append({
                                "slot": slot,
                                "rem_chargers": rem_chargers,
                                "rem_power": rem_power
                            })
                    
                    if available_slots:
                        st.success(f"🎉 Hello {new_car_name}! You don't have to wait. You can come during these slots:")
                        for info in available_slots:
                            st.markdown(f"""
                            <div class="schedule-card" style="border-left: 6px solid #B2FF59;">
                                <div class="ev-title">🕒 {info['slot']}</div>
                                <div class="ev-detail">🔌 Available Chargers: {info['rem_chargers']}</div>
                                <div class="ev-detail">⚡ Remaining Power: {info['rem_power']} kWh</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("😔 Sorry, all slots are currently fully booked or don't have enough power for your requirement. Please check back later or adjust grid limits.")
                else:
                    st.error("❌ Current schedule is invalid or fully overloaded, cannot determine free slots.")