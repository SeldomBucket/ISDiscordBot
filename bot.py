import os
import discord
import sooth
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
INVISIBLE_SUN_SOOTH_CARD_LINK = os.getenv('INVISIBLE_SUN_SOOTH_CARD_LINK')
INVISIBLE_SUN_SOOTH_CARD_IMAGE_LINK = os.getenv('INVISIBLE_SUN_SOOTH_CARD_IMAGE_LINK')
print(INVISIBLE_SUN_SOOTH_CARD_LINK)
print(INVISIBLE_SUN_SOOTH_CARD_IMAGE_LINK)

VALID_COMMANDS = ('/sooth', '/spell', '/vance', '/weaver', '/eph', '/inc', '/obj')


class CustomClient(discord.Client):
    def setup(self):
        self.sooth_deck = sooth.SoothDeck(INVISIBLE_SUN_SOOTH_CARD_LINK, INVISIBLE_SUN_SOOTH_CARD_IMAGE_LINK)

    async def on_ready(self):
        guild = discord.utils.get(client.guilds, name=GUILD)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

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
            elif command == '/eph':
                await self.ephemera_commands(message.channel, split_message[1:])
            elif command == '/inc':
                await self.incantation_commands(message.channel, split_message[1:])
            elif command == '/obj':
                await self.object_of_power_commands(message.channel, split_message[1:])
            else:
                await message.channel.send('unrecognised command')

    async def sooth_commands(self, channel, split_message):
        print('SOOTH COMMANDS')
        if split_message == []:
            print('-RANDOM')
            (card_link, image_link) = self.sooth_deck.get_random_sooth_card()
            await channel.send(image_link)
            await channel.send(card_link)
        sooth_command = split_message[0].lower()
        if sooth_command == 'draw':
            print('-DRAW')
            (card_link, image_link) = self.sooth_deck.draw_random_sooth_card()
            await channel.send(image_link)
            await channel.send(card_link)
        elif sooth_command == 'path':
            print('-PATH')
            sun_with_card = None
            if len(split_message) == 1:
                sun_with_card = self.sooth_deck.next_path_of_suns()
            else:
                sun_with_card = self.sooth_deck.next_path_of_suns(split_message[1])
            await self.display_sun_with_card(channel, sun_with_card)
        elif sooth_command == 'active':
            print('-ACTIVE')
            (sun_with_card, invisible_sun_card) = self.sooth_deck.get_active_sooth_cards()
            if (sun_with_card == None and invisible_sun_card == None):
                await channel.send('NO ACTIVE SOOTH CARDS')
            if (sun_with_card != None):
                await channel.send('ACTIVE SOOTH CARDS')
                await self.display_sun_with_card(channel, sun_with_card)
            if (invisible_sun_card != None):
                await self.display_sun_with_card(channel, invisible_sun_card)
        else:
            await channel.send(self.sooth_deck.get_sooth_card(split_message[0]))

    async def spell_commands(self, channel, split_message):
        await channel.send('TODO implement spell commands')

    async def vance_commands(self, channel, split_message):
        await channel.send('TODO implement vance commands')

    async def weaver_commands(self, channel, split_message):
        await channel.send('TODO implement weaver commands')

    async def ephemera_commands(self, channel, split_message):
        await channel.send('TODO implement ephemera commands')

    async def incantation_commands(self, channel, split_message):
        await channel.send('TODO implement incantation commands')

    async def object_of_power_commands(self, channel, split_message):
        await channel.send('TODO implement ephemera commands')

    async def display_image_with_link(self, channel, image_link, link):
        e = discord.Embed()
        e.set_image(url=image_link)
        e.title = link
        await channel.send(embed=e)

    async def display_sun_with_card(self, channel, sun_with_card):
        e = discord.Embed()
        e.set_image(url=sun_with_card.sooth_card_link)
        e.colour = sun_with_card.colour
        e.title = sun_with_card.sun_name
        await channel.send(embed=e)


client = CustomClient()
client.setup()
client.run(TOKEN)
