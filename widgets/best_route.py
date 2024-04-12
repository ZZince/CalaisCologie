
from qtmodules import *


class BestRouteWidget(QWidget):
    """Widget to visualize the best airplane, the CO2 for the route and the companies that fly the route"""

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.airplane_model = ""
        self.co2 = ""
        self.companies = []
        self.distance = 0

        self._label_distance = QLabel("Distance: 0km")
        self._label_airplane_model = QLabel("Modèle du meilleur avion : ")
        self._label_co2 = QLabel("CO2 pour le trajet : ")
        self._list_companies = QListWidget()

        self.layout.addWidget(self._label_distance)
        self.layout.addWidget(self._label_airplane_model)
        self.layout.addWidget(self._label_co2)
        self.layout.addWidget(self._list_companies)

        self.setLayout(self.layout)

    def update(self):
        """Update the widget"""

        self._label_distance.setText(f"Distance : {self.distance:.2f}km")

        self._label_airplane_model.setText(
            "Modèle du meilleur avion : " + self.airplane_model)
        self._label_co2.setText("CO2 pour le trajet : " + str(self.co2))

        self._list_companies.clear()
        for company in self.companies:
            self._list_companies.addItem(company)

        super().update()

    def set_distance(self, distance):
        self.distance = distance

    def set_airplane_model(self, airplane_model):
        """Set the airplane model"""
        self.airplane_model = airplane_model

    def set_co2(self, co2):
        """Set the co2"""
        self.co2 = co2

    def set_companies(self, companies):
        """Set the companies"""
        self.companies = companies
        
    def reset(self):
        "Reste the widget"
        self._label_distance.setText("Distance : 0km")
        self._label_airplane_model.setText("Modèle du meilleur avion :")
        self._label_co2.setText("CO2 pour le trajet :")
        self._list_companies.clear()
