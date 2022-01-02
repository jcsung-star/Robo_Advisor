### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }

def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response

"""
Step 3: Enhance the Robo Advisor with an Amazon Lambda Function

In this section, you will create an Amazon Lambda function that will validate the data provided by the user on the Robo Advisor.

1. Start by creating a new Lambda function from scratch and name it `recommendPortfolio`. Select Python 3.7 as runtime.

2. In the Lambda function code editor, continue by deleting the AWS generated default lines of code, then paste in the starter code provided in `lambda_function.py`.

3. Complete the `recommend_portfolio()` function by adding these validation rules:

    * The `age` should be greater than zero and less than 65.
    * The `investment_amount` should be equal to or greater than 5000.

4. Once the intent is fulfilled, the bot should respond with an investment recommendation based on the selected risk level as follows:

    * **none:** "100% bonds (AGG), 0% equities (SPY)"
    * **low:** "60% bonds (AGG), 40% equities (SPY)"
    * **medium:** "40% bonds (AGG), 60% equities (SPY)"
    * **high:** "20% bonds (AGG), 80% equities (SPY)"

> **Hint:** Be creative while coding your solution, you can have all the code on the `recommend_portfolio()` function, or you can split the functionality across different functions, put your Python coding skills in action!

5. Once you finish coding your Lambda function, test it using the sample test events provided for this Challenge.

6. After successfully testing your code, open the Amazon Lex Console and navigate to the `recommendPortfolio` bot configuration, integrate your new Lambda function by selecting it in the “Lambda initialization and validation” and “Fulfillment” sections.

7. Build your bot, and test it with valid and invalid data for the slots.

"""

# Complete the `recommend_portfolio()` function by adding these validation rules:
"""
"The `age` should be greater than zero and less than 65."
"The `investment_amount` should be equal to or greater than 5000."
"""            
def validate_data(first_name, age, investment_amount, risk_level, intent_request):
    """
    validates the data provided by the user.
    """
    if first_name is not None:
        if not first_name.isalpha():
            return build_validation_result(
            False,
            "firstName", 
            "Please type your first name again."
            )
        
    # Validate that the user is older than 0 and younger than 65 years old
    if age is not None:
        age = parse_int(age)
        if age <=0 or age >= 65:
            return build_validation_result(
                False, 
                "age",
                "Please enter an age greater than 0 and less than 65 to use our services."
            )
    
    # Validate the investment amount, it should be >= $5000
    if investment_amount is not None:
        investment_amount = int(investment_amount)
        if investment_amount < 5000: 
            return build_validation_result(
                False,
                "investmentAmount",
                "The amount you entered did not qualify for our services. Please enter an amount greater than or equal to $5000."
            )
    # Validade the risk level, it should be None, Low, Medium or High]        
    if risk_level is not None:
        if not risk_level.lower() in ['none', 'low', 'medium', 'high']:
            return build_validation_result(
                False,
                "riskLevel",
                "The risk_level should be None, Low, Medium or High (all are not case sensitive)."
            )
    return build_validation_result(True, None, None)

# Once the intent is fulfilled, the bot should respond with an investment recommendation based on the selected risk level as follows:       
def get_recommend_portfolio(risk_level):
    """
    Returns the investment percentages, based on risk_level:
        * **none:** "100% bonds (AGG), 0% equities (SPY)"
        * **low:** "60% bonds (AGG), 40% equities (SPY)"
        * **medium:** "40% bonds (AGG), 60% equities (SPY)"
        * **high:** "20% bonds (AGG), 80% equities (SPY)"
    """
    # Choose risk levels from None, Low, Medium or High (all are not case insensitive) from the user.
    recommend_portfolio = ""
    if risk_level == "None" or "none":
        recommend_portfolio = "100% bonds (AGG), 0% equities (SPY)"
    elif risk_level == "Low" or "low":
        recommend_portfolio = "60% bonds (AGG), 40% equities (SPY)"
    elif risk_level == "Medium" or "medium":
        recommend_portfolio = "40% bonds (AGG), 60% equities (SPY)"
    elif risk_level == "High" or "high":
        recommend_portfolio = "20% bonds (AGG), 80% equities (SPY)"
        
    return recommend_portfolio

### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]


    
    # Gets the invocation source, for lex dialogs "DialogCodeHook" is expected   
    source = intent_request["invocationSource"]
    
    if source == "DialogCodeHook":
        # Gets all the slots
        slots = get_slots(intent_request)
        
        # Validates user's inputs using the validate_data function
        validation_result = validate_data(first_name, age, investment_amount, risk_level, intent_request)
   
        # If the data provided by the user is not valid
        # the elicitSlot dialog action is used to re_promot for the first violation detected.    
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None
            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )  
        
        # Fetch current sessions attributes
        output_session_attributes = intent_request["sessionAttributes"] 
    
        # Once all slots are valid, a delegate dialog is returned to lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))
        
    # Get the asset allocation model to recommended
    allocation_recommendation = get_recommend_portfolio(risk_level)
    
    # Return a message with conversation's results    
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you, {}, for completing our survey. Based on your the risk tollerance, we recommend the following investment allocation of {}. Thank you for giving us the opportunity to serve your retirement needs.
            """.format(
                first_name, allocation_recommendation
            ),
        }
    )

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "recommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)