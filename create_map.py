import folium
from geopy.geocoders import Nominatim

# Define the list of arenas
arenas = [
"Scotiabank Arena","Capital One Arena","Wells Fargo Center (Philadelphia)","Madison Square Garden","Barclays Center","TD Garden","Scotiabank Arena","Rocket Mortgage FieldHouse","Gainbridge Fieldhouse","United Center","Fiserv Forum","Little Caesars Arena","Scotiabank Arena","Target Center","Moda Center","Golden 1 Center","Chase Center","Delta Center","Scotiabank Arena","Spectrum Center","Amway Center","Kaseya Center","Smoothie King Center","State Farm Arena","Scotiabank Arena","FedExForum","Toyota Center","Frost Bank Center","American Airlines Center","Paycom Center","Scotiabank Arena","Footprint Center","Crypto.com Arena","Crypto.com Arena","Ball Arena","Scotiabank Arena"
]

# Initialize the geolocator
geolocator = Nominatim(user_agent="team_itinerary_maps")

# Create a Folium map centered on the first arena
map_center = folium.Map(location=(0, 0), zoom_start=4)

# Define a list of colors for each run
colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown']

# Define a list of tour names
tour_names = ['Tour #1', 'Tour #2', 'Tour #3', 'Tour #4', 'Tour #5', 'Tour #6']

# Iterate over six runs
for i in range(6):
    # Extract the arenas for the current run
    current_arenas = arenas[i * 6: (i + 1) * 6]

    # Keep track of marker locations
    locations = []

    # Add markers for each arena with actual coordinates and numbered labels
    for idx, arena in enumerate(current_arenas, start=1):
        location = geolocator.geocode(arena)
        if location:
            popup_text = f'Stop {idx}: {arena}'
            folium.Marker(
                location=(location.latitude, location.longitude),
                popup=folium.Popup(popup_text, parse_html=True),
                icon=None,  # Disable the default icon
                color=colors[i],  # Use a different color for each run
                tooltip=tour_names[i]  # Add a tooltip with the tour name
            ).add_to(map_center)
            locations.append((location.latitude, location.longitude))

    # Duplicate the first location at the end to connect back to the home stadium
    locations.append(locations[0])

    # Add a polyline to connect the locations with the corresponding color
    folium.PolyLine(locations=locations, color=colors[i], tooltip=tour_names[i]).add_to(map_center)

# Add a legend
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.9;
     ">
     &nbsp; <b>Legend</b> <br>
     &nbsp; Tour #1 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i><br>
     &nbsp; Tour #2 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i><br>
     &nbsp; Tour #3 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i><br>
     &nbsp; Tour #4 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:orange"></i><br>
     &nbsp; Tour #5 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:purple"></i><br>
     &nbsp; Tour #6 &nbsp; <i class="fa fa-map-marker fa-2x" style="color:brown"></i>
</div>
'''

map_center.get_root().html.add_child(folium.Element(legend_html))

# Save the map as an HTML file
map_center.save('all_runs_map_with_legend.html')
