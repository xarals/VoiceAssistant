def log(user_text, bot_text):
    with open('chatlog.txt', 'a') as file:
        try:
            file.write("User: " + user_text + "\n")
        except:
            file.write("User: ERROR\n")
        try:
            file.write("BOT:  " + bot_text + "\n")
        except:
            file.write("BOT:  ERROR\n")
        file.close()