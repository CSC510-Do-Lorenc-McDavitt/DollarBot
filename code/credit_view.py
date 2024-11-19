import helper

# === Documentation of credit_view.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the view credit feature.
    """
    chat_id = message.chat.id

    bot.send_message(chat_id, display_credit(chat_id))

def display_credit(chat_id):
    """
    Handles reading from the credit_record.json file and then sending back a displayable message
    """
    credit_list = helper.read_credit_json()
    if(not credit_list or len(credit_list) == 0 or str(chat_id) not in credit_list):
        return "You currently have no credit records."
    output = ["Showing Accounts and Credit Expenses:",
              "------------------------------------------------------"]
    for account in credit_list[str(chat_id)]:
        output.append(account)
        output.append("  Expenses")
        for x in credit_list[str(chat_id)][account]["expenses"]:
            output.append("    " + x)
        if len(credit_list[str(chat_id)][account]["expenses"]) == 0:
            output.append("    " + "None")
        output.append("  Monthly Due Date: " + str(credit_list[str(chat_id)][account]["due date"]))
        output.append("  Currently Owing: " + str(credit_list[str(chat_id)][account]["owe"]))
        output.append(("  Calendar is currently set up for this event" 
                       if credit_list[str(chat_id)][account]["calendar"] 
                       else "  No calendar currently set up"))
        output.append("------------------------------------------------------")
    return "\n".join(output)