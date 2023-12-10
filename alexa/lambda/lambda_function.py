# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import requests
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

base_url = "https://groupfit-server.fly.dev/"


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
        
        device_id = handler_input.request_envelope.context.system.device.device_id
        device_id = "1"
        query_url = base_url + "get-plan-for-today?alexa_id="+device_id
        
        speak_output = """<amazon:emotion name="excited" intensity="high">Welcome to Group Fit.</amazon:emotion> I'm excited to be your workout partner today. """
        
        try:
            print(query_url)
            response = requests.get(query_url)
            print(response)
            
            if response.status_code == 200:
                print(response.content)
                
                # Assumption plan is a string
                plan :str = str(response.content, 'UTF-8')
                # data = json.loads(response.content)[5]
                print(plan)
                logger.info("Data Received: "+ plan)
                speak_output += " Your planned workout for today is "+ plan
                session_attr['workoutSessionPlan'] = plan
                
                return (
                    handler_input.response_builder
                        .speak("<speak>"+speak_output+"</speak>")
                        # .ask(speak_output)
                        .response
                )
            else:
                speak_output += "There was an error in fetching your plan."
                
        except:
            session_attr['workoutSessionPlan'] = None
            speak_output += "There was an error in fetching your plan."
            
            # speak_output = "Welcome to Group Fit. Let's start "
        
        reprompt = "Please come back again by saying open Group Workout "
        return (
            handler_input.response_builder
                .speak("<speak>"+speak_output+"</speak>")
                .ask(reprompt)
                .response
        )

# class HelloWorldIntentHandler(AbstractRequestHandler):
#     """Handler for Hello World Intent."""
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         speak_output = "Hello World!"

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 # .ask("add a reprompt if you want to keep the session open for the user to respond")
#                 .response
#         )

class StartWorkoutIntentHandler(AbstractRequestHandler):
    """Handler for Start Workout Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StartWorkoutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        user_id = ask_utils.get_user_id(handler_input)
        device_id = handler_input.request_envelope.context.system.device.device_id
        
        session_attr = handler_input.attributes_manager.session_attributes
        
        # Try to get session state - if workout started on watch just send whatever speak_output
        # If workout is started, speak_output becomes "Please start on watch and say yes again"

        speak_output = "Let's go! Your workout seems to be in session. "

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class NextWorkoutIntentHandler(AbstractRequestHandler):
    """Handler for Start Workout Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NextWorkoutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        user_id = ask_utils.get_user_id(handler_input)
        device_id = handler_input.request_envelope.context.system.device.device_id
        
        session_attr = handler_input.attributes_manager.session_attributes
        
        # speak_output = """<speak><amazon:effect name="whispered">Welcome.</amazon:effect>. Normal Voice</speak>"""
        speak_output = " Device id is "+str(device_id)
        speak_output += " user id is "+str(user_id)
        # speak_output "Here is your next workout"
        
        # Check if session has been started
        # if yes - GET next workout
        # else say - speech("you don't have any workout in process. Please start from watch and say begin workout") -- as reprompt
                
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
        
    
class ShowWorkoutStatusIntentHandler(AbstractRequestHandler):
    """Handler for Start Workout Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ShowWorkoutStatusIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Contains slot - FriendName
        
        # For individual user
        # GET workout status, show info in speak_output; change voice <amazon:emotion name='excited'>
        # If workout is over show summary
        # If workout in progress show current state
        
        # For friend, get same info for friend
        # Show speak output with that information
        # Same as above
        
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        
        device_id = handler_input.request_envelope.context.system.device.device_id
        device_id = "1"
        
        query_url = base_url + "get-workout-live-metrics?alexa_id="+device_id
        
        slots = handler_input.request_envelope.request.intent.slots
        name = slots['FriendName']
        if name.value:
            print("Found friend detail", type(name), name.value)
            # take me down to the paradise city
            query_url += "&participant_name="+str(name.value)
        else:
            print("Not found friend detail")
            # this city was not built on rock'n'roll
        
        try:
            print(query_url)
            response = requests.get(query_url)
            print("Received Response: ", response)
            
            if response.status_code == 200:
                print(response.content)
                
                # Assumption plan is a string
                status :str = str(response.content, 'UTF-8')
                # data = json.loads(response.content)[5]
                print(status)
                logger.info("Data Received: "+ status)
                speak_output = "Here's a quick update on your status.   "+ status
                session_attr['workoutSessionState'] = status
                
                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        # .ask(speak_output)
                        .response
                )
        except:
            session_attr['workoutSessionPlan'] = None
            
        speak_output = "There was an error in fetching your info."
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(reprompt)
                .response
        )

class ShowWorkoutSummaryIntentHandler(AbstractRequestHandler):
    """Handler for Start Workout Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ShowWorkoutSummaryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Contains slot - FriendName
        
        # For individual user
        # GET workout status, show info in speak_output; change voice <amazon:emotion name='excited'>
        # If workout is over show summary
        # If workout in progress show current state
        
        # For friend, get same info for friend
        # Show speak output with that information
        # Same as above
        
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        
        device_id = handler_input.request_envelope.context.system.device.device_id
        device_id = "1"
        
        query_url = base_url + "get-workout-summary?alexa_id="+device_id
        
        slots = handler_input.request_envelope.request.intent.slots
        name = slots['FriendName']
        if name.value:
            print("Found friend detail", type(name), name.value)
            # take me down to the paradise city
            query_url += "&participant_name="+str(name.value)
        else:
            print("Not found friend detail")
            # this city was not built on rock'n'roll
        
        try:
            print(query_url)
            response = requests.get(query_url)
            print("Received Response: ", response)
            
            if response.status_code == 200:
                print(response.content)
                
                # Assumption plan is a string
                status :str = str(response.content, 'UTF-8')
                # data = json.loads(response.content)[5]
                print(status)
                logger.info("Data Received: "+ status)
                speak_output = "Here's a summary of the workout.   "+ status
                session_attr['workoutSessionState'] = status
                
                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        # .ask(speak_output)
                        .response
                )
        except:
            session_attr['workoutSessionPlan'] = None
            
        speak_output = "There was an error in fetching your info."
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(reprompt)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "What can I help you with?"
        # You can say hello to me! How can I help?

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
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
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "speech speech"
        # "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

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

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(StartWorkoutIntentHandler())
sb.add_request_handler(NextWorkoutIntentHandler())
sb.add_request_handler(ShowWorkoutStatusIntentHandler())
sb.add_request_handler(ShowWorkoutSummaryIntentHandler())

# sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
