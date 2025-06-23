# Embedded Business Rules

## EV Definition
- If `model` = 'BEV' in `bus_specifications`

## SOC Alerts Levels
- SOC < 10% → "critical" → Suggest to return to depot
- SOC < 40% → "low" → Dispatch caution
- SOC ≥ 40% → "normal" → Operational

## In-Service Logic

A bus is considered "in-service" if:
- It appears in `realtime_inservice_dispatch_data`
- AND `block_id` is not null, empty or “N/A”
- If no match or block is assigned, clearly state that. Do not assume a default.

## SOC Guidance Logic
- Use `candidates_bus_block_end_soc` for unassigned bus-block pairing.
- If the bus is already in-service, avoid reassigning and return:  
  “This bus is currently in service. We suggest not reassigning it to another block.”
- Energy Efficiency Definitions:
  Energy efficiency = energy used / miles driven. Unit: kWh/mile. 
  Manufacturer-estimated energy efficiency = bus_specifications.energy_efficiency. Unit: kWh/mile. This is a reference value, not real-time.
  Current energy efficiency = realtime_inservice_bus_soc_forecast.avg_kwh_mile. Unit: kWh/mile. This is based on real-time bus data.

- Remaining Miles Definitions:
  Remaining miles of the in-service bus = realtime_inservice_bus_soc_forecast.current_range. Unit: mile. 
  Remaining miles of the in-service block = realtime_inservice_bus_soc_forecast.left_miles. Unit: mile.

## Location Logic
- Real-time location: `realtime_inservice_dispatch_data`.lat, `realtime_inservice_dispatch_data`.lon
- If the bus has no location data in `realtime_inservice_dispatch_data`, just clarify that "There is no data available."

## No Data
- No Data means: Query return empty string or [] or row_count = 0
- No in-service data, could reply: "bus is not inservice"
- No location data, could reply: "There is no location data for the bus"
- No prediction data, could reply: "There is no prediction data for the bus"
- No dispatch suggestion data, could reply: "There is no suggested predictin data for the bus"
- No GTFS data, could reply: "There is no matched GTFS data"

## Table Use Routing

| Intent                     | Use Table(s)                                |
|---------------------------|----------------------------------------------|
| Real-time status          | `realtime_inservice_dispatch_data`           |
| Energy range prediction   | `realtime_inservice_bus_soc_forecast`        |
| Assignment decision       | `candidates_bus_block_end_soc`               |
| Vehicle specs             | `bus_specifications`                         |
| Schedule/topology/fare    | GTFS static files (`trips.csv`, etc.)        |
