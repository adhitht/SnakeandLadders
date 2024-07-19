import logging
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove , InlineKeyboardMarkup, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
import os
import pandas as pd
import json
import shutil
from dotenv import load_dotenv

#created import
from imagecreator import createimage

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.getenv('BOT_TOKEN')


full_path =  os.path.realpath(__file__)
currentpath, filename = os.path.split(full_path)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    reply = """Want to play Snake And Ladders with friends, thats why I am here. \n
How to Play:

1. Add @snakeandladdersbot to the group you want to Play.
2. Start a game with /newgame command.
3. Choose your coin by calling @snakeandladdersbot.
4. Once all players have joined start game with /start command"""
    update.message.reply_text(reply)

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


#Game Related Functions
def gamestatejson(torf,jsonforchat):
    with open(os.path.join(currentpath,"playing/"+jsonforchat),"w+"):
        data = [[torf]]
        jsondata = pd.DataFrame(data,columns=['gamestate'])
        jsondata.to_json(os.path.join(currentpath,"playing/"+jsonforchat))
def getplaystate(patht):
    with open(os.path.join(currentpath,"playing/"+patht),"r") as f:
        data = json.load(f)
    userid = []
    players = []
    position = []
    coincolor = []
    data1 = []
    #print(data["userid"]["0"])
    try:
        for i in range(len(data["userid"])):
            userid.append(data["userid"][str(i)])
            players.append(data["player"][str(i)])
            position.append(data["position"][str(i)])
            coincolor.append(data["coincolor"][str(i)])
            data1.append([data["userid"][str(i)],data["player"][str(i)],data["position"][str(i)],data["coincolor"][str(i)]])
        return [data1,userid,players,position,coincolor]
    except:
        return None

def editplaystate(data,patht):
    data1 = pd.DataFrame(data,columns=['userid','player',"position","coincolor"])
    data1.to_json(os.path.join(currentpath,"playing/"+patht))

def killgame(update, context):
    chattype = update.message.chat.type
    chatid = update.message.chat.id
    jsonforchat1 = str(chatid)+"/"+str(chatid)+".json"
    if chattype == "private":
        context.bot.send_message(chat_id=update.effective_chat.id,text="Kill a game in group")
    elif chattype == "group" or chattype == "supergroup":
        #gamestatejson("true",jsonforchat1)
        dataa = [[654646546545,"sample",56,"red"]]
        editplaystate(dataa,str(chatid)+"/playstate.json")
        gamestatejson("false",jsonforchat1)
        startgamestatus(chatid,"write","false")
        context.bot.send_message(chat_id=update.effective_chat.id,text="Game is over!",reply_markup = ReplyKeyboardRemove())

def joingame(update,context):
    chattype = update.message.chat.type
    chatid = update.message.chat.id
    if chattype == "private":
        context.bot.send_message(chat_id=update.effective_chat.id,text="Add me to a group and start the game")
    elif chattype == "group" or chattype == "supergroup":
        playgroups = os.listdir("playing")
        userid = update.message.from_user.id
        firstname = update.message.from_user.first_name
        '''
        position = [["abhinv",55],["amith",123,1105154]]
        df1 = pd.DataFrame(position,columns=['name','position',"id"])
        df1.to_json('example.json')'''
        data1 = [[userid,firstname,"lobby",None]]
        if getplaystate(str(chatid)+"/playstate.json") == None:
            pass
        elif 654646546545 in getplaystate(str(chatid)+"/playstate.json")[1]:
            pass
        else:
            data1 = getplaystate(str(chatid)+"/playstate.json")[0]
            data1.append([userid,firstname,"lobby",None])
        keyboard = [
        [
            InlineKeyboardButton("Select Your Coin", url="https://t.me/addstickers/snakeandladdersicons"),
        ]
        ]
        if userid not in getplaystate(str(chatid)+"/playstate.json")[1]:
            editplaystate(data1,str(chatid)+"/playstate.json")
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id,text="You have joined the game, now select your coin",reply_markup=reply_markup)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,text="You have already joined the game")
def getcolor(sticker):
    if sticker == "AgADOQMAAuSl4VY":
            #Blue
        return "blue"
    elif sticker == "AgADmgEAAg464FY":
            #Cyan
        return "cyan"
    elif sticker == "AgADJwIAAkIw4VY":
            #Green
        return "green"
    elif sticker == "AgADYwIAAivE4VY":
            #Magenta
        return "magenta"
    elif sticker == "AgAD_wIAAkP34VY":
            #Orange
        return "orange"
    elif sticker == "AgADeQIAAhj94VY":
            #Purple
        return "purple"
    elif sticker == "AgADUgIAAqUP4VY":
            #Yellow
        return "yellow"
    elif sticker == "AgADkwIAAnMX4FY":
            #red
        return "red"
    else:
        return None
def newgame(update, context):
    print(update, context)
    chattype = update.message.chat.type
    chatid = update.message.chat.id
    jsonforchat = str(chatid)+".json"
    jsonforchat1 = str(chatid)+"/"+str(chatid)+".json"
    firstname = update.message.from_user.first_name

    if chattype == "private":
        context.bot.send_message(chat_id=update.effective_chat.id,text="Add me to a group and post it there")
    elif chattype == "group" or chattype == "supergroup":
        playgroups = os.listdir("playing")
        '''
        position = [["abhinv",55],["amith",123,1105154]]
        df1 = pd.DataFrame(position,columns=['name','position',"id"])
        df1.to_json('example.json')
        '''
        if str(chatid) not in playgroups:
            os.mkdir("playing/"+str(chatid))
            kk = open(os.path.join(currentpath,str(chatid)+"/playstate.json"),"w+")
            gamestatejson("true",jsonforchat1)
            context.bot.send_message(chat_id=update.effective_chat.id,text='New Game Started')
        else:
            with open(os.path.join(currentpath,"playing/"+jsonforchat1),"r") as f:
                data = json.load(f)
            if data["gamestate"]["0"] == "true":
                context.bot.send_message(chat_id=update.effective_chat.id,text='Game is already started')
            else:
                gamestatejson("true",jsonforchat1)
                context.bot.send_message(chat_id=update.effective_chat.id,text='New Game Started')
def currentplayer(chatid,posss,what):
    if what == "write":
        with open("playing/"+str(chatid)+"/"+"currentplayer.txt","w+") as f:
            f.write(posss)
    elif what == "read":
        with open("playing/"+str(chatid)+"/"+"currentplayer.txt","r") as f:
            gg = f.readline()
        return gg
def startgamestatus(chatid,what,whatwrite):
    pathth = os.path.join(currentpath,"playing/"+str(chatid)+"/"+"startgame.txt")
    print(pathth)
    if what == "write":
        with open(pathth,"w+") as f:
            f.write(whatwrite)
    elif what == "read":
        if os.path.exists(pathth):
            with open(pathth,"r") as f:
                gg = f.readline()
            if gg == "true":
                return True
        else:
            with open(pathth,"w+") as f:
                f.write("false")
        return False

def startgame(update,context):
    chatid = update.message.chat.id
    dtr = getplaystate(str(chatid)+"/playstate.json")
    if startgamestatus(chatid,"read","asdasd"):
        context.bot.send_message(chat_id=update.effective_chat.id,text="Game is already started. Now roll die")
    else:
        if len(dtr[0]) == 0 or dtr[1][0] == 654646546545:
            context.bot.send_message(chat_id=update.effective_chat.id,text="You should have atleast one player")
        else:
            if None in dtr[4]:
                ii = dtr[4].index(None)
                keyboard = [
                [
                InlineKeyboardButton("Select Your Coin", url="https://t.me/addstickers/snakeandladdersicons"),
                ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id=update.effective_chat.id,text='{name} has not chosen colour. {name}, please choose color'.format(name=dtr[2][ii]),reply_markup=reply_markup)
            else:
                currentplayer(chatid,"0","write")
                replykeyboard = [
                        ["🎲"]
                    ]
                markup = ReplyKeyboardMarkup(replykeyboard, one_time_keyboard=True)
                context.bot.send_message(chat_id=update.effective_chat.id,text="Roll Dice",reply_markup=markup)
            startgamestatus(chatid,"write","true")
def stats(chatid):
    data = getplaystate(str(chatid)+"/playstate.json")
    noofplayer = len(data[0])
    currentplayer1 = data[0][int(currentplayer(chatid,"1","read"))][1]
    playersdata = ""
    for i in range(noofplayer):
        playersdata += data[0][i][1]+" - "+data[0][i][2]
    text = """Snake and ladders Stats
Number of Players: {noof}
Current Player: {cu}

Players and Position
{pla}
    """
    return text
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Dice',
            input_message_content=InputTextMessageContent("🎲")
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)
def answercallback(update, context):
    data = update.callback_query.data
    userid = update.callback_query.from_user.id
    if data == "helpdice":
        context.bot.send_message(chat_id=userid,text="Use :dice to roll the die or you can even find it in emojis tab")
    if "stats" in data:
        chatid = int(data[5:])
        print(type(chatid))
        print(chatid)
        context.bot.send_message(chat_id=userid,text=stats(chatid))
def changeposition(argument):
    position = {
        6: 45,
        2: 23,
        20: 59,
        43: 17,
        50: 5,
        52: 72,
        56: 8,
        57: 96,
        71: 92,
        73: 15,
        84: 58,
        87: 49,
        98: 40,
    }
    return position.get(argument, argument)

def send1(update, context,mesg):
    context.bot.send_message(chat_id=update.effective_chat.id,text=mesg)

def printupdate(update,context):
    print("UPDATE",update)
    chattype = update.message.chat.type
    chatid = update.message.chat.id
    jsonforchat = str(chatid)+".json"
    jsonforchat1 = str(chatid)+"/"+str(chatid)+".json"
    playgroups = os.listdir("playing")
    firstname = update.message.from_user.first_name
    if chattype == "group" or chattype == "supergroup":
        print("Group")
        userid = update.message.from_user.id
        try:
            update.message.forward_from
            isforwarded = True
        except:
            isforwarded = False
        print(isforwarded)
        if isforwarded == True:
            try:
                dtr = getplaystate(str(chatid)+"/playstate.json")
                if len(dtr[0]) == 0:
                    context.bot.send_message(chat_id=update.effective_chat.id,text="Game Over")
                    gamestatejson("false",jsonforchat1)
                diceval = update.message.dice.value
                print(diceval)
                print("Current Player Details",dtr[0][int(currentplayer(chatid,"1","read"))])
                if userid == dtr[0][int(currentplayer(chatid,"1","read"))][0]:
                    datatata = dtr[0][int(currentplayer(chatid,"1","read"))]
                    if diceval == 1:
                        if datatata[2] == "lobby":
                            ppos = 1
                        elif datatata[2] + diceval == 100:
                            print("Player won!")
                            ppos = datatata[2] + diceval
                            context.bot.send_message(chat_id=update.effective_chat.id,text="{player} Won".format(player = firstname))
                        elif datatata[2] + diceval > 100:
                            print("Value greater thatn 1000")
                            ppos = datatata[2]
                        else:
                            ppos = datatata[2] + diceval
                    else:
                        if datatata[2] == "lobby":
                            ppos = "lobby"
                        elif datatata[2] + diceval == 100:
                            print("Player won!")
                            ppos = datatata[2] + diceval
                            context.bot.send_message(chat_id=update.effective_chat.id,text="{player} Won".format(player = firstname))
                        elif datatata[2] + diceval > 100:
                            ppos = datatata[2]
                        else:
                            ppos = datatata[2] + diceval
                    ppos = changeposition(ppos)
                    dtr[0][int(currentplayer(chatid,"1","read"))][2] = ppos
                    editplaystate(dtr[0],str(chatid)+"/playstate.json")
                    print("Current Player Details After",dtr[0][int(currentplayer(chatid,"1","read"))])
                    for i in range(len(getplaystate(str(chatid)+"/playstate.json")[0])):
                        forimage = getplaystate(str(chatid)+"/playstate.json")[0][i]
                        imageloc = os.path.join(currentpath,"snake and ladders/smallicons/"+forimage[3]+"coin.png")
                        position = forimage[2]
                        if position == "lobby":
                            position = 0
                        elif position>100:
                            position = position
                        if i > 0:
                            boardloc = os.path.join(currentpath,"playing/"+str(chatid)+"/sendboard.png")
                        else:
                            boardloc = "board.png"
                        createimage(imageloc,position,boardloc,os.path.join(currentpath,"playing/"+str(chatid)+"/sendboard.png"))
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(os.path.join(currentpath,"playing/"+str(chatid)+"/sendboard.png"), 'rb'))
                    if datatata[2] == 100:
                        print("Player won!")
                        removedata = getplaystate(str(chatid)+"/playstate.json")[0]
                        for i in range(len(getplaystate(str(chatid)+"/playstate.json")[0])):
                            if removedata[i][0] == userid:
                                print("remoing user")
                                removedata.pop(i)
                        editplaystate(removedata,str(chatid)+"/playstate.json")
                    #Writing to Currentplayer.txt
                    if int(currentplayer(chatid,"1","read")) < len(dtr[0]):
                        if int(currentplayer(chatid,"1","read")) ==  len(dtr[0])-1:
                            if diceval == 6 or diceval == 1:
                                valll = int(currentplayer(chatid,"1","read"))
                            else:
                                valll = 0
                        else:
                            if diceval == 6 or diceval == 1:
                                valll = int(currentplayer(chatid,"1","read"))
                            else:
                                valll = int(currentplayer(chatid,"1","read"))+1
                        currentplayer(chatid,str(valll),"write")
                    else:
                        currentplayer(chatid,"0","write")
                    keyboard = [
                    [
                    InlineKeyboardButton("How to roll a die", callback_data="helpdice"),
                    ]
                    ]
                    replykeyboard = [
                        ["🎲"]
                    ]
                    markup = ReplyKeyboardMarkup(replykeyboard, one_time_keyboard=True)
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    replyyy = getplaystate(str(chatid)+"/playstate.json")[0][valll]
                    context.bot.send_message(chat_id=update.effective_chat.id,text="Next Player: {name} ({color})".format(name=replyyy[1],color = replyyy[3]),reply_markup=markup)

            except Exception as e:
                print("Not playing",e)
        if str(chatid) not in playgroups:
            os.mkdir("playing/"+str(chatid))
            kkk = open(os.path.join(currentpath,"playing/"+str(chatid)+"/playstate.json"),"a+")
            kk = open(os.path.join(currentpath,"playing/"+str(chatid)+"/"+str(chatid)+".json"),"a+")
            dataa = [[654646546545,"sample",56,"red"]]
            editplaystate(dataa,str(chatid)+"/playstate.json")
            gamestatejson("false",jsonforchat1)
            print("Created json playstate")
        try:
            ss = update.message.sticker
            i = 0
            l = len(getplaystate(str(chatid)+"/playstate.json")[0])
            sticker = update.message.sticker.file_unique_id
            color = getcolor(sticker)
            if color in getplaystate(str(chatid)+"/playstate.json")[4]:
                context.bot.send_message(chat_id=update.effective_chat.id,text="This color is already choosen")
                kk = 55+"asd"
            if userid in getplaystate(str(chatid)+"/playstate.json")[1]:
                while i < l:
                    if getplaystate(str(chatid)+"/playstate.json")[4][i] == None and getplaystate(str(chatid)+"/playstate.json")[1][i] == userid:
                        datata = getplaystate(str(chatid)+"/playstate.json")[0]
                        if color != None:
                            datata[i][3] = color
                            editplaystate(datata,str(chatid)+"/playstate.json")
                            context.bot.send_message(chat_id=update.effective_chat.id,text="{color} is choosen".format(color=color))
                            break
                    i+=1
            '''else:
                with open(os.path.join(currentpath,"playing/"+jsonforchat1)) as f:
                    data = json.load(f)
                if data["gamestate"] == "true":
                    context.bot.send_message(chat_id=update.effective_chat.id,text="You are not currently Playing")
        '''
        except Exception as e:
            print(e)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('1672404737:AAHEksOQMG9BqVzpJNm4dBsDg4RO7axY6IY')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("newgame", newgame))
    dp.add_handler(CommandHandler("joingame", joingame))
    dp.add_handler(CommandHandler("killgame", killgame))
    dp.add_handler(CommandHandler("startgame", startgame))

    dp.add_handler(CallbackQueryHandler(answercallback))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.all, printupdate))
    inline_caps_handler = InlineQueryHandler(inline_caps)
    dp.add_handler(inline_caps_handler)
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
