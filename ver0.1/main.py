import chatbotRouter
from getpass import getpass

bot = chatbotRouter.Bot("kshr2d2@outlook.com", getpass('password : '))
bot.listen()
