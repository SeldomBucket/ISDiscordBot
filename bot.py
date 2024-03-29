import os
import discord
import argparse

from deck_json import Deck
from dotenv import load_dotenv
from old_sooth_deck import OldSoothDeck
from sooth_deck import SoothDeck

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SOOTH_CARD_LINK = os.getenv('SOOTH_CARD_LINK')
SOOTH_CARD_IMAGE_LINK = os.getenv('SOOTH_CARD_IMAGE_LINK')
INCANTATION_CARD_PATH = os.getenv('INCANTATION_CARD_PATH')
EPHEMERA_CARD_PATH = os.getenv('EPHEMERA_CARD_PATH')
OBJECTS_OF_POWER_CARD_PATH = os.getenv('OBJECTS_OF_POWER_CARD_PATH')
GENERAL_SPELLS_CARD_PATH = os.getenv('GENERAL_SPELLS_CARD_PATH')

BOT_COMMANDS = ['is']
SOOTH_COMMANDS = ['sooth', 'so']
VANCE_COMMANDS = ['vance', 'v']
WEAVER_COMMANDS = ['weaver', 'w']
SPELL_COMMANDS = ['spell', 'spe']
EPHEMERA_COMMANDS = ['ephemera', 'eph', 'e']
INCANTATION_COMMANDS = ['incantation', 'inc', 'i']
OBJECT_OF_POWER_COMMANDS = ['objectofpower', 'obj', 'oop', 'o']
KINDLED_ITEM_COMMANDS = ['kindleditems', 'kin']

VALID_COMMANDS = tuple(
    BOT_COMMANDS +
    SOOTH_COMMANDS +
    VANCE_COMMANDS +
    WEAVER_COMMANDS +
    SPELL_COMMANDS +
    EPHEMERA_COMMANDS +
    INCANTATION_COMMANDS +
    OBJECT_OF_POWER_COMMANDS +
    KINDLED_ITEM_COMMANDS
    )

class CustomClient(discord.Client):
    def setup(self):
        self.card_search_parser = argparse.ArgumentParser(description='Argument parser for basic card search', conflict_handler="resolve")
        self.card_search_parser.add_argument('-h', '--help', action='store_true', help='Show this message' )
        self.card_search_parser.add_argument('-l', '--level', type=int, help='A level for card searching')
        self.card_search_parser.add_argument('-lb', '--lower-bound', type=int, default=1, help='A lower level bound for card searching')
        self.card_search_parser.add_argument('-ub', '--upper-bound', type=int, default=10, help='An upper level bound for card searching')
        self.card_search_parser.add_argument('-c', '--colour', type=str, help='A colour to search')
        self.card_search_parser.add_argument('-s', '--search', metavar='SEARCH_TERM', type=str, nargs='+', default=None, help='A lower level bound for card searching' )

        self.incantation_deck = Deck('decks/incantation.json', INCANTATION_CARD_PATH)
        self.ephemera_deck = Deck('decks/ephemera.json', EPHEMERA_CARD_PATH)
        self.objects_of_power_deck = Deck('decks/objects.json', OBJECTS_OF_POWER_CARD_PATH)
        self.kindled_items_deck = Deck('decks/kindled.json', OBJECTS_OF_POWER_CARD_PATH)
        self.general_spells_deck = Deck('decks/general-spells.json', GENERAL_SPELLS_CARD_PATH)

        self.sooth_deck = SoothDeck('decks/sooth.json', SOOTH_CARD_LINK, SOOTH_CARD_IMAGE_LINK)
        print('-SOOTH LOAD')
        self.sooth_deck.load()

    async def on_ready(self):
        guild = discord.utils.get(client.guilds, name=GUILD)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(self, message):
        if message.author == client.user:
            return
        if not (message.content.startswith('/') or message.content.startswith('!')):
            return
        stripped_message = message.content[1:]
        if stripped_message.startswith(VALID_COMMANDS):
            split_message = stripped_message.split(' ')[:]
            command = split_message[0].lower()
            if command in BOT_COMMANDS:
                help_string =  'Sooth Deck Commands:\t\t\t\t\t' + ', '.join(SOOTH_COMMANDS) + '\n'
                help_string += 'Vance Spell Deck Commands:\t\t\t' + ', '.join(VANCE_COMMANDS) + '\n'
                help_string += 'Weaver Aggregate Commands:\t\t\t' + ', '.join(WEAVER_COMMANDS) + '\n'
                help_string += 'General Spell Deck Commands:\t\t\t' + ', '.join(SPELL_COMMANDS) + '\n'
                help_string += 'Ephemera Deck Commands:\t\t\t\t' + ', '.join(EPHEMERA_COMMANDS) + '\n'
                help_string += 'Incantation Deck Commands:\t\t\t' + ', '.join(INCANTATION_COMMANDS) + '\n'
                help_string += 'Object of Power Deck Commands:\t\t' + ', '.join(OBJECT_OF_POWER_COMMANDS) + '\n'
                help_string += 'Kindled Item Deck Commands:\t\t\t' + ', '.join(KINDLED_ITEM_COMMANDS) + '\n'
                e = discord.Embed()
                e.title = 'Valid Commands (prefix with / or !, use -h afterwards for help)'
                e.set_footer(text=help_string)
                await message.channel.send(embed=e)
                return
            # Complex deck commands
            if command in SOOTH_COMMANDS:
                await self.sooth_commands(message.channel, split_message[1:])
                return
            elif command in VANCE_COMMANDS:
                await self.vance_commands(message.channel, split_message[1:])
                return
            elif command in WEAVER_COMMANDS:
                await self.weaver_commands(message.channel, split_message[1:])
                return
            # Standard deck commands
            try:
                should_display_help = len(split_message[1:]) != 0
                parsed_args = vars(self.card_search_parser.parse_args(split_message[1:]))
            except:
                await message.channel.send('unrecognised command')
                return
            if command in SPELL_COMMANDS:
                await self.general_spells_commands(message.channel, parsed_args, should_display_help)
            elif command in EPHEMERA_COMMANDS:
                await self.ephemera_commands(message.channel, parsed_args, should_display_help)
            elif command in INCANTATION_COMMANDS:
                await self.incantation_commands(message.channel, parsed_args, should_display_help)
            elif command in OBJECT_OF_POWER_COMMANDS:
                await self.object_of_power_commands(message.channel, parsed_args, should_display_help)
            elif command in KINDLED_ITEM_COMMANDS:
                await self.kindled_items_commands(message.channel, parsed_args, should_display_help)

    async def sooth_commands(self, channel, split_message):
        print('SOOTH COMMANDS')
        if split_message == []:
            print('-RANDOM')
            sooth_card = self.sooth_deck.get_random_sooth_card()
            await self.display_sooth_card_with_link(channel, sooth_card.image_link, link=sooth_card.link)
            return
        sooth_command = split_message[0].lower()
        if sooth_command == '-h' or sooth_command == '--help' or sooth_command == 'help':
            e = discord.Embed()
            help_text = 'The path of suns saves and loads automatically, so be careful with these commands!\n'
            help_text += 'draw:     Draw a card from the sooth deck and saves the path state.\n'
            help_text += 'path:     Play the next card on the path of suns. Follow with a card name to use that card next.\n'
            help_text += 'active:   Show the current active sooth cards.\n'
            help_text += 'clear:    Clears the current path of suns.\n'
            help_text += 'reset:    Resets the sooth deck.\n'
            e.set_footer(text=help_text)
            await channel.send(embed=e)
        elif sooth_command == 'draw':
            print('-DRAW')
            card = None
            if len(split_message) == 1:
                card = self.sooth_deck.get_random_sooth_card_from_deck()
            else:
                card = self.sooth_deck.get_sooth_card_from_deck(split_message[1])
            await self.display_sooth_card_with_link(channel, card.image_link, link=card.link)
        elif sooth_command == 'path':
            print('-PATH')
            sun_with_card = None
            if len(split_message) == 1:
                sun_with_card = self.sooth_deck.next_path_of_suns()
            else:
                sun_with_card = self.sooth_deck.next_path_of_suns(split_message[1])
            await self.display_sun_with_sooth_card(channel, sun_with_card)
        elif sooth_command == 'active':
            print('-ACTIVE')
            (sun_with_card, card) = self.sooth_deck.get_active_sooth_cards()
            if (sun_with_card == None and card == None):
                await channel.send('NO ACTIVE SOOTH CARDS')
            if (sun_with_card != None):
                await channel.send('ACTIVE SOOTH CARDS')
                await self.display_sun_with_sooth_card(channel, sun_with_card)
            if (card != None):
                await self.display_sun_with_sooth_card(channel, card)
        elif sooth_command == 'clear':
            print('-CLEAR')
            self.sooth_deck.path_of_suns.clear_path()
            await channel.send('CLEARED PATH OF SUNS')
        elif sooth_command == 'reset':
            print('-RESET')
            self.sooth_deck.reset()
            await channel.send('RESET SOOTH DECK')
        else:
            search_term = split_message[0]
            for term in split_message[1:]:
                search_term = search_term + ' ' + term
            sooth_card = self.sooth_deck.get_sooth_card(search_term)
            if sooth_card:
                await self.display_sooth_card_with_link(channel, sooth_card.image_link, link=sooth_card.link)
            else:
                e = discord.Embed()
                e.set_footer(text='Sooth card not found')
                e.colour = discord.Colour.red()
                await channel.send(embed=e)

    async def vance_commands(self, channel, split_message):
        # get named
        # get random
        # get random for size
        await channel.send('TODO implement vance commands')

    async def weaver_commands(self, channel, split_message):
        # get named
        await channel.send('TODO implement weaver commands')

    async def general_spells_commands(self, channel, parsed_args, should_display_help):
        print('GENERAL SPELL COMMANDS')
        await self.basic_deck_commands(channel, parsed_args, should_display_help, self.general_spells_deck)

    async def ephemera_commands(self, channel, parsed_args, should_display_help):
        print('EPHEMERA COMMANDS')
        await self.basic_deck_commands(channel, parsed_args, should_display_help, self.ephemera_deck)

    async def incantation_commands(self, channel, parsed_args, should_display_help):
        print('INCANTATION COMMANDS')
        await self.basic_deck_commands(channel, parsed_args, should_display_help, self.incantation_deck)

    async def object_of_power_commands(self, channel, parsed_args, should_display_help):
        print('OBJECTS OF POWER COMMANDS')
        await self.basic_deck_commands(channel, parsed_args, should_display_help, self.objects_of_power_deck)

    async def kindled_items_commands(self, channel, parsed_args, should_display_help):
        print('KINDLED ITEMS COMMANDS')
        await self.basic_deck_commands(channel, parsed_args, should_display_help, self.kindled_items_deck)

    async def basic_deck_commands(self, channel, parsed_args, should_display_help, deck):
        print(parsed_args)
        if parsed_args['help']:
            print('-HELP')
            e = discord.Embed()
            e.set_footer(text=self.card_search_parser.format_help())
            await channel.send(embed=e)
        elif parsed_args['search'] != None:
            complete_search_term = ' '.join(parsed_args['search'])
            print('-SEARCH {complete_search_term}'.format(complete_search_term=complete_search_term))
            card_file = deck.get_card_by_name(complete_search_term)
            if card_file:
                await self.display_card_by_path(channel, card_file)
            else:
                e = discord.Embed()
                e.set_footer(text='Card not found')
                await channel.send(embed=e)
        else:
            if parsed_args['level'] != None:
                print('-LEVEL {level}'.format(level=parsed_args['level']))
                lower_bound = parsed_args['level']
                upper_bound = parsed_args['level']
            else:
                lower_bound = parsed_args['lower_bound']
                upper_bound = parsed_args['upper_bound']
                print('-LEVEL_RANGE {lower_level} to {upper_level}'.format(lower_level=lower_bound, upper_level=upper_bound))
            colour = None
            if parsed_args['colour']:
                colour = parsed_args['colour']
                print('-COLOUR {colour}'.format(colour=colour))
            card_file = deck.get_card_by_parameters(lower_bound, upper_bound, colour)
            if card_file:
                await self.display_card_by_path(channel, card_file)
            else:
                e = discord.Embed()
                e.set_footer(text='No card matching those parameters found')
                e.colour = discord.Colour.red()
                await channel.send(embed=e)

    async def display_image_with_link(self, channel, link, image_link):
        e = discord.Embed()
        e.set_image(url=image_link)
        e.title = link
        await channel.send(embed=e)

    async def display_sun_with_sooth_card(self, channel, sun_with_card):
        await self.display_sooth_card_with_link(
            channel,
            sun_with_card.sooth_card.image_link,
            sun_with_card.sun_colour,
            sun_with_card.sooth_card.link,
            self.sooth_deck.get_card_function(sun_with_card),
            sun_with_card.sun_name.value + " Sun"
        )

    async def display_sooth_card_with_link(self, channel, card_image_link, colour = discord.Colour.default(), link = '', description = '', footer = ''):
        e = discord.Embed()
        e.set_image(url=card_image_link)
        e.colour = colour
        e.title = description
        e.set_footer(text=footer)
        await channel.send(link, embed=e)

    async def display_card_by_path(self, channel, card_image_path):
        await channel.send(file=discord.File(card_image_path))


client = CustomClient()
client.setup()
client.run(TOKEN)
