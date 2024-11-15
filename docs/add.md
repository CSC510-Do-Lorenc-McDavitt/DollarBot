# About MyDollarBot's /add Feature
This feature enables the user to add a new expense to their expense tracker.
Currently we have the following expense categories set by default:

- Food
- Groceries
- Utilities
- Transport
- Shopping
- Miscellaneous

The user can choose a category and add the amount they have spent to be stored in the expense tracker.
The user can also choose to add their own category and record an expense for that category.
The user has the option to repeat any previously recorded expense (recurring expenses such as rent, utilities, etc.)

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/aditikilledar/dollar_bot_SE23/blob/main/code/add.py)

# Code Description
## Functions

1. run(message, bot):
This is the main function used to implement the add feature. It gives the user the option to repeat a previously recorded expense, or record a new one. It pops up a menu on the bot asking the user to choose their expense category, after which control is given to post_category_selection(message, bot) for further proccessing. It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the main code.py function.

2. post_category_selection(message, bot):
It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the run(message, bot): function in the add.py file. If the user wants to add a new category, passes control to post_append_spend(message,bot): to update the categories. Otherwise, it requests the user to enter the amount they have spent on the expense category chosen and then passes control to post_amount_input(message, bot): for further processing.

3. post_append_spend(message,bot):
This function adds the user defined category to the list of options available to record expenses, and then asks the user to pick the category for which they want to record an expense. The control passes back to post_category_selection(message, bot) once the user has selected the category to add an expense.

4. record_expense(message, bot, previous_expenses):
This function takes **previous expenses** as an argument, which is the list of previously recorded expenses that users can choose to repeat. After the user selects the expense they want to repeat, it calls post_expense_selection(message,bot): to update and store the information.

5. post_expense_selection(message,bot):
This function is called to record the previously recorded expense with the date updated to the current date.  

6. post_amount_input(message, bot):
It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the post_category_selection(message, bot): function in the add.py file. It takes the amount entered by the user, validates it with helper.validate() and then calls add_user_record to store it.

7. add_user_record(chat_id, record_to_be_added):
 Takes 2 arguments - **chat_id** or the chat_id of the user's chat, and **record_to_be_added** which is the expense record to be added to the store. It then stores this expense record in the store.

# How to run this feature?
Once the project is running(please follow the instructions given in the main README.md for this), please type /add into the telegram bot.
