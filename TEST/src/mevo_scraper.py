import folium
from folium.plugins import MarkerCluster
import csv
from bike_service_proxy import BikeServiceProxy

def get_icon_color(battery_level):
    if battery_level is None:
        return 'gray'

    if battery_level > 50:
        return 'green'

    if battery_level > 20:
        return 'orange'
    else:
        return 'red'

bikes_map = folium.Map(location=[54.34632, 18.649246])
bikes_cluster = MarkerCluster()
bikes_proxy = BikeServiceProxy()

bike_file = bikes_proxy.current_locations_file
bikes_reader = csv.DictReader(bike_file)

for station_row in bikes_reader:
    available_bikes = int(station_row['DOSTĘPNE ROWERY'])

    if available_bikes > 0:
        available_bikes_ids_str = station_row['NUMERY DOSTĘPNYCH ROWERÓW']
        available_bikes_ids = available_bikes_ids_str.split(',')

        coordinates_str = station_row['WSPÓŁRZĘDNE']
        coordinates = coordinates_str.split(', ')

        latitude = float(coordinates[0])
        longitude = float(coordinates[1])
        coordinates = [latitude, longitude]

        for bike_id in available_bikes_ids:
            battery_level = bikes_proxy.battery_info_for_bike(bike_id)

            if battery_level is None:
                battery_info = 'Nieznana wartość'
            else:
                battery_info = f'{battery_level}%'

            station_info = f'ID: {bike_id} Bateria: {battery_info}'
            icon_color = get_icon_color(battery_level)
            bike_icon = folium.Icon(icon='bicycle', prefix='fa', color=icon_color)

            bike_marker = folium.Marker(location=coordinates, popup=station_info, icon=bike_icon)
            bikes_cluster.add_child(bike_marker)

bikes_map.add_child(bikes_cluster)
bikes_map.save('bikes_map.html')