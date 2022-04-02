from ast import Pass
import telebot
from top_secret import TOKEN, QUESTION_GROUP_ID, ANSWERS_CHANNEL_ID
from default_messages import START, HELP, NO_QUESTION

bot = telebot.TeleBot(TOKEN, "HTML")

@bot.message_handler(commands=["start"])
def start_message(message: telebot.types.Message) -> None:
    chat_id = message.chat.id
    bot.send_message(chat_id, START)

@bot.message_handler(commands=["help"])
def start_message(message: telebot.types.Message) -> None:
    chat_id = message.chat.id
    bot.send_message(chat_id, HELP)

@bot.message_handler(commands=["pregunta", "preguntar"])
def forward_question(message: telebot.types.Message) -> None:
    if len(telebot.util.extract_arguments(message.text)) < 1:
        bot.reply_to(message, "Hola! \nSi tienes una pregunta para el CaDCC envía un mensaje con el comando /pregunta@cadccbot seguido de tu pregunta")
    else:
        question = telebot.util.extract_arguments(message.html_text)
        chat_id = message.chat.id
        message_id = message.id
        username = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>"

        text = f"Nueva Pregunta Recibida\n\nID chat: {chat_id}\nID mensaje: {message_id}\nUser: {username}\n\n###PREGUNTA###\n{question}"
        
        bot.send_message(QUESTION_GROUP_ID, text)
        # bot.forward_message(QUESTION_GROUP_ID, message.chat.id, message.id)

@bot.message_handler(commands=["respuesta", "responder"])
def answer_question(message: telebot.types.Message) -> None:
    if message.chat.id != QUESTION_GROUP_ID or message.reply_to_message == None or \
        len(telebot.util.extract_arguments(message.text)) < 1:
        return
    
    if not message.reply_to_message.text.startswith("Nueva Pregunta Recibida"):
        bot.reply_to(message, NO_QUESTION)
        return

    info = message.reply_to_message.text.split("\n")

    chat_id = info[2][9:]
    message_id = info[3][12:]

    question = message.reply_to_message.html_text.split("\n###PREGUNTA###\n")[1]
    answer = telebot.util.extract_arguments(message.html_text)

    text = f"Pregunta:\n{question}\nRespuesta:\n{answer}"

    bot.send_message(chat_id, text, reply_to_message_id= message_id)
    # bot.send_message(ANSWERS_CHANNEL_ID, text)
    
# @bot.message_handler(commands=["debug"])
# def debug_message(message: telebot.types.Message) -> None:
#     bot.send_message(message.chat.id, f"Chat ID: {message.chat.id}")

bot.infinity_polling()