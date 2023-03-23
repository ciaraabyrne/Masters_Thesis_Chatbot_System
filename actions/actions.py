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
#  blah
from database_con import dataGeneralQuestion, DataUpdate, dataQuery, dataGetId, dataGetPrevQ, dataGetNewQ, \
    dataCheckAnswer, dataUpdateOnQuit, FirstTimeQustion, dataShowAnswer


class ActionGeneralQuestion(Action):
    def name(self):
        return "action_general_help"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message.get('text')

        new_q = dataGeneralQuestion(message, tracker.get_slot("level"), dispatcher)
        # dispatcher.utter_message(message)
        return [SlotSet("reply", new_q)]


class ActionCheckAnswer(Action):
    def name(self):
        return "action_checkanswer"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message.get('text')

        new_q, n = dataCheckAnswer(message, tracker.get_slot("exercise_id"), dispatcher, tracker.get_slot("id"),
                                   tracker.get_slot("n_correct_qs"))
        # dispatcher.utter_message(message)
        return [SlotSet("reply", new_q), SlotSet("n_correct_qs", n)]


class ActionNewQuestion(Action):
    def name(self):
        return "action_newquestion"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        x = tracker.latest_message['intent'].get('name')
        # dispatcher.utter_message(f"----------len(NAME) IS {len(x)}----------.")
        # if len(x) < 2:
        #     x = "similar"
        # # dispatcher.utter_message(x)
        # dispatcher.utter_message(f"----------NAME IS {x}----------.")
        new_q, qid, level, n = dataGetNewQ(x, tracker.get_slot("id"), dispatcher, tracker.get_slot("level"),
                                           tracker.get_slot("exercise_id"), tracker.get_slot("n_correct_qs"))
        # dispatcher.utter_message(qid)
        return [SlotSet("new_exercise", new_q), SlotSet("exercise_id", qid), SlotSet("level", level),
                SlotSet("n_correct_qs", n)]


class ActionLastQuestion(Action):
    def name(self):
        return "action_lastquestion"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        x, level, n, na, qid = dataGetPrevQ(tracker.get_slot("id"), dispatcher)
        # dispatcher.utter_message(response="utter_response")
        return [SlotSet("exercise", x), SlotSet("level", level), SlotSet("n_correct_qs", n), SlotSet("name", na),
                SlotSet("exercise_id", qid)]


class ActionResponse(Action):
    def name(self):
        return "action_response"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        name = dataQuery(tracker.get_slot("name"), dispatcher)
        # dispatcher.utter_message(response="utter_response")
        return [SlotSet("name", name), SlotSet("n_correct_qs", 0)]


class ActionShowAnswer(Action):
    def name(self):
        return "action_show_answer"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        dataShowAnswer(dispatcher, tracker.get_slot("exercise_id"))
        # dispatcher.utter_message(response="utter_response")
        return []


class ActionSkipQuestion(Action):
    def name(self):
        return "action_skip_question"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        x = 'similar'
        eid = tracker.get_slot("exercise_id")
        # ex_id = eid + 1
        # dispatcher.utter_message(f"----------len(NAME) IS {len(x)}----------.")
        # if len(x) < 2:
        #     x = "similar"
        # # dispatcher.utter_message(x)
        # dispatcher.utter_message(f"----------NAME IS {x}----------.")
        new_q, qid, level, n = dataGetNewQ(x, tracker.get_slot("id"), dispatcher, tracker.get_slot("level"), eid
                                           , tracker.get_slot("n_correct_qs"))
        # dispatcher.utter_message(qid)
        return [SlotSet("new_exercise", new_q), SlotSet("exercise_id", qid), SlotSet("level", level),
                SlotSet("n_correct_qs", n)]


class ActionSubmit(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DataUpdate(tracker.get_slot("name"),
                   tracker.get_slot("email"), dispatcher)
        x = dataGetId(tracker.get_slot("name"),
                      tracker.get_slot("email"), dispatcher)
        question, q_id, ex = FirstTimeQustion(dispatcher)

        # dispatcher.utter_message("Thanks for the valuable information. ")
        return [SlotSet("id", x), SlotSet("new_exercise", question), SlotSet("exercise_id", q_id),
                SlotSet("n_correct_qs", 0),SlotSet("level", 1), SlotSet("exercise", ex)]



class ActionQuit(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_quit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message("here")
        dataUpdateOnQuit(tracker.get_slot("id"), tracker.get_slot("level"), dispatcher, tracker.get_slot("name"),tracker.get_slot("n_correct_qs"))
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
