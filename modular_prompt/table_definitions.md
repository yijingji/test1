
# Table Definitions (High Level)

| Table                               | Purpose                                                   | Key Fields                      |
|------------------------------------|-----------------------------------------------------------|---------------------------------|
| bus_specifications                 | Static EV specs (capacity, efficiency, model)             | bus_id                          |
| realtime_cad_avl_data   | Real-time AVL and service status from Clever Devices for all buses      | bus_id, tmstmp, block_id        |
| realtime_ev_telematics   | Current SOC value of each EV (includes: bus_id, current_soc, current range, current gps, current speed, current odo)      | bus_id        |
| realtime_forecast_of_inservice_bus_soc| Real-time end-of-trip & end-of-block SOC and energy usage for active in-service EVs| bus_id, block_id, timestamp     |
| candidates_bus_block_end_soc       | Suitability scores for possible bus-block assignments     | bus_id, block_id                |
| historical_inservice_trip_statistics       | Statistics summary of historical inservice events on trip level (EV only)      | bus_id, trip_id, record_date                |
| historical_inservice_block_statistics       | Statistics summary of historical inservice events on block level (EV only)     | bus_id, block_id, record_date               |
| GTFS Static Tables                | Core transit schedule topology (CSV)                      | varies by file               |

## GTFS Static Tables Summary

| CSV File           | Description                                   | Key Fields                    |
|--------------------|-----------------------------------------------|-------------------------------|
| routes.csv         | Basic route list                              | route_id                      |
| trips.csv          | Trip metadata incl. route/block/service links | trip_id, route_id, block_id   |
| stop_times.csv     | Stop-by-stop sequence per trip                | trip_id, stop_id              |
| stops.csv          | Stop locations                                | stop_id                       |
| shapes.csv         | GPS trace per shape                           | shape_id                      |
| calendar.csv       | Standard weekly service calendar              | service_id                    |
| calendar_dates.csv | Exceptions to the calendar                    | service_id, date              |
| fare_attributes.csv| Fare costs and rules                          | fare_id                       |
| fare_rules.csv     | Fare rule mappings by route/zone              | fare_id, route_id             |
| agency.csv         | Operator info                                 | agency_id                     |
| feed_info.csv      | Feed metadata and versioning                  | feed_publisher_name           |
| frequencies.csv    | High-frequency trip headways                  | trip_id                       |
| transfers.csv      | Stop-to-stop transfer rules                   | from_stop_id, to_stop_id      |
