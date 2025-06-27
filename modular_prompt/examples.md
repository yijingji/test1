# Example Applications

**Q:** What is the current location of bus 2401?  
→ Use `realtime_cad_avl_data`. Filter by `bus_id = '2401'`.

**Q:** What is the predicted SOC for bus 2401 at the end of the current block?  
→ Use `realtime_forecast_of_inservice_bus_soc`. Filter by `bus_id = '2401'`. Return `pred_end_block_soc`.

**Q:** Which buses can serve block 12 with highest remaining SOC?  
→ Use `candidates_bus_block_end_soc`. Filter `block_id = '12'` and filter out inservice EVs and sort by `end_soc DESC`.

**Q:** What type of bus is 2401?  
→ Use `bus_specifications`. Filter by `bus_id = '2401'`.

**Q:** What is the average energy efficiency of derver 113501?
→ Use `historical_inservice_trip_statistics`. Filter by `driver_id = '113501'`.

**Q:** What is the average energy efficiency of bus 2401?
→ Use `historical_inservice_block_statistics`. Filter by `bus_id = '2401'`.

**Q:** What is the energy efficiency of bus 2401 on block 12?
→ Use `historical_inservice_block_statistics`. Filter by `bus_id = '2401'` and `block_id = '12'`.
