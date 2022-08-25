import random
import json
from enum import Enum
from discord import Colour


class SoothCardType(Enum):
    SUN = "Sun"
    APPRENTICE = "Apprentice"
    COMPANION = "Companion"
    ADEPT = "Adept"
    DEFENDER = "Defender"
    NEMESIS = "Nemesis"
    SOVEREIGN = "Sovereign"


class SoothCardFamily(Enum):
    SECRETS = "Secrets"
    MYSTERIES   = "Mysteries"
    VISIONS = "Visions"
    NOTIONS = "Notions"


class SunColours(Enum):
    SILVER = 'Silver'
    GREEN = 'Green'
    BLUE = 'Blue'
    INDIGO = 'Indigo'
    GREY = 'Grey'
    PALE = 'Pale'
    RED = 'Red'
    GOLD = 'Gold'
    INVISIBLE = 'Invisible'


PATH_OF_SUNS = [
    SunColours.SILVER,
    SunColours.GREEN,
    SunColours.BLUE,
    SunColours.INDIGO,
    SunColours.GREY,
    SunColours.PALE,
    SunColours.RED,
    SunColours.GOLD,
    SunColours.INVISIBLE
]

SUNS_COLOURS = {
    SunColours.SILVER: Colour.from_rgb(211, 229, 240),
    SunColours.GREEN: Colour.green(),
    SunColours.BLUE: Colour.blue(),
    SunColours.INDIGO: Colour.from_rgb(0, 21, 181),
    SunColours.GREY: Colour.from_rgb(100, 100, 100),
    SunColours.PALE: Colour.from_rgb(190, 190, 190),
    SunColours.RED: Colour.red(),
    SunColours.GOLD: Colour.gold(),
    SunColours.INVISIBLE: Colour.from_rgb(255, 255, 255),
}

PLAYERS_BY_FAMILY = {
    SoothCardFamily.VISIONS: ["Lành-Tye", "Brayeden Mackquelleigha Aliviyah", "Elpis Synerga"],
    SoothCardFamily.NOTIONS: ["Percival Ickle", "Zovulalano G Mooloolahbah"],
    SoothCardFamily.MYSTERIES: ["Cadmia Desforges"]
}


class SoothDeck:
    def __init__(self, sooth_deck_path, card_base_link, card_base_image_link):
        self.path_of_suns = PathOfSuns()

        self.card_base_path = card_base_link
        self.cards = []

        json_string = ""
        loaded_cards = {}
        with open(sooth_deck_path, "r") as file:
            loaded_cards = json.load(file)
        processed_card_list = []
        for card in loaded_cards["cards"]:
            card_name = card["name"]

            card_number = card["number"]
            card_link = card_base_link + card_number
            card_image_link = card_base_image_link + card_number + '.png'

            card_family = SoothCardFamily(card["family"])

            card_type = SoothCardType(card["type"])

            try:
                card_sun_boost = SunColours(card["sunBoost"])
            except:
                card_sun_boost = None

            try:
                card_sun_diminish = SunColours(card["sunDiminish"])
            except:
                card_sun_diminish = None

            try:
                self.cards.append(
                    SoothCard(
                        card_name,
                        card_number,
                        card_image_link,
                        card_link,
                        card_family,
                        card_type,
                        card_sun_boost,
                        card_sun_diminish
                    )
                )
            except:
                print("COULD NOT ADD " + card_name)
        self.current_sooth_deck = self.cards.copy()

    def get_sooth_card(self, sooth_name_prefix):
        print(sooth_name_prefix)
        for card in self.cards:
            if card.name.lower().startswith(sooth_name_prefix.lower()):
                print("--" + card.name)
                return card
        print('--could not find sooth card')
        return None

    def get_sooth_card_from_deck(self, sooth_name_prefix):
        for card in self.current_sooth_deck:
            if card.name.lower().startswith(sooth_name_prefix.lower()):
                print("--" + card.name)
                self.current_sooth_deck.remove(card)
                return card
        print('--could not find sooth card in remaining deck')
        return None

    def get_random_sooth_card(self):
        card = random.choice(self.cards)
        print("--" + card.name)
        return card

    def get_random_sooth_card_from_deck(self):
        card = random.choice(self.current_sooth_deck)
        print("--" + card.name)
        self.current_sooth_deck.remove(card)
        return card

    def next_path_of_suns(self, given_card_name=''):
        if given_card_name != '':
            card = self.get_sooth_card_from_deck(given_card_name)
        else:
            card = self.get_random_sooth_card_from_deck()
        self.path_of_suns.next_sun(card)
        return self.path_of_suns.get_current_active_sun()

    def get_active_sooth_cards(self):
        return (self.path_of_suns.get_current_active_sun(), self.path_of_suns.get_current_active_invisible_sun())


class SoothCard:
    def __init__(self, card_name, card_number, card_image_link, card_link, card_family, card_type, card_sun_boost, card_sun_diminish):
        self.name = card_name
        self.number = card_number
        self.image_link = card_image_link
        self.link = card_link
        self.family = card_family
        self.type = card_type
        self.sun_boost = card_sun_boost
        self.sun_diminish = card_sun_diminish

    def get_card_function(self, current_sun, player_names_by_family = PLAYERS_BY_FAMILY):
        players_not_in_family_list = []
        players_in_family = ""
        players_not_in_family = ""

        for family in player_names_by_family.keys():
            if (family == self.family):
                players_in_family = ', '.join(player_names_by_family[family])
            else:
                players_not_in_family_list += player_names_by_family[family]
        players_not_in_family = ', '.join(players_not_in_family_list)

        if (self.type == SoothCardType.SUN):
            boost_value = "+1"
            diminish_value = "-1"
            if (self.sun_boost == current_sun):
                boost_value = "+2"
            elif (self.sun_diminish == current_sun):
                diminish_value = "-2"

            function_description = boost_value + " to " + self.sun_boost.value + " effects\n"
            if self.sun_diminish != None:
                function_description += diminish_value + " to " + self.sun_diminish.value + " effects\n"
            if players_in_family != "":
                function_description += "+1 to all actions by " + players_in_family

            return function_description

        elif (self.type == SoothCardType.APPRENTICE):
            # Apprentice: −1 to all actions if heart is linked to family
            if (players_in_family != ""):
                return "-1 to all actions by " + players_in_family
            else:
                return "no effect"

        elif (self.type == SoothCardType.COMPANION):
            return "Duplicates the effects of the previously played card"

        elif (self.type == SoothCardType.ADEPT):
            return "Play another card on the next sun"

        elif (self.type == SoothCardType.DEFENDER):
            if (players_in_family != ""):
                return "+2 to all actions by " + players_in_family
            else:
                return "no effect as no players in the " + self.family.value + " family"

        elif (self.type == SoothCardType.NEMESIS):
            function_description = ""
            if (players_in_family != ""):
                function_description += "-2 to all actions by " + players_in_family + "\n"
            function_description += "-1 to all actions by " + players_not_in_family
            return function_description

        elif (self.type == SoothCardType.DEFENDER):
            # Defender: +2 to all actions if heart is linked to family
            if (players_in_family != ""):
                return "+2 to all actions by " + players_in_family
            else:
                return "no effect as no players in the " + self.family.value + " family"

        elif (self.type == SoothCardType.SOVEREIGN):
            # Sovereign: +1 to all actions, +2 if heart is linked to family
            function_description = ""
            if (players_in_family != ""):
                function_description += "+2 to all actions by " + players_in_family + "\n"
            function_description += "+1 to all actions by " + players_not_in_family
            return function_description


class PathOfSuns:
    def __init__(self):
        self.current_sun = 8
        self.current_path = [None for i in range(9)]
        self.current_sun_with_card = None
        self.invisible_sun_card = None

    def next_sun(self, card):
        self.current_sun = (self.current_sun + 1) % 9
        self.current_sun_with_card = SunWithCard(PATH_OF_SUNS[self.current_sun], card)
        self.current_path[self.current_sun] = self.current_sun_with_card
        if self.current_sun_with_card.sun_name == SunColours.INVISIBLE:
            self.invisible_sun_card = SunWithCard(PATH_OF_SUNS[self.current_sun], card)

    def get_current_active_sun(self):
        return self.current_sun_with_card

    def get_current_active_invisible_sun(self):
        return self.invisible_sun_card


class SunWithCard:
    def __init__(self, sun_name, sooth_card):
        self.sun_name = sun_name
        self.sooth_card = sooth_card
        self.sun_colour = SUNS_COLOURS[sun_name]
