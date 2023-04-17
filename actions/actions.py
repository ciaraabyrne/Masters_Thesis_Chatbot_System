from typing import Any, Text, Dict, List, Union

from rasa.core.actions.forms import FormAction, REQUESTED_SLOT
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from database_con import dataGeneralQuestion, DataUpdate, dataQuery, dataGetId, dataGetPrevQ, dataGetNewQ, \
    dataCheckAnswer, dataUpdateOnQuit, FirstTimeQustion, dataShowAnswer


# deal with a users general questions
class ActionGeneralQuestion(Action):
    def name(self):
        return "action_general_help"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message.get('text')  # get most recent user message
        new_q = dataGeneralQuestion(message, tracker.get_slot("level"), dispatcher)  # database function
        return [SlotSet("reply", new_q)]  # fill slots


# correct users answer
class ActionCheckAnswer(Action):
    def name(self):
        return "action_checkanswer"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message.get('text')  # get most recent user message
        new_q, n = dataCheckAnswer(message, tracker.get_slot("exercise_id"), dispatcher, tracker.get_slot("id"),
                                   tracker.get_slot("n_correct_qs"))  # database function
        return [SlotSet("reply", new_q), SlotSet("n_correct_qs", n)]


# get a new question
class ActionNewQuestion(Action):
    def name(self):
        return "action_newquestion"

    def run(self, dispatcher, tracker, domain):
        x = tracker.latest_message['intent'].get('name')  # get latest intent name
        new_q, qid, level, n = dataGetNewQ(x, tracker.get_slot("id"), dispatcher, tracker.get_slot("level"),
                                           tracker.get_slot("exercise_id"), tracker.get_slot("n_correct_qs"))
        return [SlotSet("new_exercise", new_q), SlotSet("exercise_id", qid), SlotSet("level", level),
                SlotSet("n_correct_qs", n)]


# previous session information
class ActionLastQuestion(Action):
    def name(self):
        return "action_lastquestion"

    def run(self, dispatcher, tracker, domain):
        x, level, n, na, qid = dataGetPrevQ(tracker.get_slot("id"), dispatcher)
        return [SlotSet("exercise", x), SlotSet("level", level), SlotSet("n_correct_qs", n), SlotSet("name", na),
                SlotSet("exercise_id", qid)]


# unused
class ActionResponse(Action):
    def name(self):
        return "action_response"

    def run(self, dispatcher, tracker, domain):
        name = dataQuery(tracker.get_slot("name"), dispatcher)
        return [SlotSet("name", name), SlotSet("n_correct_qs", 0)]


# show the user the answer to a question
class ActionShowAnswer(Action):
    def name(self):
        return "action_show_answer"

    def run(self, dispatcher, tracker, domain):
        dataShowAnswer(dispatcher, tracker.get_slot("exercise_id"))
        return []


# skip a question
class ActionSkipQuestion(Action):
    def name(self):
        return "action_skip_question"  # Be careful, did you mean action_fetch_data?

    def run(self, dispatcher, tracker, domain):
        x = 'similar'
        eid = tracker.get_slot("exercise_id")
        new_q, qid, level, n = dataGetNewQ(x, tracker.get_slot("id"), dispatcher, tracker.get_slot("level"), eid
                                           , tracker.get_slot("n_correct_qs"))
        return [SlotSet("new_exercise", new_q), SlotSet("exercise_id", qid), SlotSet("level", level),
                SlotSet("n_correct_qs", n)]


# enter new user into database
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

        return [SlotSet("id", x), SlotSet("new_exercise", question), SlotSet("exercise_id", q_id),
                SlotSet("n_correct_qs", 0), SlotSet("level", 1), SlotSet("exercise", ex)]


# quit session, update database, give lesson summary
class ActionQuit(Action):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "action_quit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dataUpdateOnQuit(tracker.get_slot("id"), tracker.get_slot("level"), dispatcher, tracker.get_slot("name")
                         , tracker.get_slot("n_correct_qs"))
        return []

# new user information
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
