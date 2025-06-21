# Example Applications

**Q:** What is the current location of bus 2401?  
→ Use `realtime_inservice_dispatch_data`. Filter by `bus_id = '2401'`.

**Q:** What is the predicted SOC for bus 2401 at the end of the current block?  
→ Use `realtime_inservice_bus_soc_forecast`. Filter by `bus_id = '2401'`. Return `pred_end_block_soc`.

**Q:** Which buses can serve block 12 with highest remaining SOC?  
→ Use `candidates_bus_block_end_soc`. Filter `block_id = '12'` and sort by `end_soc DESC`.

**Q:** What type of bus is 2401?  
→ Use `bus_specifications`. Filter by `bus_id = '2401'`.
