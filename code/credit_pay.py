import helper
from telebot import types

# === Documentation of credit_pay.py ===
account_names = {}
def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the pay credit feature
    """
    chat_id = message.chat.id
    account_names[chat_id] = {}  # Reset the current account for the current user
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    credit_list = helper.read_credit_json()
    if str(chat_id) not in credit_list:
        bot.send_message(chat_id,"You do not have any credit accounts!")
        return
    for c in credit_list[str(chat_id)].keys():
        markup.add(c)
    msg = bot.send_message(chat_id, "Which account do you want to pay for?", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_account_name, bot)


def handle_account_name(message, bot):
    """
    Handles the input of the group name for paying a credit account
    """
    chat_id = message.chat.id
    credit_list = helper.read_credit_json()
    if(not credit_list or len(credit_list) == 0 or str(chat_id) not in credit_list):
        helper.write_credit_json({str(chat_id) : {}})
    credit_list = helper.read_credit_json()
    account_names[chat_id] = str(message.text)
    account_name = account_names[chat_id]
    if(account_name not in credit_list[str(chat_id)].keys()):
        bot.send_message(chat_id, "That account name doesn't exist!")
        return
    bot.send_message(chat_id, "This account currently owes " + str(credit_list[str(chat_id)][account_name]["owe"]))
    msg = bot.send_message(chat_id, "How much do you want to pay for this account?")
    bot.register_next_step_handler(msg, handle_payment, bot)

def handle_payment(message, bot):
    """
    Handles the input of the payment for a credit card bank account. 
    Pays off a certain amount of money for the account.
    """
    chat_id = message.chat.id
    credit_list = helper.read_credit_json()
    if(not credit_list or len(credit_list) == 0 or str(chat_id) not in credit_list):
        helper.write_credit_json({str(chat_id) : {}})
    credit_list = helper.read_credit_json()
    account_name = account_names[chat_id]
    if(account_name not in credit_list[str(chat_id)].keys()):
        bot.send_message(chat_id, "That account doesn't exist!")
        return
    try:
        credit_list[str(chat_id)][account_name]["owe"] = credit_list[str(chat_id)][account_name]["owe"] - int(message.text)
    except Exception:
        bot.send_message(chat_id, "Invalid input, please try again")
        return
    
    helper.write_credit_json(credit_list)
    bot.send_message(chat_id, "You now owe " + str(credit_list[str(chat_id)][account_name]["owe"]))
