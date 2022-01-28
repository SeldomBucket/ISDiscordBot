import os
import discord
import sooth
from dotenv import load_dotenv

load_dotenv()
TOKEN =                     os.getenv('DISCORD_TOKEN')
GUILD =                     os.getenv('DISCORD_GUILD')
INVISIBLE_SUN_SOOTH_CARD_LINK =   os.getenv('INVISIBLE_SUN_SOOTH_CARD_LINK')

VALID_COMMANDS = ('/sooth', '/spell')

client = discord.Client()

class CustomClient(discord.Client):
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
            response = self.get_message_response(message.content.split(' ')[:])
            # if response != '':
            await message.channel.send(response)

    def get_message_response(self, message):
        command = message[0].lower()
        if command == '/sooth':
            return self.sooth_commands(message[1:])
        if command == '/spell':
            return self.spell_commands(message[1:])
        else:
            return 'unrecognised command'

    def sooth_commands(self, message):
        print('SOOTH COMMANDS')
        if message == []:
            print('-RANDOM')
            return sooth.get_random_sooth_card()
        sooth_command = message[0].lower()
        if sooth_command == 'draw':
            print('-DRAW')
            return sooth.draw_random_sooth_card()
        else:
            return sooth.get_sooth_card(message[0])

    def spell_commands(self, message):
        return 'TODO implement spell commands'

sooth.set_sooth_link_base(INVISIBLE_SUN_SOOTH_CARD_LINK)
client = CustomClient()
client.run(TOKEN)
