# About MyDollarBot's /display Feature's Graph module
This feature enables the user to see their expense in a graphical format to enable better UX.

Currently, the /display & /analytics commands can display graphs. Use /analytics for better formats.

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/aditikilledar/dollar_bot_SE23/blob/main/code/graphing.py)

# Code Description
## Functions

1. visualize(total_text):
This is the main function used to implement the graphing part of display feature. This file is called from display.py, and takes the user expense as a string and creates a dictionary which in turn is fed as input matplotlib to create the graph

2. addlabels(x, y):
This function is used to add the labels to the graph. It takes the expense values and adds the values inside the bar graph for each expense type

3. viewBudget(data):
This function saves a pie chart with the cateogry-wise budget split

4. overall_split(category_budget):
This function is the updated version of viewBudget

5. spend_wise_split(category_spend):
This function saves a pie chart with the category wise split of expenditure

6. remaining(category_spend_percent):
This function saves a bar graph with the cateogry-wise % of budget remaining

7. time_series(cat_spend_dict):
This function saves a time series graph with history of spending

# How to run this feature?
After you've added sufficient input data, use the /display or /analytics command and you can see the output in a pictorial representation. 
