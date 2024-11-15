# About MyDollarBot's /edit Feature
This feature enables the user to edit a previously entered expense in the app. The use can change the amount set in the bot with this command. 

Please note that this is still a Work In Progress.

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/aditikilledar/dollar_bot_SE23/blob/main/code/edit.py)

# Code Description
## Functions

1. run(message, bot):
This is the main function used to implement the delete feature. It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the main code.py function. It gets the details for the expense to be edited from here and passes control onto edit2(m, bot): for further processing.

2. select_category_to_be_updated(m, bot):
It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the  run(message, bot): function in the same file. It provides the user with the list of categories that they can update in the expense such as date, amount, category. Once the user selects the field that they want to update, control passes to enter_updated_data(m, bot, selected_data, updated): for further processing.

3. enter_updated_data(m, bot, selected_data, updated):
It takes 4 arguments for processing - **message** which is the message from the user, **bot** which is the telegram bot object from the select_category_to_be_updated(m, bot): function in the same file, **selected_data**, which is the expense that is being updated, and **updated**, which keeps track of the categories that have been updated so far. Based on the category chosen for editing by the user, it redirects to the corresponding function for further processing.

4. edit_date(bot, selected_data, result, c, updated):
It takes 5 arguments for processing - **bot** which is the telegram bot object from the enter_updated_data(m, bot,selected_data,updated): function in the same file, **selected_data**, which is the expense that is being updated, **result**, which is the user selected date from the interactive calendar, **c**, the calendar object callback function which has the data about the chat(simulates message), and **updated**, which keeps track of the categories that have been updated so far. It takes care of date change and edits.

5. edit_cost(m, bot, selected_data, updated):
It takes 4 arguments for processing - **message** which is the message from the user, **bot** which is the telegram bot object from the  enter_updated_data(m, bot,selected_data,updated):unction in the same file, **selected_data**, which is the expense that is being updated, and **updated**, which keeps track of the categories that have been updated so far. It takes care of cost change and edits.

6. edit_cat(m, bot, selected_data, updated):
It takes 4 arguments for processing - **message** which is the message from the user, **bot** which is the telegram bot object from the enter_updated_data(m, bot,selected_data,updated): function in the same file, **selected_data**, which is the expense that is being updated, and **updated**, which keeps track of the categories that have been updated so far. It takes care of category change and edits.

7. update_different_category(m, bot, selected_data, updated):
It takes 4 arguments for processing - **message** which is the message from the user, **bot** which is the telegram bot object from the enter_updated_data(m, bot,selected_data,updated): function in the same file, **selected_data**, which is the expense that is being updated, and **updated**, which keeps track of the categories that have been updated so far. It allows the user to select from the categories that have not previously been edited and passes the control to enter_updated_data(m, bot, selected_data, updated) for further processing.

# How to run this feature?
type /edit, then follow the instructions on the chat to continue 