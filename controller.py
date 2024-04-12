import logging
import os
import psycopg2
import math
from utils import *

""""
Country = (Nom VARCHAR(100), ISO VARCHAR(2), DAFIF VARCHAR(2));
Plane = (IATA VARCHAR(3), ICAO VARCHAR(4), Name VARCHAR(80));
Equipment = (IATA VARCHAR(3), Equipment_ID INT, #(IATA_1, ICAO));
Arline = (Airline_ID INT, Name VARCHAR(100), Alias VARCHAR(50), IATA VARCHAR(2), ICAO VARCHAR(3), Callsign VARCHAR(50), Country VARCHAR(100), Active VARCHAR(1), #Nom);
Siege = (ID VARCHAR(4), nbre_siege INT, #(IATA, ICAO));
Airport = (Airport_ID INT, Name VARCHAR(100), City VARCHAR(100), Country VARCHAR(100), IATA VARCHAR(3), ICAO VARCHAR(4), Latitude DOUBLE, Longitude DOUBLE, Altitude INT, Timezone INT, DST VARCHAR(1), Tz VARCHAR(100), Type VARCHAR(100), Source VARCHAR(100), #Nom);
Vol = (#Airport_ID, #Airport_ID_1, #IATA, #Airline_ID, Codeshare VARCHAR(1), Stops INT);

VUES
vue_vol_info = (Airline_ID INT, Airline_Name VARCHAR(100), Departure_Airport_ID INT, Departure_Airport VARCHAR(100), Destination_Airport_ID INT, Destination_Airport VARCHAR(100), Plane VARCHAR(80), Seat INT, Distance DOUBLE, CO2_Emissions DOUBLE);
vue_vol_info_rounded = (Airline_ID INT, Airline_Name VARCHAR(100), Departure_Airport_ID INT, Departure_Airport VARCHAR(100), Destination_Airport_ID INT, Destination_Airport VARCHAR(100), Plane VARCHAR(80), Seat INT, Distance DOUBLE, CO2_Emissions DOUBLE);

FONCTIONS
FUNCTION calcul_distance(lat1 double precision, lon1 double precision, lat2 double precision, lon2 double precision) RETURNS double precision
FUNCTION calcul_distance(lat1 numeric, lon1 numeric, lat2 numeric, lon2 numeric) RETURNS numeric
FUNCTION calculer_emissions_co2(distance double precision, nb_sieges integer DEFAULT NULL::integer) RETURNS numeric
FONCTION calculer_emissions_co2(distance numeric, nb_sieges numeric DEFAULT NULL::numeric) RETURNS numeric

"""


# load_dotenv(find_dotenv('.env'), override=True)


class Controller():
    def __init__(self, password):
        self.conn = psycopg2.connect(
            database="sae_aeroport",
            user="sae_aeroport_user",
            password=password
        )

    def get_total_flights(self, country):
        """ Renvoie le nombre de vols total d'un pays"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM vol WHERE source_airport_id IN (SELECT airport_id FROM airport WHERE country = %s)", (country,))
        flights = cursor.fetchone()
        cursor.close()
        return flights[0]

    def get_countries_with_iso(self, must_have_airport=True, must_have_flight=True):
        """ Renvoie la liste des pays avec leur code ISO

        Returns:
            list: Liste des pays avec leur code ISO
        """
        cursor = self.conn.cursor()

        # FIXME can cause errors if must_have_flights is True and must_have_airport is False
        request = """
       SELECT name, iso 
       FROM country
        
        
        """
        if must_have_airport:
            request += """ 
        WHERE name IN (
            SELECT distinct country from airport
        )
        """

        if must_have_flight:
            request += """
        AND name IN (
            select distinct country from airport where airport_id in (
                select distinct source_airport_id from vol
                )
        )
        """

        cursor.execute(request)
        countries = cursor.fetchall()
        cursor.close()
        return countries

    def get_airport_id_by_coords(self, lon, lat):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT Airport_ID FROM airport WHERE Longitude = %s AND Latitude = %s", (lon, lat))
        try:
            airport = cursor.fetchone()
        except psycopg2.OperationalError:
            logging.error("Erreur lors de la récupération de l'aéroport")
            airport = None
        cursor.close()
        return airport

    def get_airport_coords_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT Latitude, Longitude FROM airport WHERE Name = %s", (name,))
        try:
            airport = cursor.fetchone()
        except psycopg2.OperationalError:
            logging.error("Erreur lors de la récupération de l'aéroport")
            airport = None
        cursor.close()
        print(name, airport)
        return airport

    def get_companies_for_route_by_plane_model(self, airport1: str, airport2: str, plane_model: str):
        """ Renvoie la liste des compagnies aériennes qui effectuent un trajet donné avec un avion donné"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT airline_name FROM vue_vol_info WHERE departure_airport = %s AND destination_airport = %s AND plane = %s", (airport1, airport2, plane_model))
        try:
            companies = cursor.fetchall()
            companies = [company[0] for company in companies]
        except psycopg2.OperationalError:
            logging.error("Erreur lors de la récupération de l'aéroport")
            companies = None
        cursor.close()
        return companies

    def get_best_airplane_model_for_route(self, airport1: str, airport2: str):
        """ Renvoie le nom du meilleur avion pour un trajet donné, ainsi que ses émissions de CO2"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT plane, co2_emissions FROM vue_vol_info_rounded WHERE departure_airport = %s AND destination_airport = %s ORDER BY co2_emissions ASC LIMIT 1", (airport1, airport2))
        try:
            plane = cursor.fetchone()
        except psycopg2.OperationalError:
            logging.error("Erreur lors de la récupération de l'aéroport")
            plane = None
        cursor.close()
        return plane

    def get_distance_between_airports(self, airport1: str, airport2: str):
        """ Renvoie la distance entre deux aéroports passés par leur nom"""

        # get the lat and lon of the airports
        start_lng, start_lat = self.get_airport_coords_by_name(airport1)
        end_lng, end_lat = self.get_airport_coords_by_name(airport2)

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT calcul_distance(%s, %s, %s, %s)", (start_lat, start_lng, end_lat, end_lng))
        try:
            distance = cursor.fetchone()
        except psycopg2.OperationalError:
            logging.error("Erreur lors de la récupération de la distance")
            distance = None
        cursor.close()
        return distance[0]

    def get_countries(self):
        """ Renvoie la liste des pays

        Returns:
            list: Liste des pays
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT Name FROM country")
        countries = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return countries

    def get_airports(self) -> list[str, tuple[float, float]]:
        """ Renvoie la liste des aéroports avec leur latitude et longitude

        Returns:
            list[str, tuple[float, float]]: Liste des aéroports
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT Name, Latitude, Longitude FROM airport")
        airports = [row for row in cursor.fetchall()]
        cursor.close()
        return [(airports[0], (airports[1], airports[2])) for airports in airports]

    def get_airport_name_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT Name FROM airport WHERE Airport_ID = %s", (id,))
        airport = cursor.fetchone()
        cursor.close()
        return airport[0]

    def get_aeroports_by_country(self, country):
        """ Renvoie la liste des aéroports d'un pays

        Args:
            country (str): Nom du pays

        Returns:
            list: Liste des aéroports d'un pays
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT Name FROM airport WHERE country = %s ORDER BY Name", (country,))
        aeroports = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return aeroports

    def get_aeroports_by_country_constraint(self, country, first_aero):
        """Renvoie la liste des aéroports d'un pays si ceux si sont reliés au premier aéroport par un vol ( arrivé ou départ)

        Args:
            country (str): Nom du pays
            first_aero (str): Nom du premier aéroport
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT Name FROM airport WHERE country = %s AND (airport_id IN (SELECT source_airport_id FROM vol WHERE destination_airport_id = (SELECT airport_id FROM airport WHERE name = %s)) OR airport_id IN (SELECT destination_airport_id FROM vol WHERE source_airport_id = (SELECT airport_id FROM airport WHERE name = %s))) ORDER BY Name", (country, first_aero, first_aero))
        aeroports = [row[0] for row in cursor.fetchall()]
        cursor.close()
        print(aeroports)
        return aeroports

    def get_airports_coors_by_country(self, country) -> list[str, tuple[float, float]]:

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT Name, Latitude, Longitude FROM airport WHERE country = %s ORDER BY Name", (country,))
        aeroports = [row for row in cursor.fetchall()]
        cursor.close()
        return [(aeroports[0], (aeroports[1], aeroports[2])) for aeroports in aeroports]

    def get_useful_airports_coords_by_country(self, country_id) -> list[str, tuple[float, float]]:
        """Only returns airports with at least one flight from it"""

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                A.Name AS Airport_Name,
                A.Latitude,
                A.Longitude
            FROM
                Airport A
            WHERE
                A.Airport_ID IN (
                    SELECT DISTINCT
                        V.source_airport_id
                    FROM
                        Vol V
                    UNION
                    SELECT DISTINCT
                        V.destination_airport_id
                    FROM
                        Vol V
                )
                AND A.Country = %s;
            """, (country_id,)
        )
        aeroports = [row for row in cursor.fetchall()]
        cursor.close()
        return [(aeroports[0], (aeroports[1], aeroports[2])) for aeroports in aeroports]

    def get_info_aeroport(self, aeroport):
        """ Renvoie les informations d'un aéroport

        Args:
            aeroport (str): Nom de l'aéroport

        Returns:
            tuple: Informations de l'aéroport
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT Name, City, Country, IATA, ICAO, Latitude, Longitude, Altitude, Timezone, DST, Tz_database_time_zone, Type, Source FROM airport WHERE Name = %s", (aeroport,))
        aeroport_info = cursor.fetchone()
        cursor.close()
        return aeroport_info

    def pourcentage_outside_country(self, country):
        """ Renvoie le pourtacege de vol qui sont en dehors du pays

        Args:
            country (str): Nom du pays

        Returns:
            float: Pourcentage de vol qui sont en dehors du pays
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Vol WHERE Source_airport_ID IN (SELECT Airport_ID FROM Airport WHERE Country = %s) AND Destination_airport_ID NOT IN (SELECT Airport_ID FROM Airport WHERE Country = %s)", (country, country))
        nbre_vol_outside = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM Vol WHERE Source_airport_ID IN (SELECT Airport_ID FROM Airport WHERE Country = %s)", (country,))
        nbre_vol = cursor.fetchone()[0]
        if nbre_vol == 0:
            return 0
        return nbre_vol_outside/nbre_vol

    def pourcentage_inside_country(self, country):
        """ Renvoie le pourtacege de vol dont le départ et l'arrivée sont dans le pays

        Args:
            country (str): Nom du pays

        Returns:
            float: Pourcentage de vol dont le départ et l'arrivée sont dans le pays
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Vol WHERE Source_airport_ID IN (SELECT Airport_ID FROM Airport WHERE Country = %s) AND Destination_airport_ID IN (SELECT Airport_ID FROM Airport WHERE Country = %s)", (country, country))
        nbre_vol_inside = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM Vol WHERE Source_airport_ID IN (SELECT Airport_ID FROM Airport WHERE Country = %s)", (country,))
        nbre_vol = cursor.fetchone()[0]
        if nbre_vol == 0:
            return 0
        return nbre_vol_inside/nbre_vol

    def calcul_distance(self, aeroport1, aeroport2):
        # Récupération des coordonnées géographiques des aéroports
        # Et calcule de la distance entre les deux aéroports grace a la fonction sql calcul_distance

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT Latitude, Longitude FROM airport WHERE Name = %s", (aeroport1,))
        aeroport1_coord = cursor.fetchone()
        cursor.execute(
            "SELECT Latitude, Longitude FROM airport WHERE Name = %s", (aeroport2,))
        aeroport2_coord = cursor.fetchone()
        cursor.execute(
            "SELECT calcul_distance(%s, %s, %s, %s)", (aeroport1_coord[0], aeroport1_coord[1], aeroport2_coord[0], aeroport2_coord[1]))
        distance = cursor.fetchone()[0]
        cursor.close()
        return distance

    # def calcul_distance(lat1, lon1, lat2, lon2):
    #     """ Calcule la distance entre deux aéroports grâce à leurs coordonnées géographiques

    #     Args:
    #         lat1 (float): Latitude du premier aéroport
    #         lon1 (float): Longitude du premier aéroport
    #         lat2 (float): Latitude du deuxième aéroport
    #         lon2 (float): Longitude du deuxième aéroport

    #     Returns:
    #         float: Distance entre les deux aéroports
    #     """
    #     rayon_de_la_terre = 6371.0

    #     lat1_rad = math.radians(lat1)
    #     lon1_rad = math.radians(lon1)
    #     lat2_rad = math.radians(lat2)
    #     lon2_rad = math.radians(lon2)

    #     # Calcul de la distance géodésique
    #     delta_lon = lon2_rad - lon1_rad
    #     delta_lat = lat2_rad - lat1_rad
    #     a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * \
    #         math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    #     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    #     distance = rayon_de_la_terre * c

    #     return distance

    def get_country_flights_info(self, country) -> tuple[int, int]:
        """ Renvoie la part de vols internes / externes d'un pays"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Vol WHERE Source_airport_ID IN (SELECT Airport_ID FROM Airport WHERE Country = %s) AND Destination_airport_ID NOT IN (SELECT Airport_ID FROM Airport WHERE Country = %s)", (country, country))
        nbre_vol_outside = cursor.fetchone()[0]
        cursor.execute(
            "SELECT COUNT(*) FROM Vol WHERE Source_airport_ID IN (SELECT Airport_ID FROM Airport WHERE Country = %s)", (country,))
        nbre_vol_inside = cursor.fetchone()[0]

        return nbre_vol_inside, nbre_vol_outside

    @staticmethod
    def calculer_emissions_CO2(distance, nb_sieges=None):
        """ Calcule les émissions de CO2 d'un vol grace à sa distance et au nombre de sièges de l'avion

        Args:
            distance (float): Distance du vol
            nb_sieges (int, optional): Nombre de sièges de l'avion. Defaults to None.

        Returns:
            float: Emissions de CO2 du vol
        """
        if distance < 1500:
            if not nb_sieges:
                nb_sieges = 153.51
            facteur_charge_passagers = 0.82
            facteur_cargaison = 1 - 0.07
            poids_classe = 0.96
            facteur_emission = 3.15
            facteur_emission_preprod = 0.54
            multiplicateur = 2
            facteur_aeronef = 0.00038
            emissions_infrastructure = 11.68
            a = 0.0000
            b = 2.714
            c = 1166.52
        elif distance > 2500:
            if not nb_sieges:
                nb_sieges = 280.21
            facteur_charge_passagers = 0.82
            facteur_cargaison = 1 - 0.26
            poids_classe = 1.26
            facteur_emission = 3.15
            facteur_emission_preprod = 0.54
            multiplicateur = 2
            facteur_aeronef = 0.00038
            emissions_infrastructure = 11.68
            a = 0.0001
            b = 7.104
            c = 5044.9
        else:
            # interpolation linéaire
            if not nb_sieges:
                nb_sieges = 153.51 + (distance - 1500) * \
                    (280.21 - 153.51) / (2500 - 1500)
            facteur_charge_passagers = 0.82
            facteur_cargaison = 1 - \
                (0.07 + (distance - 1500) * (0.26 - 0.07) / (2500 - 1500))
            poids_classe = 0.96 + (distance - 1500) * \
                (1.26 - 0.96) / (2500 - 1500)
            facteur_emission = 3.15 + (distance - 1500) * \
                (3.15 - 3.15) / (2500 - 1500)
            facteur_emission_preprod = 0.54 + \
                (distance - 1500) * (0.54 - 0.54) / (2500 - 1500)
            multiplicateur = 2
            facteur_aeronef = 0.00038
            emissions_infrastructure = 11.68
            a = 0.0000 + (distance - 1500) * (0.0001 - 0.0000) / (2500 - 1500)
            b = 2.714 + (distance - 1500) * (7.104 - 2.714) / (2500 - 1500)
            c = 1166.52 + (distance - 1500) * \
                (5044.9 - 1166.52) / (2500 - 1500)

        LTO = 0  # carbuant consommé à l'attérissage et au décollage

        emissions_CO2 = (((a * distance**2 + b * distance + c) + LTO) / (nb_sieges * facteur_charge_passagers)) * (1 - facteur_cargaison) * \
            poids_classe * (facteur_emission * multiplicateur + facteur_emission_preprod) + \
            facteur_aeronef * distance + emissions_infrastructure

        return emissions_CO2

    def get_top_countries(self, country, nb_countries=5) -> list[tuple[float, str]]:
        """ Renvoie les nb_countries pays destination les plus courants d'un pays"""

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                COUNT(*),
                A.Country
            FROM
                Vol V
                JOIN Airport A ON V.Destination_airport_ID = A.Airport_ID
            WHERE
                V.Source_airport_ID IN (SELECT Airport_ID FROM Airport WHERE Country = %s)
                AND A.Country != %s
            GROUP BY
                A.Country
            ORDER BY
                COUNT(*) DESC
            LIMIT %s;
            """, (country, country, nb_countries))
        return cursor.fetchall()

    def get_most_polluting_routes(self, airport_id, nb_routes=5) -> list[tuple[float, str]]:
        """ 
        Recupère les données sur le Co2 et les aéroports d'arrivée des nb_routes routes les plus polluantes

        Args:
            airport_id (int): ID de l'aéroport de départ
            nb_routes (int, optional): Nombre de routes à récupérer. Defaults to 5.

        Returns:
            list: Liste des nb_routes routes les plus polluantes
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                VI.CO2_Emissions,
                VI.Destination_Airport
            FROM
                vue_vol_info VI
                JOIN Airport A1 ON VI.Departure_Airport_ID = A1.Airport_ID
                JOIN Airport A2 ON VI.Destination_Airport_ID = A2.Airport_ID
            WHERE
                A1.Airport_ID = %s
            ORDER BY
                VI.CO2_Emissions DESC
            LIMIT %s;
            """, (airport_id, nb_routes)
        )
        routes = cursor.fetchall()
        cursor.close()
        return routes

    def get_info_download(self, airport1: str, airport2: str) -> tuple:
        """Renvoie toutes les infos pour le téléchargement

        Args:
            airport1 (str): Nom de l'aéroport de départ
            airport2 (str): Nom de l'aéroport d'arrivée

        Returns:
            tuple: Infos pour le téléchargement
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT Airline_Name,Departure_Airport,Destination_Airport,Plane, Seat, Distance, CO2_Emissions FROM vue_vol_info_rounded WHERE Departure_Airport = %s AND Destination_Airport = %s;
            """, (airport1, airport2)
        )
        info = cursor.fetchall()
        cursor.close()
        return info


# print(pourcentage_outside_country("France"))
# print(pourcentage_inside_country("Navassa Island"))
