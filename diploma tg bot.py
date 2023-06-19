import telebot as tb
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer


def summarize(text, num_sentences=2):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
  
    summary = summarizer(parser.document, num_sentences)
    summary_text = ""
    for sentence in summary:
        summary_text += str(sentence) + " "
    return summary_text

token = '6129286982:AAFjl5uQuVw9av8sKqLLmYv2-Z2Vl7uTFGw'
bot = tb.TeleBot(token)
message_text = []
number = None


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Здравствуйте. Данный бот создан с целью генерации заголовков к англоязычным '
                                      'текстам. Чтобы им воспользоваться просто введите текст, а бот выдаст вам '
                                      'сгенерированный к нему заголовок. Начинайте пожалуйста ваше '
                                      'сообщение со слова START и заканчивайте его словом END. Это необходимо для '
                                      'обхода ограничения Telegram на максимальную длину сообщения - 4096. Если ваше '
                                      'сообщение короче, чем 4096 символов, то просто добавьте START в его начало и '
                                      'следующим сообщением отправьте END. Вы можете ввести предпочтительное число '
                                      'предложений для вывода отдельным сообщением. Учтите, что его следует вводить '
                                      'до текста, который вы хотите сжать.')


@bot.message_handler(func=lambda message: message.text.startswith('START'))
def handle_start(message):
    global message_text
    message_text = [message.text]


@bot.message_handler(func=lambda message: message.text.endswith('END'))
def handle_end(message):
    global message_text
    global number
    if message_text:
        message_text.append(message.text)
        combined_message = ' '.join(message_text)
        if number:
            bot.send_message(message.chat.id, f'Автоматически сгенерированное краткое содержание вашего текста:\n{summarize(combined_message, number)}')
            message_text = []
            number = None
        else:
            bot.send_message(message.chat.id, f'Автоматически сгенерированное краткое содержание вашего текста:\n{summarize(combined_message)}')
            message_text = []
    else:
        bot.send_message(message.chat.id, 'Ошибка. Не обнаружено стартового слова START перед сообщением, содержащим '
                                          'слово END.')


@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_number(message):
    global number
    if int(message.text) > 7:
        number = 7
    elif int(message.text) < 1:
        number = 1
    else:
        number = int(message.text)


@bot.message_handler(func=lambda message: not message.text.startswith('START') and not message.text.endswith(
    'END') and not message.text.isdigit())
def handle_all_messages(message):
    global message_text
    if message_text:
        message_text.append(message.text)


bot.infinity_polling()
