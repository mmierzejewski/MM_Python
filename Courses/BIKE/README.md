# Bike Service Proxy

A Python client for retrieving station locations and bike battery data from rowermevo.pl.

`BikeServiceProxy` fetches the current locations CSV into `current_locations_file` and parses battery levels for bike identifiers. Use `battery_info_for_bike(bike_id)` to get a bike's battery value; it returns `None` when the identifier is not present.

Install the project dependencies with:

```bash
python3 -m pip install -r requirements.txt
```