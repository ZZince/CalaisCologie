from __future__ import annotations
from qtmodules import *
from .list_select import ListSelect


class CountryItem(QListWidgetItem):
    """ListWidgetItem modified to include the flags of the countries as an image"""

    def __init__(self, country_name: str, iso: str):
        """Initializes the CountryItem widget

        Args:
            country_name (str): Name of the country
            iso (str): Iso code of the country
        """

        super().__init__()

        self.country_name = country_name
        self.iso = iso

        self.setText(self.country_name)

        if self.iso is None:
            # self.setIcon(QIcon("interface/img/flags/unknown.png"))
            return

        self.setIcon(QIcon("img/flags/" +
                     self.iso.upper() + "-128.png"))

    @property
    def text(self) -> str:
        return self.country_name


class CountrySelect(ListSelect):
    """ListSelect modified to include the flags of the countries"""

    country_list = []
    instances: set[CountrySelect] = set()

    def __init__(self):
        super().__init__()
        self.items = CountrySelect.country_list
        CountrySelect.instances.add(self)

    def select_list(self, item):
        """
        Émettre un signal avec l'item sélectionné.
        """
        self.item_selected.emit(item.text)

    def set_list(self, countries: list[tuple[str, str]]):
        raise SystemError(
            "Can't set the country this way, use the class method instead")

    @classmethod
    def set_country_list(cls, countries: list[tuple[str, str]]):
        cls.country_list = countries

        # update all instances of CountrySelect
        for instance in cls.instances:
            instance.items = cls.country_list
            instance.search()

    def search(self):
        search_text = self.search_bar.text()
        self.list_widget.clear()
        for name, iso in self.items:
            if search_text.lower() in name.lower():
                self.list_widget.addItem(CountryItem(name, iso))
