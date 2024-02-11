from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте, {user.mention_html()}! Чтобы найти расшифровку аббревиатуры введите её боту.",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    helptext = f'Данный бот поможет вам найти расшифровку аббревиатур английского языка.\nЧтобы найти аббревиатуру введите её боту и он попробует её найти.'
    await update.message.reply_text(helptext)


async def returnabbrev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    connections = list()
    # print(update)
    
    with open('abbreviations.txt', encoding='utf-8') as f:
        reader = f.readlines()

        for number, i in enumerate(reader):
            if i.split(';')[0].lower() == update.message.text.lower():
                await update.message.reply_text(i.split(';')[1])
                break
            else:
                con = findcorrelations(i.split(';')[0].lower(), update.message.text.lower())

                if con != None:
                    connections.append(con)

            if (number + 1 == len(reader)) and (i.split(';')[0].lower() not in i.split()):
                if len(connections) == 0:
                    await update.message.reply_text('Аббревиатуры не найдено')
                else:
                    txt = f'Данной аббревиатуры не найдено, однако возможно вы имели ввиду "{sorted(connections)[0][0]}"'
                    await update.message.reply_text(txt)


def findcorrelations(abv, messg):   # поиск похожих аббревиатур
    dict = {
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0,
        'e': 0,
        'f': 0,
        'g': 0,
        'h': 0,
        'j': 0,
        'k': 0,
        'l': 0,
        'm': 0,
        'n': 0,
        'o': 0,
        'p': 0,
        'q': 0,
        'r': 0,
        's': 0,
        't': 0,
        'u': 0,
        'v': 0,
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0
        }

    messg = messg.lower()
    count = 0

    for i in messg:
        dict[i] = messg.count(i)
    
    for key in dict.keys():
        if dict[key] != 0:
            if key in abv:
                count += abv.count(key)
    
    sim = (count / len(abv)) * 100   # в процентах

    if round(sim) >= 65:
        return [abv, round(sim)]


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6266082698:AAGpswBIwmDH9T_Nk32ih0b7RXGH4jdqpE8").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, returnabbrev))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()