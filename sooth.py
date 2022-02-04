import random
import os
from discord import Colour

PATH_OF_SUNS = [
    'silver',
    'green',
    'blue',
    'indigo',
    'grey',
    'pale',
    'red',
    'gold',
    'invisible',
]

SUNS_COLOURS = {
    'silver': Colour.from_rgb(211, 229, 240),
    'green': Colour.green(),
    'blue': Colour.blue(),
    'indigo': Colour.from_rgb(0, 21, 181),
    'grey': Colour.from_rgb(100, 100, 100),
    'pale': Colour.from_rgb(190, 190, 190),
    'red': Colour.red(),
    'gold': Colour.gold(),
    'invisible': Colour.from_rgb(255, 255, 255),
}

# TODO sooth card class with suits and functions
# TODO reset path of suns function

SOOTH_DECK = {
    'Hidden Moon': '01',
    'Incriminating Skull': '02',
    'Compelling Voice': '03',
    'Weeping Priest': '04',
    'Crowded Tomb': '05',
    'Unknowable Truth': '06',
    'Relentless Rumor': '07',
    'Mysterious Rune': '08',
    'Sealed Door': '09',
    'Endless Maze': '10',
    'Raven': '11',
    'Alchemist': '12',
    'Conspirator': '13',
    'Devil': '14',
    'Revolutionary': '15',
    'Blind Guardian': '16',
    'Suspicious Hound': '17',
    'Whispering Lover': '18',
    'Savage Sword': '19',
    'Inevitable Cataclysm': '20',
    'Questing Knight': '21',
    'Eternal Mountain': '22',
    'Elusive Sleep': '23',
    'Revealing Knife': '24',
    'Enticing Jewel': '25',
    'Ambassador': '26',
    'Imperator': '27',
    'Swan': '28',
    'Doctor': '29',
    'Messiah': '30',
    'Looming Shade': '31',
    'Ghostly Presence': '32',
    'Harvesting Spider': '33',
    'Banished Serpent': '34',
    'Forgotten Prisoner': '35',
    'Untrustworthy Mirror': '36',
    'Misremembered Dream': '37',
    'Endless Woods': '38',
    'Enveloping Darkness': '39',
    'Fleeting Moment': '40',
    'Jackal': '41',
    'Assassin': '42',
    'Rat': '43',
    'Driver': '44',
    'Watcher': '45',
    'Lost Star': '46',
    'Misunderstood Beast': '47',
    'Golden Ship': '48',
    'Unwelcome Child': '49',
    'Empty Gallows': '50',
    'Imprisoning Ice': '51',
    'Dangerous Elixir': '52',
    'Tyrannical Clock': '53',
    'Forbidden Game': '54',
    'Lucky Coin': '55',
    'Monarch': '56',
    'Cat': '57',
    'Angel': '58',
    'Vizier': '59',
    'Hunter': '60'
}


class SoothDeck:
    def __init__(self, card_base_link, card_base_image_link):
        self.sooth_card_link_base = card_base_link
        self.sooth_card_image_link_base = card_base_image_link
        self.path_of_suns = PathOfSuns()
        self.current_sooth_deck = SOOTH_DECK.copy()

    def get_sooth_link(self, sooth_card_number):
        return self.sooth_card_link_base + f'{sooth_card_number}'

    def get_sooth_image_link(self, sooth_card_number):
        return self.sooth_card_image_link_base + f'{sooth_card_number}.png'

    def get_sooth_card(self, sooth_name_prefix):
        for key in SOOTH_DECK:
            if key.lower().startswith(sooth_name_prefix.lower()):
                sooth_card_number = SOOTH_DECK[key]
                return (self.get_sooth_image_link(sooth_card_number), self.get_sooth_link(sooth_card_number))
        print('--sooth card not recognised')
        return (None, None)

    def get_random_sooth_card_name(self, deck=SOOTH_DECK):
        card_name = random.choice(list(deck.items()))[0]
        print('--' + card_name)
        return card_name

    def get_random_sooth_card(self):
        return self.get_sooth_card(self.get_random_sooth_card_name())

    def draw_random_sooth_card(self):
        if self.current_sooth_deck == {}:
            return '--SOOTH DECK IS EMPTY'
        card_name = self.get_random_sooth_card_name(self.current_sooth_deck)
        self.current_sooth_deck.pop(card_name)
        return self.get_sooth_card(card_name)

    def next_path_of_suns(self, given_card_name=''):
        card_link = ''
        card_image_link = ''
        if given_card_name != '':
            (card_image_link, card_link) = self.get_sooth_card(given_card_name)
            for key in self.current_sooth_deck:
                if key.lower().startswith(given_card_name.lower()):
                    self.current_sooth_deck.pop(key)
                    break
        else:
            (card_image_link, card_link) = self.draw_random_sooth_card()
        self.path_of_suns.next_sun(card_link, card_image_link)
        return self.path_of_suns.get_current_active_sun()

    def get_active_sooth_cards(self):
        return (self.path_of_suns.get_current_active_sun(), self.path_of_suns.get_current_active_invisible_sun())


class PathOfSuns:
    def __init__(self):
        self.current_sun = 8
        self.current_path = [None for i in range(9)]
        self.current_sun_with_card = None
        self.invisible_sun_card = None

    def next_sun(self, card_link, card_image_link):
        self.current_sun = (self.current_sun + 1) % 9
        self.current_sun_with_card = SunWithCard(PATH_OF_SUNS[self.current_sun], card_link, card_image_link)
        self.current_path[self.current_sun] = self.current_sun_with_card
        if self.current_sun_with_card.sun_name == 'invisible':
            self.invisible_sun_card = SunWithCard(PATH_OF_SUNS[self.current_sun], card_link, card_image_link)

    def get_current_active_sun(self):
        return self.current_sun_with_card

    def get_current_active_invisible_sun(self):
        return self.invisible_sun_card


class SunWithCard:
    def __init__(self, sun_name, sooth_card_link, sooth_card_image_link):
        self.sun_name = sun_name
        self.sooth_card_link = sooth_card_link
        self.sooth_card_image_link = sooth_card_image_link
        self.sun_colour = SUNS_COLOURS[sun_name]


if __name__ == '__main__':
    pass
