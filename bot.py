import os
import deck
import discord

from dotenv import load_dotenv
from ephemera_deck import EphemeraDeck
from incantation_deck import IncantationDeck
from kindled_items_deck import KindledItemsDeck
from objects_of_power_deck import ObjectsOfPowerDeck
from sooth import SoothDeck

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
INVISIBLE_SUN_SOOTH_CARD_LINK = os.getenv('INVISIBLE_SUN_SOOTH_CARD_LINK')
INVISIBLE_SUN_SOOTH_CARD_IMAGE_LINK = os.getenv('INVISIBLE_SUN_SOOTH_CARD_IMAGE_LINK')
INCANTATION_CARD_PATH = os.getenv('INCANTATION_CARD_PATH')
EPHEMERA_CARD_PATH = os.getenv('EPHEMERA_CARD_PATH')
OBJECTS_OF_POWER_CARD_PATH = os.getenv('OBJECTS_OF_POWER_CARD_PATH')

VALID_COMMANDS = (
    '/sooth',
    '/spell',
    '/vance',
    '/weaver',
    '/ephemera',
    '/eph',
    '/incantation',
    '/inc',
    '/objectofpower',
    '/obj',
    '/oop',
    '/kindleditems',
    '/kin'
)


class CustomClient(discord.Client):
    def setup(self):
        self.sooth_deck = SoothDeck(INVISIBLE_SUN_SOOTH_CARD_LINK, INVISIBLE_SUN_SOOTH_CARD_IMAGE_LINK)
        self.incantation_deck = IncantationDeck(INCANTATION_CARD_PATH)
        self.ephemera_deck = EphemeraDeck(EPHEMERA_CARD_PATH)
        self.objects_of_power_deck = ObjectsOfPowerDeck(OBJECTS_OF_POWER_CARD_PATH)
        self.kindled_items_deck = KindledItemsDeck(OBJECTS_OF_POWER_CARD_PATH)

    async def on_ready(self):
        guild = discord.utils.get(client.guilds, name=GUILD)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    # TODO IS Help
    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content.startswith(VALID_COMMANDS):
            split_message = message.content.split(' ')[:]
            command = split_message[0].lower()
            if command == '/sooth':
                await self.sooth_commands(message.channel, split_message[1:])
            elif command == '/spell':
                await self.spell_commands(message.channel, split_message[1:])
            elif command == '/vance':
                await self.vance_commands(message.channel, split_message[1:])
            elif command == '/weaver':
                await self.incantation_commands(message.channel, split_message[1:])
            elif command in ['/ephemera', '/eph']:
                await self.ephemera_commands(message.channel, split_message[1:])
            elif command in ['/incantation', '/inc']:
                await self.incantation_commands(message.channel, split_message[1:])
            elif command in ['/objectofpower', '/obj', '/oop']:
                await self.object_of_power_commands(message.channel, split_message[1:])
            elif command in ['/kindleditems', '/kin']:
                await self.kindled_items_commands(message.channel, split_message[1:])
            else:
                await message.channel.send('unrecognised command')

    async def sooth_commands(self, channel, split_message):
        print('SOOTH COMMANDS')
        if split_message == []:
            print('-RANDOM')
            (image_link, card_link) = self.sooth_deck.get_random_sooth_card()
            await self.display_card_by_link(channel, image_link, link=card_link)
            return
        sooth_command = split_message[0].lower()
        if sooth_command == 'draw':
            print('-DRAW')
            (image_link, card_link) = self.sooth_deck.draw_random_sooth_card()
            await self.display_card_by_link(channel, image_link, link=card_link)
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
            (sun_with_card, invisible_sun_card) = self.sooth_deck.get_active_sooth_cards()
            if (sun_with_card == None and invisible_sun_card == None):
                await channel.send('NO ACTIVE SOOTH CARDS')
            if (sun_with_card != None):
                await channel.send('ACTIVE SOOTH CARDS')
                await self.display_sun_with_sooth_card(channel, sun_with_card)
            if (invisible_sun_card != None):
                await self.display_sun_with_sooth_card(channel, invisible_sun_card)
        else:
            search_term = split_message[0]
            for term in split_message[1:]:
                search_term = search_term + ' ' + term
            (image_link, card_link) = self.sooth_deck.get_sooth_card(search_term)
            if image_link and card_link:
                await self.display_card_by_link(channel, card_link, image_link)
            else:
                await channel.send('Sooth card not found')

    async def spell_commands(self, channel, split_message):
        # get named
        # get random
        # get random for level
        # get random in level range
        # get random for sun type
        await channel.send('TODO implement spell commands')

    async def vance_commands(self, channel, split_message):
        # get named
        # get random
        # get random for size
        await channel.send('TODO implement vance commands')

    async def weaver_commands(self, channel, split_message):
        # get named
        await channel.send('TODO implement weaver commands')

    async def ephemera_commands(self, channel, split_message):
        print('EPHEMERA COMMANDS')
        await self.basic_deck_commands(channel, split_message, self.ephemera_deck)

    async def incantation_commands(self, channel, split_message):
        print('INCANTATION COMMANDS')
        await self.basic_deck_commands(channel, split_message, self.incantation_deck)

    async def object_of_power_commands(self, channel, split_message):
        print('OBJECTS OF POWER COMMANDS')
        await self.basic_deck_commands(channel, split_message, self.objects_of_power_deck)

    async def kindled_items_commands(self, channel, split_message):
        print('KINDLED ITEMS COMMANDS')
        await self.basic_deck_commands(channel, split_message, self.kindled_items_deck)

    async def basic_deck_commands(self, channel, split_message, deck):
        if split_message == []:
            print('-RANDOM_BELOW_10')
            card_file = deck.get_random_card_with_level_below(10)
            await self.display_card_by_path(channel, card_file)
            return
        incantation_command = split_message[0].lower()
        if incantation_command in ['l', 'level'] or incantation_command.isdigit():
            level = 1
            try:
                level = int(split_message[1])
            except:
                level = int(incantation_command)
            print('-LEVEL {level}'.format(level=level))
            card_file = deck.get_random_card_with_level(level)
            await self.display_card_by_path(channel, card_file)
        elif incantation_command in ['lb', 'below', 'levelbelow']:
            level = int(split_message[1])
            print('-LEVEL_BELOW {level}'.format(level=level))
            card_file = deck.get_random_card_with_level_below(level)
            await self.display_card_by_path(channel, card_file)
        elif incantation_command in ['ll', 'between', 'levelbetween']:
            lower_level = int(split_message[1])
            upper_level = int(split_message[2])
            print('-LEVEL_RANGE {lower_level} to {upper_level}'.format(lower_level=lower_level, upper_level=upper_level))
            card_file = deck.get_random_card_in_level_range(lower_level, upper_level)
            await self.display_card_by_path(channel, card_file)
        elif incantation_command == 'all_levels':
            print('-ALL_LEVELS')
            card_file = deck.get_random_card()
            await self.display_card_by_path(channel, card_file)
        else:
            search_term = split_message[0]
            for term in split_message[1:]:
                search_term = search_term + ' ' + term
            print('-SEARCH {search_term}'.format(search_term=search_term))
            card_file = deck.get_card_by_name(search_term)
            if card_file:
                await self.display_card_by_path(channel, card_file)
            else:
                await channel.send('Card not found')

    async def display_image_with_link(self, channel, link, image_link):
        e = discord.Embed()
        e.set_image(url=image_link)
        e.title = link
        await channel.send(embed=e)

    async def display_sun_with_sooth_card(self, channel, sun_with_card):
        await self.display_card_by_link(
            channel,
            sun_with_card.sooth_card_image_link,
            sun_with_card.sun_colour,
            sun_with_card.sooth_card_link,
            sun_with_card.sun_name
        )

    async def display_card_by_link(self, channel, card_image_link, colour = discord.Colour.default(), link = '', footer = ''):
        e = discord.Embed()
        e.set_image(url=card_image_link)
        e.colour = colour
        e.title = link
        e.set_footer(text=footer)
        await channel.send(embed=e)

    async def display_card_by_path(self, channel, card_image_path):
        await channel.send(file=discord.File(card_image_path))


client = CustomClient()
client.setup()
client.run(TOKEN)
