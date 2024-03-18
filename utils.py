def map_time_to_period(time_slots):
    periods = {
        "Mañana": (0, 12),   
        "Tarde": (12, 18), 
        "Noche": (18, 24) 
    }

    time_ranges = time_slots.split(", ")
    
    day_periods = set()

    for time_range in time_ranges:
        if not time_range:
            continue
        start_time, end_time = time_range.split("-")
        start_hour = int(start_time.split(":")[0])
        end_hour = int(end_time.split(":")[0])

        for period, (start, end) in periods.items():
            if start_hour < end and end_hour > start:  
                day_periods.add(period)

    return list(day_periods)