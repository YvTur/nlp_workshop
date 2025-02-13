import random
import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import Response

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Generate a random number
SECRET_NUMBER = random.randint(1, 10)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch"""
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome to the Guess the Number game! Try to guess a number between 1 and 10."
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class GuessNumberIntentHandler(AbstractRequestHandler):
    """Handler for the user's guess"""
    def can_handle(self, handler_input):
        return is_intent_name("GuessNumberIntent")(handler_input)

    def handle(self, handler_input):
        global SECRET_NUMBER
        slots = handler_input.request_envelope.request.intent.slots
        guessed_number = int(slots["number"].value)

        if guessed_number == SECRET_NUMBER:
            speak_output = f"Congratulations! {guessed_number} is correct. You win!"
            SECRET_NUMBER = random.randint(1, 10)  # Reset the game
        elif guessed_number < SECRET_NUMBER:
            speak_output = "Too low! Try again."
        else:
            speak_output = "Too high! Try again."

        return handler_input.response_builder.speak(speak_output).ask("Guess another number.").response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent"""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Try to guess a number between 1 and 10. Say a number to begin!"
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    """Handler for Stop/Cancel Intent"""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.speak("Goodbye!").response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End"""
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GuessNumberIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

lambda_handler = sb.lambda_handler()
