import  discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


client = MyClient()
client.run('NjY4OTUyNDAyMDMxODA0NDI1.XiYwkQ.dpQZMfuOGWQ9xWKJIe5bX1DZGGE')
client.on_ready()
client.on_message()
