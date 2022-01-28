import random
import os

SOOTH_DECK={
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

current_sooth_deck = SOOTH_DECK.copy()

INVISIBLE_SUN_SOOTH_CARD_LINK = ''

def set_sooth_link_base(link):
    global INVISIBLE_SUN_SOOTH_CARD_LINK
    INVISIBLE_SUN_SOOTH_CARD_LINK = link
    print(INVISIBLE_SUN_SOOTH_CARD_LINK)

def get_sooth_link(sooth_card_number):
    return INVISIBLE_SUN_SOOTH_CARD_LINK + f'{sooth_card_number}.png'

def get_sooth_card(sooth_name):
    for key in SOOTH_DECK:
        if key.lower().startswith(sooth_name.lower()):
            return get_sooth_link(SOOTH_DECK[key])
    return '--sooth card not recognised'

def get_random_sooth_card_name():
    card_name = random.choice(list(SOOTH_DECK.items()))[0]
    print('--' + card_name)
    return card_name

def get_random_sooth_card():
    return get_sooth_card(get_random_sooth_card_name())

def draw_random_sooth_card():
    if current_sooth_deck == {}:
        return '--SOOTH DECK IS EMPTY'
    card_name = get_random_sooth_card_name()
    current_sooth_deck.pop(card_name)
    return get_sooth_card(card_name)

if __name__ == '__main__':
    pass
