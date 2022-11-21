# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa.core.actions.forms import FormAction, REQUESTED_SLOT
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from database_con import DataUpdate, dataQuery, dataGetId


# class ActionName(Action):
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "action_name"
#
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="supply_contact_info")
#         return [SlotSet('name', tracker.latest_message['text'])]

class ActionResponse(Action):
    def name(self):
        return "action_response"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        dataQuery(tracker.get_slot("id"), dispatcher)
        # dispatcher.utter_message(response="utter_response")
        return []


class ActionSubmit(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DataUpdate(tracker.get_slot("name"),
                   tracker.get_slot("email"), dispatcher)
        dataGetId(tracker.get_slot("name"),
                  tracker.get_slot("email"), dispatcher)
        # dispatcher.utter_message("Thanks for the valuable information. ")
        return []


class ActionFormInfo(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "person_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["name", "email"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to - an extracted entity - intent: value pairs - a whole message or a list of them, where a first match will be picked """
        return {
            "name": [self.from_entity(entity="name",
                                      intent="supply_contact_info"), ],
            "email": [self.from_entity(entity="email",
                                       intent="supply_contact_info"), ],
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> List[Dict]:
        """Define what the form has to do after all required slots are filled"""  # utter submit template
        dispatcher.utter_message(response="utter_acknowledge_provided_info",
                                 name=tracker.get_slot("name"),
                                 email=tracker.get_slot("email"))

        return []
