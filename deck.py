import random

class Deck:
    def __init__(self, card_list, card_base_path):
        self.cards = []
        for card in card_list:
            self.cards.append(Card(card[0], card[1], card[2]))
        self.card_base_path = card_base_path
        self.cards_by_level = []
        for i in range(14):
            level = i+1
            self.cards_by_level.append([card for card in self.cards if card.level == level])

    def get_card_by_name(self, card_name):
        search_term = card_name.upper()
        search_term = search_term.replace(' ', '_')
        for card in self.cards:
            if (card.name.startswith(search_term)):
                print('--' + card.name)
                return self.card_base_path + card.name
        print('--card not recognised')

    def get_random_card(self):
        card = random.choice(self.cards)
        print(card)
        return self.card_base_path + card.name

    def get_random_card_with_level(self, level):
        return self.get_card_by_parameters(level, level, None)

    def get_card_by_parameters(self, lower_level, upper_level, colour):
        cards_to_choose_from = []
        for i in range(lower_level - 1, upper_level):
            cards_to_choose_from = cards_to_choose_from + self.cards_by_level[i]
        filtered_cards = cards_to_choose_from.copy()
        if colour:
            filtered_cards = [card for card in cards_to_choose_from if card.colour.lower() == colour.lower()]
        if len(filtered_cards) > 0:
            card = random.choice(filtered_cards)
            print('--' + card.name)
            return self.card_base_path + card.name
        return None





class Card:
    def __init__(self, name, level, colour):
        self.name = name
        self.level = level
        self.colour = colour

    def __str__(self):
        return """
            Name: {name}\n
            Level: {level}\n
            Colour{colour}""".format(name=self.name, level=self.level, colour=self.colour)



if __name__ == '__main__':
    pass