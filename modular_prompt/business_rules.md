# Embedded Business Rules

## EV Definition
- If `model` = 'BEV' in `bus_specifications`

## SOC Alerts Levels
- SOC < 10% → "critical" → If in-service, suggest to return to depot
- SOC < 40% → "low" → If in-service, need dispatch caution
- SOC ≥ 40% → "normal" → Operational

## In-Service Logic

A bus is considered "in-service" if:
- It appears in `realtime_inservice_dispatch_data` AND `block_id` is not null, "", empty or “N/A”
- If output of the SQL is empty, it means the bus is not inservice. 
- If output is a block_id, double check whether it exists inside GTFS. If not, then the bus is not inservice. 

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
  Remaining miles of the in-service block served by EV = realtime_inservice_bus_soc_forecast.left_miles. Unit: mile.
  Remaining miles of the in-service block served by non-EV = candidates_bus_block_end_soc.remaining_block_miles WHERE bus_id is non-EV. Unit: mile.

- Current/realtime SOC of EV = realtime_ev_soc.current_soc. Unit: %
- Predicted end-of-block SOC of in-service EV = realtime_inservice_bus_soc_forecast.pred_end_block_soc. Unit: %
- Predicted end-of-trip SOC of in-service EV = realtime_inservice_bus_soc_forecast.pred_end_trip_soc. Unit: %
- Predicted end-of-block SOC of unassigned bus-block pairing = candidates_bus_block_end_soc.end_soc. Unit: %

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

## GTFS - calendar_dates.txt Logic
- Recommended: Use calendar_dates.txt in conjunction with calendar.txt to define exceptions to the default service patterns defined in calendar.txt. If service is generally regular, with a few changes on explicit dates (for instance, to accommodate special event services, or a school schedule), this is a good approach. In this case calendar_dates.service_id is a foreign ID referencing calendar.service_id.
- Alternate: Omit calendar.txt, and specify each date of service in calendar_dates.txt. This allows for considerable service variation and accommodates service without normal weekly schedules. In this case service_id is an ID.
- Definiiton of exception_type: Indicates whether service is available on the date specified in the date field. Valid options are:
  1 - Service has been added for the specified date.
  2 - Service has been removed for the specified date.
