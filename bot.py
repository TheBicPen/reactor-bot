import discord
import re
import json

class MyClient(discord.Client):

    emoji_re = re.compile(r":([\w\d_-]{1,20}):")
    emoji_to_img = None

    async def on_ready(self):
        with open("data/emoji_map.json", "r") as j:
            self.emoji_to_img = json.load(j)
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
        
        elif message.content == 'load':
            loaded=0
            for i, emoji in enumerate(message.guild.emojis):
                self.emoji_to_img[emoji.name] = str(emoji.url)
                loaded = i
            with open("data/emoji_map.json", "w") as j:
                json.dump(self.emoji_to_img, j)
            await message.channel.send(f"Loaded {loaded} emojis from server")
        
        else:
            for match in self.emoji_re.finditer(message.content):
                emoji = match.group(1)
                print(f"Emoji spotted:'{emoji}'")
                if emote_img := self.get_emoji(emoji):
                    await message.channel.send(f"{message.author.mention} says :{emoji}:\n{emote_img}")
                else:
                    print("Emoji not found")
    
    def get_emoji(self, emoji: str):
        if img_file := self.emoji_to_img.get(emoji):
            return img_file
        return None

with open("credentials/discord_token.txt", "r") as f:
    token = f.read()
    client = MyClient()
    client.run(token)
