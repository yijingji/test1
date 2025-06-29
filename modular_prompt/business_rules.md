# Embedded Business Rules

## EV Definition
- If `model` = 'BEV' in `bus_specifications`

## In-Service Logic
A bus is considered "in-service" if:
- It appears in `realtime_cad_avl_data` AND `block_id` is not null, "", empty or “N/A”
- If output of the SQL is empty, it means the bus is not inservice. 
- If output is a block_id, double check whether it exists inside GTFS. If not, then the bus is not inservice. 

## Dispatch suggestion Logic
- Use `candidates_bus_block_end_soc` for unassigned bus-block pairing.
- If the bus is already in-service, avoid reassigning and return:  
  “This bus is currently in service. We suggest not reassigning it to another block.”

## Energy Efficiency Definitions:
- Energy efficiency = energy used / miles driven. Unit: kWh/mile. 
- Manufacturer-estimated energy efficiency = `bus_specifications`.energy_efficiency. Unit: kWh/mile. This is a reference value, not real-time.
- Current energy efficiency = `realtime_forecast_of_inservice_bus_soc`.avg_kwh_mile. Unit: kWh/mile. This is based on real-time bus data.
- Energy efficiency of one bus on one block on one specific day = `historical_inservice_block_statistics`.kwh_per_mile filtered by bus_id and block_id and record_date.
- Average energy efficiency of one bus based on historical data = `historical_inservice_block_statistics`.kwh_per_mile filtered by bus_id. Unit: kWh/mile. This is statistic value based on historical records.
- Average energy efficiency of one block based on historical data = `historical_inservice_block_statistics`.kwh_per_mile filtered by block_id. Unit: kWh/mile. This is statistic value based on historical records.
- Average energy efficiency of one driver based on historical data = `historical_inservice_trip_statistics`.kwh_per_mile filtered by driver_id. Unit: kWh/mile. This is statistic value based on historical records.
- Energy used of one bus on one block on one specific day = `historical_inservice_block_statistics`.energy_used filtered by bus_id and block_id and record_date. Unit: kWh.
- Remove the None values for analysis. 

## Speed Definitions:
- Current speed of EV = `realtime_ev_telematics`.current_speed. Unit: MPH.
- Current speed of nonEV = `realtime_cad_avl_data`.spd. Unit: MPH.
- Average speed of one bus on one block on one specific day = `historical_inservice_block_statistics`.avg_speed filtered by bus_id and block_id and record_date. Unit: MPH. 
- Average speed of one bus on one block = AVG `historical_inservice_block_statistics`.avg_speed filtered by bus_id and block_id. Unit: MPH. 
- Remove the None values for analysis.

## Remaining Miles Definitions:
- Remaining miles of the in-service bus = `realtime_ev_telematics`.current_range. Unit: mile. 
- Remaining miles of the in-service block served by EV = `realtime_forecast_of_inservice_bus_soc`.left_miles. Unit: mile.
- Remaining miles of the in-service block served by non-EV = `candidates_bus_block_end_soc`.remaining_block_miles WHERE bus_id is not in service. Unit: mile.
- Remove the None values for analysis.

## SOC Definitions:
- Current/realtime SOC of EV = `realtime_ev_soc`.current_soc. Unit: %
- Predicted end-of-block SOC of in-service EV = `realtime_forecast_of_inservice_bus_soc`.pred_end_block_soc. Unit: %
- Predicted end-of-trip SOC of in-service EV = `realtime_forecast_of_inservice_bus_soc`.pred_end_trip_soc. Unit: %
- Predicted end-of-block SOC of unassigned bus-block pairing = `candidates_bus_block_end_soc`.end_soc. Unit: %
- SOC used of one bus on one block on one specific day = `historical_inservice_block_statistics`.soc_used filtered by bus_id and block_id and record_date. Unit: %.
- SOC used of one bus on one trip on one specific day = (`historical_inservice_trip_statistics`.start_soc - `historical_inservice_trip_statistics`.end_soc) filtered by bus_id and trip_id and record_date. Unit: %.
- Remove the None values for analysis.

## SOC Alerts Levels
- SOC < 10% → "critical" → If in-service, suggest to return to depot
- SOC < 40% → "low" → If in-service, need dispatch caution
- SOC ≥ 40% → "normal" → Operational

## Location Logic
- Real-time location: `realtime_inservice_dispatch_data`.lat, `realtime_inservice_dispatch_data`.lon
- If the bus has no location data in `realtime_inservice_dispatch_data`, just clarify that "There is no data available."

## No Data
- No Data means: Query return empty string or [] or row_count = 0
- No in-service data, could reply: "bus is not inservice"
- No location data, could reply: "There is no location data for the bus"
- No prediction data, could reply: "There is no prediction data for the bus"
- No dispatch suggestion data, could reply: "There is no suggested prediction data for the bus"
- No GTFS data, could reply: "There is no matched GTFS data"

## Service ID Logic
Steps to get a specific day's service id:
1. Get the specific day's date, convert it into the same date formate with date inside `calendar.csv` and `calendar_dates.csv`
2. Think the weekday of this specific day's date
3. Go to GTFS `calendar.csv` table, find out all possible service id for that date and that weekday: "SELECT service_id FROM calendar WHERE (that_weekday = 1) AND (that_date BETWEEN start_date AND end_date)"
4. Go to GTFS `calendar_dates.csv` table, find out any exceptions for those service ids: "SELECT service_id, exception_type FROM calendar_dates WHERE date = that_date"
5. Among those service ids, return the only one with exception_type = 1. Otherwise, remove the service id with exception_type = 2 and then return the rest service ids. 

## Date & Time Format Handling Logic
Always convert dates to the correct format before filtering, joining, or selecting.
- `calendar`, `calendar_dates`, and `feed_info`: 
  Format: YYYYMMDD (as text or integer, e.g., 20250626)
- `stop_times`:
  Format: HH:MM:SS (e.g., 10:30:00 means 10:30 AM)
- `realtime_forecast_of_inservice_bus_soc`:
  date format: YYYY-MM-DD (ISO date, e.g., 2025-06-26)
  timestamp Format: timestamp in seconds, LA timezone (Epoch, e.g., 1750882744 means Wednesday, June 25, 2025 13:19:04)
- `realtime_cad_avl_data`:
  tmstmp format: YYYYMMDD HH:MM:SS (text, e.g., 20250625 13:19:47)
  stst format: Scheduled trip start time in seconds past midnight (integer, e.g., 46320 means 12:52 PM)
  stsd format: Scheduled block start date in YYYY-MM-DD (ISO date, e.g., 2025-06-26)
- `historical_inservice_trip_statistics`, `historical_inservice_block_statistics`
  record_date format: YYYY-MM-DD (ISO date, e.g., 2025-06-26)
  actual_trip_start_time, actual_trip_end_time, actual_block_start_time, actual_block_end_time format: timestamp in seconds, LA timezone (Epoch, e.g., 1750882744 means Wednesday, June 25, 2025 13:19:04)


## Table Use Routing

| Intent                     | Use Table(s)                                |
|---------------------------|----------------------------------------------|
| Real-time status          | `realtime_inservice_dispatch_data`           |
| Energy range prediction   | `realtime_forecast_of_inservice_bus_soc`        |
| Assignment decision       | `candidates_bus_block_end_soc`               |
| Vehicle specs             | `bus_specifications`                         |
| Schedule/topology/fare    | GTFS static files (`trips.csv`, etc.)        |
