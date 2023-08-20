from geopy.geocoders import Nominatim
import streamlit as st
import folium
import math
from folium import *

m = folium.Map(location=[45.3288, -121.6625], zoom_start=10)



def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def get_coordinates(location):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None




add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Find Location", "Find Distance", "Mark Boundaries")
)

if add_selectbox == 'Find Location':
    location = st.sidebar.text_input("Enter Location🌍")

    st.header(":blue[Streamlit🍁 + OpenStreetMap🗾]")

    zoom_level = st.sidebar.slider("Zoom Level:", min_value=1, max_value=30, value=5)



    if st.button("Search"):
        coords = get_coordinates(location)
        lat, lon = coords
        st.warning("Your location's Latitude is: "+str(lat)+","+"\tYour location's Longitude is:"+str(lon))
        m = folium.Map(location=[lat, lon], zoom_start=zoom_level)
        folium.Marker(location=[lat, lon], popup=location).add_to(m)
        m.save('openstreetmap_example.html')
        map_html = m._repr_html_()
        with open("openstreetmap_example.html", "r") as f:
            external_map_html = f.read()
            st.components.v1.html(external_map_html, height=1000)
    else:
        pass

elif add_selectbox == 'Find Distance':
    tooltip = "Click me!"

    source = st.sidebar.text_input("Enter Source Location🌍")

    destination = st.sidebar.text_input("Enter Destination Location🏭")

    st.header(":blue[Streamlit🍁 + OpenStreetMap🗾]")

    zoom_level = st.sidebar.slider("Zoom Level:", min_value=1, max_value=30, value=5)


    if st.button("Search"):
        coords1 = get_coordinates(source)
        lat1, lon1 = coords1
        coords2 = get_coordinates(destination)
        lat2, lon2 = coords2

        st.warning("Latitude is: "+str(lat1))
        st.warning("\nLongitude is:"+str(lon1))
        m = folium.Map(location=[lat1, lon1], zoom_start=zoom_level)
        folium.Marker(location=[lat1, lon1], popup=source).add_to(m)
        folium.Marker(location=[lat2, lon2], popup=destination).add_to(m)
        folium.PolyLine([[lat1, lon1], [lat2, lon2]], tooltip="Coast").add_to(m)

        m.save('openstreetmap_example.html')
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        st.success("Distance between two points is "+str(distance)+" km")
        map_html = m._repr_html_()
        with open("openstreetmap_example.html", "r") as f:
            external_map_html = f.read()
            st.components.v1.html(external_map_html, height=1000)
            
    else:
        pass



elif add_selectbox == 'Mark Boundaries':
        location = st.sidebar.text_input("Enter the location")
        st.header(":blue[Streamlit🍁 + OpenStreetMap🗾]")
        if st.button("Search"):
            coords = get_coordinates(location)
            lat, lon = coords
            central_location = (lat, lon)
            distance = 0.01

            input_coordinates = [
            [central_location[1] - distance, central_location[0] - distance],  # Lower left corner
            [central_location[1] - distance, central_location[0] + distance],  # Lower right corner
            [central_location[1] + distance, central_location[0] + distance],  # Upper right corner
            [central_location[1] + distance, central_location[0] - distance],  # Upper left corner
            ]
            input_coordinates.append(input_coordinates[0])
            geojson_data = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [input_coordinates]
            }
            }
            geojson_layer = GeoJson(geojson_data, style_function=lambda x: {"color": "blue", "fillOpacity": 0.3})

            # Add the GeoJson layer to the map
            geojson_layer.add_to(m)
            m.save('openstreetmap_example.html')
            map_html = m._repr_html_()
            with open("openstreetmap_example.html", "r") as f:
                external_map_html = f.read()
                st.components.v1.html(external_map_html, height=1000)

else:
    st.sidebar.text_input("Enter Phone Number")





