import helper
from telebot import types

# === Documentation of credit_clear.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the clearing credit feature
    """
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    credit_list = helper.read_credit_json()
    if (not credit_list
        or str(chat_id) not in credit_list
            or len(credit_list[str(chat_id)].keys()) == 0):
        bot.send_message(chat_id, "You do not have any credit accounts!")
        return
    for c in credit_list[str(chat_id)].keys():
        markup.add(c)
    msg = bot.send_message(chat_id,
                           "Which account do you want to clear?",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, handle_account_name, bot)


def handle_account_name(message, bot):
    """
    Handles the input of the group name for clearing a credit account
    """
    chat_id = message.chat.id
    credit_list = helper.read_credit_json()
    if (not credit_list or len(credit_list) == 0 or str(chat_id) not in credit_list):
        helper.write_credit_json({str(chat_id): {}})
    credit_list = helper.read_credit_json()
    account_name = str(message.text)
    if (account_name not in credit_list[str(chat_id)].keys()):
        bot.send_message(chat_id, "That account name doesn't exist!")
        return
    credit_list[str(chat_id)][account_name]["expenses"] = []
    helper.write_credit_json(credit_list)
    bot.send_message(chat_id, "Account expenses cleared!")
