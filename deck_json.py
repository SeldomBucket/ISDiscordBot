import random
import json
import re


class Deck:
    def __init__(self, json_path, card_base_path):
        self.card_base_path = card_base_path
        self.cards = []
        json_string = ""
        loaded_cards = {}
        with open(json_path, "r") as file:
            loaded_cards = json.load(file)
        processed_card_list = []
        for card in loaded_cards["cards"]:
            card_title = card["title"]

            card_file = card_title.replace(" ", "_") + ".jpg"

            # remove the (+x die/dice) from levels
            card_level = re.sub(r"\s\(\+\d di.+\)", "", card["level"])

            card_color = card["colour"]

            card_description = card["description"]

            try:
                card_depletion = card["depletion"]
            except:
                card_depletion = None

            try:
                card_effect_depletion = card["effect_depletion"]
            except:
                card_effect_depletion = None

            try:
                card_object_depletion = card["object_depletion"]
            except:
                card_object_depletion = None

            try:
                card_form = card["form"]
            except:
                card_form = None

            self.cards.append(
                Card(
                    card_file,
                    card_title,
                    int(card_level),
                    card_color,
                    card_description,
                    card_depletion,
                    card_effect_depletion,
                    card_object_depletion,
                    card_form
                    )
                )
        self.cards_by_level = []
        for i in range(17):
            level = i+1
            self.cards_by_level.append([card for card in self.cards if card.level == level])

    def get_card_by_name(self, filename):
        search_term = filename.upper()
        search_term = search_term.replace(' ', '_')
        for card in self.cards:
            if (card.filename.startswith(search_term)):
                print('--' + card.title)
                return self.card_base_path + card.filename
        print('--card not recognised')

    def get_random_card(self):
        card = random.choice(self.cards)
        print(card)
        return self.card_base_path + card.filename

    def get_card_by_parameters(self, lower_level, upper_level, colour):
        cards_to_choose_from = []
        for i in range(lower_level - 1, upper_level):
            cards_to_choose_from = cards_to_choose_from + self.cards_by_level[i]
        filtered_cards = cards_to_choose_from.copy()
        if colour:
            filtered_cards = [card for card in cards_to_choose_from if card.colour.lower() == colour.lower()]
        if len(filtered_cards) > 0:
            card = random.choice(filtered_cards)
            print('--' + card.title)
            return self.card_base_path + card.filename
        return None


class Card:
    def __init__(self, filename, title, level, colour, description, depletion, effect_depletion, object_depletion, form):
        self.filename = filename
        self.title = title
        self.level = level
        self.colour = colour
        self.description = description
        self.depletion = depletion
        self.effect_depletion = effect_depletion
        self.object_depletion = object_depletion
        self.form = form

    def __str__(self):
        return """
            Name: {title}\n
            Level: {level}\n
            Colour: {colour}
            Description: {description}"""
            .format(
                title=self.title, 
                level=self.level, 
                description=self.description)


if __name__ == '__main__':
    pass