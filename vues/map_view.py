import os
import folium
from qtmodules import *
import logging

from geopy.distance import geodesic

Coordinates = tuple[float, float]


class MapWidget(QWidget):

    marker_clicked = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._engine = QWebEngineView()
        self._engine.loadFinished.connect(self._on_load_finished)
        self.layout.addWidget(self.engine, 1, Qt.AlignmentFlag.AlignCenter)

        # self.run_load_animation() # Run loading animation instead of an empty map

        self._web_channel = QWebChannel()
        self._web_channel.registerObject('mapWidget', self)
        self.engine.page().setWebChannel(self._web_channel)

        self._folium_map = folium.Map()

        self.render_map()

    # Getters / setters

    @property
    def engine(self):
        return self._engine

    @property
    def folium_map(self):
        return self._folium_map

    @folium_map.setter
    def folium_map(self, folium_map):
        self._folium_map = folium_map
        self.render_map()

    # Methods

    def run_load_animation(self):
        """Replaces the map with a loading animation"""
        try:
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'map/load.svg')), 'r') as f:
                self.engine.setHtml(f.read())
                logging.info('map/load.svg loaded from module' + __name__)
        except FileNotFoundError:
            logging.warning('map/load.svg not found from module' + __name__)
            self.engine.setHtml('<h1>Loading...</h1>')

    def render_map(self):
        self.engine.setHtml(self.folium_map.get_root().render())
        logging.debug('Map updated')

    @pyqtSlot(float, float)
    def onMarkerClicked(self, lng: float, lat: float):
        logging.debug(f"Marker clicked at {lng}, {lat}")
        self.marker_clicked.emit(lng, lat)

    def _on_load_finished(self, ok: bool):
        if ok:
            self._web_channel = QWebChannel(self._engine.page())
            self._web_channel.registerObject('mapWidget', self)
            self._engine.page().setWebChannel(self._web_channel)

            # Inject QWebChannel script
            self._engine.page().runJavaScript('''
                                              
            // Inject QWebChannel script if not already present
            if (typeof QWebChannel === 'undefined') {
                var script = document.createElement('script');
                script.src = 'qrc:/qtwebchannel/qwebchannel.js';
                document.head.appendChild(script);
            }
            
            // wait for the channel to be ready
            var waitForChannel = setInterval(function() {
                if (typeof QWebChannel !== 'undefined') {
                    clearInterval(waitForChannel);
                    var channel = new QWebChannel(qt.webChannelTransport, function(channel) {
                        mapWidget = channel.objects.mapWidget;
                        
                        // mapWidget._onChannelCreated(channel);
                        // If we ever want to do stuff when the channel is created
                    });
                }
            }, 100);
            ''')

            # Make markers interactive
            self._engine.page().runJavaScript('''                           
            // Get a variable "map" from the global scope where a "map_1220565..." variable is stored

            var map = null;
            var propertyPattern = /^map_[a-f0-9]{32}$/; // Regex pattern to match the map variable name

            var globalProperties = Object.keys(window);
            var mapProperties = globalProperties.filter(function(property) {
                return propertyPattern.test(property);
            });

            if (mapProperties.length === 1) {
                map = window[mapProperties[0]];
            }
            
                

            // Select the markers using Folium's feature groups
            var markers = L.featureGroup();
            map.eachLayer(function(layer) {
                if (layer instanceof L.Marker) {
                    markers.addLayer(layer);
                }
            });

            // Add a click event listener to the markers
            markers.on('click', function(e) {
                var marker = e.layer;
                
                // Retrieve the GPS location of the marker
                var markerLatLng = marker.getLatLng();
                var markerLat = markerLatLng.lat;
                var markerLng = markerLatLng.lng;

                // Emit a signal to Python
                mapWidget.onMarkerClicked(markerLng, markerLat);
            });

            // Add the markers to the map
            map.addLayer(markers);
            ''')

            logging.info('Map loaded')
        else:
            logging.error('Map failed to load')

    def add_marker(self, tooltip: str, coordinates: Coordinates):
        """Adds a marker on the map at the given coordinates with the given tooltip"""
        self.run_load_animation()
        self.folium_map.add_child(folium.Marker(
            location=coordinates, popup=tooltip))
        self.render_map()

    def load_marker_list(self, marker_list: list[tuple[str, Coordinates]], drop_current_map: bool = True):

        self.run_load_animation()

        if drop_current_map:
            self.folium_map = folium.Map()

        for marker in marker_list:
            self.folium_map.add_child(
                folium.Marker(marker[1], popup=marker[0]))

        self.render_map()

    def load_folium(self, folium_map: folium.Map):
        """Loads a folium.Map object into the map"""
        self.run_load_animation()
        self.folium_map = folium_map  # Already renders the map with the setter

    def trace_path(self, coord1: Coordinates, coord2: Coordinates, drop_current_map: bool = True):
        """Trace a line between two points that follow the curvature of the earth"""

        print(coord1, coord2)

        start_lat, start_lng = coord1
        end_lat, end_lng = coord2

        # Calculate the intermediate points along the geodesic path
        line_points = []
        distance = geodesic(coord1, coord2).meters
        num_points = int(distance / 1000)  # Adjust the resolution as needed

        for i in range(num_points + 1):
            fraction = i / num_points
            intermediate_lat = start_lat + (end_lat - start_lat) * fraction
            intermediate_lng = start_lng + (end_lng - start_lng) * fraction
            line_points.append((intermediate_lat, intermediate_lng))

        # Create a folium map centered at the starting point
        map_center = [(start_lat + end_lat) / 2, (start_lng + end_lng) / 2]
        folium_map = folium.Map(location=map_center, zoom_start=10)

        # Create a PolyLine between the coordinates
        line = folium.PolyLine(
            locations=line_points,
            color='blue',
            weight=2,
            opacity=1,
            smooth_factor=1
        )

        if drop_current_map:
            self.folium_map = folium.Map()

        line.add_to(self.folium_map)
        self.render_map()

    def reset_map(self):
        """Resets the map to its initial state"""
        self.folium_map = folium.Map()
        self.render_map()
