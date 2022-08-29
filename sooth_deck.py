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

PATH_SAVE_FILE = 'decks/sun_state.json'

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

    def reset(self):
        self.current_sooth_deck = self.cards.copy()

    def load(self):
        from_file = ''
        with open(PATH_SAVE_FILE, 'r') as f:
            from_file = f.read()
        saved_path = json.loads(from_file)

        self.path_of_suns.clear_path()
        for sun in saved_path['path_of_suns']:
            self.next_path_of_suns(sun['name'])
        self.path_of_suns.current_sun = saved_path['current_sun']

    def get_card_function(self, sun_with_card, player_names_by_family = PLAYERS_BY_FAMILY):
        card = sun_with_card.sooth_card
        current_sun = sun_with_card.sun_name
        players_not_in_family_list = []
        players_in_family = ""
        players_not_in_family = ""

        for family in player_names_by_family.keys():
            if (family == card.family):
                players_in_family = ', '.join(player_names_by_family[family])
            else:
                players_not_in_family_list += player_names_by_family[family]
        players_not_in_family = ', '.join(players_not_in_family_list)

        if (card.type == SoothCardType.SUN):
            boost_value = "+1"
            diminish_value = "-1"
            if (card.sun_boost == current_sun):
                boost_value = "+2"
            elif (card.sun_diminish == current_sun):
                diminish_value = "-2"

            function_description = boost_value + " to " + card.sun_boost.value + " effects\n"
            if card.sun_diminish != None:
                function_description += diminish_value + " to " + card.sun_diminish.value + " effects\n"
            if players_in_family != "":
                function_description += "+1 to all actions by " + players_in_family

            return function_description

        elif (card.type == SoothCardType.APPRENTICE):
            # Apprentice: −1 to all actions if heart is linked to family
            if (players_in_family != ""):
                return "-1 to all actions by " + players_in_family
            else:
                return "no effect"

        elif (card.type == SoothCardType.COMPANION):
            previous_card = self.path_of_suns.get_previous_card()
            function_description = self.get_card_function(previous_card)
            function_description += "\n--Duplicates " + previous_card.sooth_card.name + " on " + previous_card.sun_name.value + "--"
            return function_description

        elif (card.type == SoothCardType.ADEPT):
            return "Play another card on the next sun"

        elif (card.type == SoothCardType.DEFENDER):
            if (players_in_family != ""):
                return "+2 to all actions by " + players_in_family
            else:
                return "no effect as no players in the " + card.family.value + " family"

        elif (card.type == SoothCardType.NEMESIS):
            function_description = ""
            if (players_in_family != ""):
                function_description += "-2 to all actions by " + players_in_family + "\n"
            function_description += "-1 to all actions by " + players_not_in_family
            return function_description

        elif (card.type == SoothCardType.DEFENDER):
            # Defender: +2 to all actions if heart is linked to family
            if (players_in_family != ""):
                return "+2 to all actions by " + players_in_family
            else:
                return "no effect as no players in the " + card.family.value + " family"

        elif (card.type == SoothCardType.SOVEREIGN):
            # Sovereign: +1 to all actions, +2 if heart is linked to family
            function_description = ""
            if (players_in_family != ""):
                function_description += "+2 to all actions by " + players_in_family + "\n"
            function_description += "+1 to all actions by " + players_not_in_family
            return function_description


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


class PathOfSuns:
    def __init__(self):
        self.current_sun = 8
        self.current_path = [None for i in range(9)]
        self.current_sun_with_card = None
        self.invisible_sun_card = None

    def clear_path(self):
        self.current_sun = 8
        self.current_path = [None for i in range(9)]

    def next_sun(self, card):
        self.current_sun = (self.current_sun + 1) % 9
        new_sun = SunWithCard(PATH_OF_SUNS[self.current_sun], card)
        self.current_path[self.current_sun] = new_sun
        if new_sun.sun_name == SunColours.INVISIBLE:
            self.invisible_sun_card = SunWithCard(PATH_OF_SUNS[self.current_sun], card)
        self.save()

    def get_previous_card(self):
        previous_sun = self.current_sun-1
        if previous_sun < 0:
            previous_sun = 7
        return self.current_path[previous_sun]

    def get_current_active_sun(self):
        return self.current_path[self.current_sun]

    def get_current_active_invisible_sun(self):
        return self.current_path[8]

    def save(self):
        json_to_save = self.to_json()
        with open(PATH_SAVE_FILE, 'w') as f:
            f.write(json_to_save)

    def to_json(self):
        return json.dumps(self.__dict__())

    def __dict__(self):
        dict_rep = {}
        dict_rep['path_of_suns'] = []
        for sun in self.current_path:
            if sun != None:
                sun_dict_rep = sun.__dict__()
                dict_rep['path_of_suns'].append(sun_dict_rep)
        dict_rep['current_sun'] = self.current_sun
        return dict_rep



class SunWithCard:
    def __init__(self, sun_name, sooth_card):
        self.sun_name = sun_name
        self.sooth_card = sooth_card
        self.sun_colour = SUNS_COLOURS[sun_name]

    def __dict__(self):
        dict_rep = {}
        dict_rep['sun'] = self.sun_name.value
        dict_rep['name'] = self.sooth_card.name
        return dict_rep
