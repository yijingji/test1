# Embedded Business Rules

## EV Definition
- If `model` = 'BEV' in `bus_specifications`

## SOC Alerts
- SOC < 10% → "critical"
- SOC < 40% → "low"
- SOC ≥ 40% → "normal"

## In-Service Rule
- A bus is considered in-service if `block_id` in `realtime_inservice_dispatch_data` is not NULL, N/A, or empty.

## SOC Guidance Logic
- Use `realtime_inservice_bus_soc_forecast` if the bus is currently in-service.
- Use `candidates_bus_block_end_soc` for unassigned bus-block pairing.
- If the bus is already in-service, avoid reassigning and return:  
  “This bus is currently in service. We suggest not reassigning it to another block.”
- Energy Efficiency Definitions:
  Energy efficiency = energy used / miles driven. Unit: kWh/mile. 
  Manufacturer-estimated energy efficiency = bus_specifications.energy_efficiency. Unit: kWh/mile. This is a reference value, not real-time.
  Current energy efficiency = realtime_inservice_bus_soc_forecast.avg_kwh_mile. Unit: kWh/mile. This is based on real-time bus data.

- Remaining Miles Definitions:
  Remaining miles of the in-service bus = realtime_inservice_bus_soc_forecast.current_range. Unit: mile. 
  Remaining miles of the in-service block = 
    1. find out the EVs that are not inservice
    2. search candidates_bus_block_end_soc.remaining_block_miles where bus_id = not inservice EVs' id and block_id = in-service block




## SOC Alert Levels

- SOC < 10% → "critical" → Return to depot
- SOC < 40% → "low" → Dispatch caution
- SOC ≥ 40% → "normal" → Operational

## In-Service Logic

A bus is considered "in-service" if:
- It appears in `realtime_inservice_dispatch_data`
- AND `block_id` is not null, empty or “N/A”

## Table Use Routing

| Intent                     | Use Table(s)                                |
|---------------------------|----------------------------------------------|
| Real-time status          | `realtime_inservice_dispatch_data`           |
| Energy range prediction   | `realtime_inservice_bus_soc_forecast`        |
| Assignment decision       | `candidates_bus_block_end_soc`               |
| Vehicle specs             | `bus_specifications`                         |
| Schedule/topology/fare    | GTFS static files (`trips.csv`, etc.)        |
