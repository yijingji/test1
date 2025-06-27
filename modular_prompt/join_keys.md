# Join Keys & Relationships

## Common Join Keys

| Join Key  | Tables                                       | Purpose                                 |
|-----------|----------------------------------------------|------------------------------------------|
| bus_id    | All except GTFS CSV tables                         | Identifies a bus                         |
| block_id  | All except `bus_specifications` and `historical_inservice_trip_statistics`              | GTFS Block ID a bus is/was/will be serving  |
| trip_id   | Realtime tables + `historical_inservice_trip_statistics` + GTFS `trips`, GTFS `stop_times` | Trip definition & stop info           |
| route_id  | GTFS `routes` + realtime forecasts       | Maps trip/block to route                 |
| stop_id   | GTFS `stop_times`, GTFS `stops`, GTFS `transfers`| Used for stop names, coordinates        |
| timestamp | `realtime_forecast_of_inservice_bus_soc`                       | Real-time prediction time                    |
| tmstmp    | `realtime_cad_avl_data`                          | Timestamp of bus status                      |

## Relationships
- `bus_specifications`.bus_id = `realtime_cad_avl_data`.bus_id
- `bus_specifications`.bus_id = `realtime_ev_soc`.bus_id
- `realtime_cad_avl_data`.block_id = `realtime_forecast_of_inservice_bus_soc`.block_id
- `realtime_cad_avl_data`.block_id = GTFS `trips`.block_id
- `historical_inservice_block_statistics`.block_id = GTFS `trips`.block_id
- `historical_inservice_trip_statistics`.trip_id = GTFS `trips`.trip_id
- `candidates_bus_block_end_soc`.block_id = `realtime_forecast_of_inservice_bus_soc`.block_id

## GTFS Static Table Relationships

- `trips.route_id = routes.route_id`
- `trips.service_id = calendar.service_id`
- `trips.shape_id = shapes.shape_id`
- `stop_times.trip_id = trips.trip_id`
- `stop_times.stop_id = stops.stop_id`
- `frequencies.trip_id = trips.trip_id`
- `fare_rules.route_id = routes.route_id`
- `fare_rules.fare_id = fare_attributes.fare_id`
