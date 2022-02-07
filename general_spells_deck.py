from deck import Deck
import json
import re

class GeneralSpellsDeck(Deck):
    def __init__(self, card_path):
        json_string = ""
        loaded_spells = {}
        with open("general-spells.json", "r") as file:
            loaded_spells = json.load(file)
        processed_spell_list = []
        for spell in loaded_spells["spells"]:
            spell_title = spell["title"]
            spell_title = spell_title.replace(" ", "_")
            spell_title += ".jpg"
            spell_level = re.sub(r"\s\(\+\d di.+\)", "", spell["level"])
            spell_colour = spell["color"]
            processed_spell_list.append(tuple([spell_title, int(spell_level), spell_colour]))
        Deck.__init__(self, processed_spell_list, card_path)


if __name__ == '__main__':
    pass
