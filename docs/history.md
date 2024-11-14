# About MyDollarBot's /history Feature
This feature enables the user to view all of their stored records i.e it gives a historical view of all the expenses stored in MyDollarBot.

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/aditikilledar/dollar_bot_SE23/blob/main/code/history.py)

# Code Description
## Functions

1. run(message, bot):
This is the main function used to implement the delete feature. It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the main code.py function. It calls helper.py to get the user's historical data and based on whether there is data available, it either prints an error message or displays the user's historical data.

# How to run this feature?
Once the project is running(please follow the instructions given in the main README.md for this), please type /history into the telegram bot.
