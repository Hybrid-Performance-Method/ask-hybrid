import logging
import ask_sdk_core.utils as ask_utils
import requests
import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to the Hybrid Nutrition virtual assistant! How can I help you stay on track?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class NutritionRequestHandler(AbstractRequestHandler):
    """
    Handler class for nutrition requests.

    Intent:
        "Ask Hybrid"

    Slot values:
        Any sentance following "Ask Hybrid"

    Return values:
        Calories
        nutrition
        alternate response

    Edamam api:
    https://developer.edamam.com/edamam-docs-nutrition-api
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("macros")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # returns slot value
        slot = ask_utils.request_util.get_slot(handler_input, "FoodSentence")
        slot_value = slot.value

        url = 'https://api.edamam.com/api/nutrition-data'

        params = {
            'app_id': 'da0f7443',  # free api access for now. add your own get more mileage
            'app_key': '50dee54b60a3301ca8da3f7d7026e812',
            'ingr': slot_value,
            'nutrition-type': 'logging'
        }

        r = requests.get(url, params=params)
        data = json.loads(r.text)
        ingredient = data['ingredients'][0]['parsed'][0]
        nutrients = ingredient['nutrients']

        if data['calories'] != 0:
            protein = round(nutrients['PROCNT']['quantity'])
            carbs = round(nutrients['CHOCDF']['quantity'])
            fat = round(nutrients['FAT']['quantity'])
            food_quantity = ingredient['quantity']
            measure = ingredient['measure']
            food_name = ingredient['foodMatch']

            if "calories" in slot_value:
                cals = round(nutrients['ENERC_KCAL']['quantity'])
                speak_output = "{} {} {} has about {} calories.".format(
                    food_quantity, measure, food_name, cals)
            else:
                speak_output = "{} {} {} has about {} grams of protein, {} grams of carbohydrates, and {} grams of fat.".format(
                    food_quantity, measure, food_name, protein, carbs, fat)
        else:
            speak_output = "Either you didn't select a valid food, or it has no calories,\
            which means it is not food. Please pick a real food."

        card_title = "Hybrid Nutrition Tracker Assistant"

        return handler_input.response_builder.speak(speak_output).set_card(
            SimpleCard(card_title, speak_output)).set_should_end_session(False).response


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "What's up my baby!? How's the hybrid life treating you?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "If you are having trouble, start your question with \"ask hybrid\" followed by the food you want to track."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .set_should_end_session(False)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "I got you. catch you next time"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I don't think I heard that right. Please ask hybrid again."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .set_should_end_session(False)
            .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(NutritionRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
