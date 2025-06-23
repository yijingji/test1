# Join Keys & Relationships

## Common Join Keys

| Join Key  | Tables                                       | Purpose                                 |
|-----------|----------------------------------------------|------------------------------------------|
| bus_id    | All except GTFS CSV tables                         | Identifies a bus                         |
| block_id  | All except `bus_specifications`              | GTFS Block ID a bus is/was/will be serving  |
| trip_id   | Realtime tables + GTFS `trips`, GTFS `stop_times` | Trip definition & stop info           |
| route_id  | GTFS `routes` + realtime forecasts       | Maps trip/block to route                 |
| stop_id   | GTFS `stop_times`, GTFS `stops`, GTFS `transfers`| Used for stop names, coordinates        |
| timestamp | `realtime_inservice_bus_soc_forecast`                       | Real-time prediction time                    |
| tmstmp    | `realtime_inservice_dispatch_data`                          | Timestamp of bus status                      |

## Relationships
- `bus_specifications`.bus_id = `realtime_inservice_dispatch_data`.bus_id
- `realtime_inservice_dispatch_data`.block_id = `realtime_inservice_bus_soc_forecast`.block_id
- `realtime_inservice_dispatch_data`.block_id = GTFS `trips`.block_id
- `candidates_bus_block_end_soc`.block_id = `realtime_inservice_bus_soc_forecast`.block_id

## GTFS Static Table Relationships

- `trips.route_id = routes.route_id`
- `trips.service_id = calendar.service_id`
- `trips.shape_id = shapes.shape_id`
- `stop_times.trip_id = trips.trip_id`
- `stop_times.stop_id = stops.stop_id`
- `frequencies.trip_id = trips.trip_id`
- `fare_rules.route_id = routes.route_id`
- `fare_rules.fare_id = fare_attributes.fare_id`
