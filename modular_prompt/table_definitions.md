
# Table Definitions (High Level)

| Table                               | Purpose                                                   | Key Fields                      |
|------------------------------------|-----------------------------------------------------------|---------------------------------|
| bus_specifications                 | Static EV specs (capacity, efficiency, model)             | bus_id                          |
| realtime_inservice_dispatch_data   | Real-time AVL and service status from Clever Devices for all buses      | bus_id, tmstmp, block_id        |
| realtime_inservice_bus_soc_forecast| Real-time predicted SOC and energy usage for active in-service EVs| bus_id, block_id, timestamp     |
| candidates_bus_block_end_soc       | Suitability scores for possible bus-block assignments     | bus_id, block_id                |
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

