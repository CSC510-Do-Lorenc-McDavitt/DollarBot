import helper

# === Documentation of credit_setup.py ===
account_names = {}


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the setup credit feature.
    """
    chat_id = message.chat.id
    # Reset the current account name for the current user
    account_names[chat_id] = {}
    msg = bot.send_message(
        chat_id, "What's the name of the account you want to add?")
    bot.register_next_step_handler(msg, handle_account_name, bot)


def handle_account_name(message, bot):
    """
    Handles the input of the group name for creating a new group.
    """
    chat_id = message.chat.id
    credit_list = helper.read_credit_json()
    if not credit_list or len(credit_list) == 0:
        helper.write_credit_json({str(chat_id): {}})
    credit_list = helper.read_credit_json()
    if str(chat_id) not in credit_list:
        credit_list[str(chat_id)] = {}
        helper.write_credit_json(credit_list)
    credit_list = helper.read_credit_json()
    account_names[chat_id] = str(message.text)
    account_name = account_names[chat_id]
    if account_name in credit_list[str(chat_id)].keys():
        bot.send_message(chat_id, "That account name is already taken!")
        return
    credit_list[str(chat_id)][account_name] = {"expenses": [],
                                               "owe": 0.0,
                                               "calendar": False}
    helper.write_credit_json(credit_list)
    msg = bot.send_message(
        chat_id, "What's the recurring due date for this account? Enter a number between 1-28")
    bot.register_next_step_handler(msg, handle_due_date, bot)


def handle_due_date(message, bot):
    """
    Handles the input of the due date for a credit card bank account
    """
    chat_id = message.chat.id
    credit_list = helper.read_credit_json()
    if (not credit_list or len(credit_list) == 0 or str(chat_id) not in credit_list):
        helper.write_credit_json({str(chat_id): {}})
    credit_list = helper.read_credit_json()
    account_name = account_names[chat_id]
    if (account_name not in credit_list[str(chat_id)].keys()):
        bot.send_message(chat_id, "That account doesn't exist!")
        return
    try:
        if (int(message.text) < 1 or int(message.text) > 28):
            bot.send_message(chat_id, "Invalid due date, try again!")
            msg = bot.send_message(
                chat_id, "What's the recurring due date for this account? Enter a number between 1-28")
            bot.register_next_step_handler(msg, handle_due_date, bot)
            return
    except Exception:
        bot.send_message(chat_id, "Invalid due date, try again!")
        msg = bot.send_message(
            chat_id, "What's the recurring due date for this account? Enter a number between 1-28")
        bot.register_next_step_handler(msg, handle_due_date, bot)
        return

    credit_list[str(chat_id)][account_name]["due date"] = int(message.text)
    helper.write_credit_json(credit_list)
    bot.send_message(
        chat_id, "Successfully created a credit account with the name " + account_names[chat_id])
