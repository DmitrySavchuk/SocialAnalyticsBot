import telebot
from ToneAnalyzer import ToneAnalyzer
from TwitterCrawler import TwitterCrawler

token = "494262611:AAFsbPdr0BHy-LuIVvkiomx4kigJ-sGOblA"
bot = telebot.TeleBot(token)
update = bot.get_updates()
last_update = update[-1]
last_chat_text = last_update.message.text
last_chat_id = last_update.message.chat.id
last_username = last_update.message.from_user.first_name

tones_list = ['Emotion Tone', 'Writing Tone', 'Social Tone']

hide_markup = telebot.types.ReplyKeyboardRemove()
isRateCommandActive = 0
location = None


def choice_keyboard():
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row("Result description")
    user_markup.row("Continue rating")
    user_markup.row("Continue rating by region")
    user_markup.row("Exit")
    return user_markup


def choice_next():
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row("Emotion tone", "Writing tone", "Social tone")
    user_markup.row("Continue rating", "Continue rating by region")
    return user_markup


def region_keyboard():
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row("USA", "Russia", "United Kingdom", )
    user_markup.row("Italy", "India", "Japan")
    user_markup.row("France", "Australia", "Turkey")
    user_markup.row("Germany", "Canada", "Finland")
    return user_markup


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hello, {}!\nWelcome to the social rating studio!\n "
                                      "Here is the main command to use here:\n"
                                      "/rateit - start assessment\n"
                                      "/rateregion - get assessment in accordance with the specified region".format(message.from_user.first_name),
                     reply_markup=hide_markup)


@bot.message_handler(func=lambda message: message.text == "Exit", content_types='text')
def exit(message):
    bot.send_message(message.chat.id, "Goodbye!", reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "This bot provides the assessment of emotional, writing and social tone of various things or objects.\n\n"
                                      "<b>List of commands with description</b>\n"
                                      "\n/start - begin using this rating bot"
                                      "\n/rateit - start assessment process. Please specify the name of the thing to be assessed as precisely as possible."
                                      "\n/rateregion - works just like the previous one but in accordance with the chosen region"
                                      "\n/help - view the list of commands with description", parse_mode='HTML')


@bot.message_handler(commands=['rateit'])
def handle_rate(message):
    global isRateCommandActive
    isRateCommandActive = 1
    bot.send_message(message.chat.id, "Great!\n"
                                      "In order to start assessment process, please enter the name of the thing "
                                      "you wish to get rating for."
                                      "\nExample: USA election", reply_markup=hide_markup)


@bot.message_handler(commands=['rateregion'])
def rate_region(message):
    user_markup = region_keyboard()
    bot.send_message(message.chat.id, "Choose the region for which You'd like to get the results", reply_markup=user_markup)


@bot.message_handler(func=lambda message: message.text == "Result description", content_types='text')
def result_desc(message):
    user_markup = choice_next()
    bot.send_message(message.chat.id, "Choose which tone would You like me to describe?", reply_markup=user_markup)


@bot.message_handler(func=lambda message: message.text == "Emotion tone", content_types='text')
def result_desc(message):
    user_markup = choice_next()
    bot.send_message(message.chat.id, """<b>Emotion tone</b> indicates emotional state of a person, associated with the things he\she tweets about. As a result You will get the intensity of the five different emotions. (E.g. Joy – 80% means people are largely satisfied with an object chosen).""", parse_mode='HTML', reply_markup=user_markup)


@bot.message_handler(func=lambda message: message.text == "Writing tone", content_types='text')
def result_desc(message):
    user_markup = choice_next()
    bot.send_message(message.chat.id, """<b>Writing tone</b> describes the language style a person uses in his tweets, mainly reflecting his\her assertiveness and objectivity.\n
    <i>An analytical tone</i> shows a person's reasoning and analytical attitude about things (when the percentage of the analytical tone is high, the attitude to the thing You’ve chosen is rational and systematic).\n
    <i>A confident tone</i> indicates a person's degree of certainty.\n
    <i>A tentative tone</i> indicates a person's degree of uncertainty and doubt (when the percentage of the tentative tone is high, the attitude to the thing You’ve chosen is debatable or doubtful).""",  parse_mode='HTML', reply_markup=user_markup)


@bot.message_handler(func=lambda message: message.text == "Social tone", content_types='text')
def result_desc(message):
    user_markup = choice_next()
    bot.send_message(message.chat.id, """<b>Social tone</b> indicates how much the writing expresses the personality attributes of openness, agreeableness and conscientiousness.
                                       """, parse_mode='HTML', reply_markup=user_markup)


@bot.message_handler(func=lambda message: message.text == "Continue rating", content_types='text')
def return_rating(message):
    handle_rate(message)


@bot.message_handler(func=lambda message: message.text == "Continue rating by region", content_types='text')
def return_region_rating(message):
    rate_region(message)


@bot.message_handler(func=lambda message: (message.text == "USA" or
                                           message.text == "Russia" or
                                           message.text == "United Kingdom" or
                                           message.text == "Germany" or
                                           message.text == "Italy" or
                                           message.text == "India" or
                                           message.text == "Canada" or
                                           message.text == "Japan" or
                                           message.text == "France" or
                                           message.text == "Australia" or
                                           message.text == "Turkey" or
                                           message.text == "Finland") and isRateCommandActive != 1)
def return_country(message):
    global location
    location = message.text
    handle_rate(message)


@bot.message_handler(content_types='text')
def rating(message):
    global isRateCommandActive, location
    if isRateCommandActive == 1:
        new_search = TwitterCrawler()
        text = new_search.tweet_search('#' + message.text.strip(), location)
        isRateCommandActive -= 1
        location = None

        if text == '':
            bot.send_message(message.chat.id, 'Sorry, information is not found.', reply_markup=hide_markup)
        else:
            bot.send_message(message.chat.id, "Wait please. The analysis is in process.")
            analyzer = ToneAnalyzer(text)
            analytics = analyzer.analyze_tone()
            analyzer.plotting()

            user_markup = choice_keyboard()

            for tone in tones_list:
                bot.send_photo(chat_id=message.chat.id, photo=open(tone + '.png', 'rb'))
            bot.send_message(message.chat.id, analytics, reply_markup=user_markup)
            bot.send_message(message.chat.id, "For further explanation of the results press 'Result description'\n"
                                              "To continue assessment press 'Continue rating' "
                                              "or 'Continue region rating'.")
    else:
        bot.send_message(message.chat.id, "I can't understand you. If you want to analyze this text, "
                                          "use /rateit or /rateregion")


bot.polling()
