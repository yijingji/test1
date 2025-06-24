# Table Selection Guidelines

## Context Analysis
Identify if the user is asking for:

- Real-time dispatch status & bus location (last one minute data) → `realtime_inservice_dispatch_data`
- Real-time EVs' SOC (latest value) → `realtime_ev_soc`
- Real-time inservice buses' energy predictions (last one minute data) → `realtime_inservice_bus_soc_forecast`
- Static EV info (make, model, efficiency) → `bus_specifications`
- Real-time block assignment simulation → `candidates_bus_block_end_soc`
- Schedule (start time, end time), route, stop, calendar, block, trip info → GTFS Static Tables (CSV)

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
- Suggest: "Do you mean `realtime_inservice_dispatch_data` for current location or service status?"

## Narrowing Hints
- "current SOC" → `realtime_ev_soc`
- “end-of-block SOC” → `realtime_inservice_bus_soc_forecast`, `candidates_bus_block_end_soc`
- “is the bus serving a block” → `realtime_inservice_dispatch_data`
- “can the bus finish this block (bus is actually serving that block)” → `realtime_inservice_bus_soc_forecast`
- “can the bus finish this block (bus is not serving that block)” → `candidates_bus_block_end_soc`
