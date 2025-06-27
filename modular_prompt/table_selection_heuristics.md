# Table Selection Guidelines

## Context Analysis
Identify if the user is asking for:

- Real-time dispatch status & bus location (last one minute data) → `realtime_cad_avl_data`
- Real-time EVs' SOC → `realtime_ev_telematics`
- Real-time inservice buses' energy predictions (last one minute data) → `realtime_forecast_of_inservice_bus_soc`
- Static EV info (make, model, efficiency) → `bus_specifications`
- Real-time block assignment simulation → `candidates_bus_block_end_soc`
- Schedule (start time, end time), route, stop, calendar, block, trip info → GTFS Static Tables (CSV)
- Historical analysis of driving behavior and energy efficiency → `historical_inservice_trip_statistics` for trip level, `historical_inservice_block_statistics` for block level

## GTFS Static Tables Use Cases

| Question Type             | Use CSV(s)                         |
|--------------------------|-------------------------------------|
| Route to trip mapping     | `trips.csv`, `routes.csv`           |
| Trip to stop sequence     | `stop_times.csv`, `stops.csv`       |
| Service calendars         | `calendar.csv`, `calendar_dates.csv`|
| Fare details              | `fare_rules.csv`, `fare_attributes.csv`|
| GPS path (geometry)       | `shapes.csv`                        |
| Transfers and frequencies | `transfers.csv`, `frequencies.csv` |

## Fallback Logic
If unsure which table to use:
- Ask: "Are you looking for real-time status, energy prediction, or static vehicle data?"
- Suggest: "Do you mean `realtime_cad_avl_data` for current location or service status?"

## Narrowing Hints
- "manufacturer", "model", "battery_capacity" → `bus_specifications`
- "current SOC" → `realtime_ev_telematics`
- “end-of-block SOC” → `realtime_forecast_of_inservice_bus_soc`, `candidates_bus_block_end_soc`
- “is the bus serving a block” → `realtime_cad_avl_data`
- “can the bus finish this block (bus is actually serving that block)” → `realtime_forecast_of_inservice_bus_soc`
- “can the bus finish this block (bus is not serving that block)” → `candidates_bus_block_end_soc`
- "historical", "last week", "this month" → `historical_inservice_trip_statistics`, `historical_inservice_block_statistics`
