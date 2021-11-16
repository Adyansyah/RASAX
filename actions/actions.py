# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import sqlite3
from pathlib import Path
from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCheckKnowledge(Action):
    knowledge = Path("data/areas.txt").read_text().split("\n")

    def name(self) -> Text:
        return "action_check_areas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        for x in tracker.latest_message['entities']:
            print(tracker.latest_message)
            if x['entity'] == 'materi':
                materi = x['value'].lower()
                if materi in self.knowledge:
                    dispatcher.utter_message(
                        text=f"Ya, kamu bisa bertanya mengenai {materi}.")
                else:
                    dispatcher.utter_message(
                        text=f"Maaf saya tidak tahu mengenai {materi}, coba cek lagi pengejaan yang benar.")
        return []


class ActionStoringFeedback(Action):

    def name(self) -> Text:
        return "action_storing_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        feed = tracker.latest_message.get("text")
        name = tracker.get_slot("name")

        # connect to sqlite
        connection = sqlite3.connect('rasa_database.db')
        cursor = connection.cursor()

        # create table if not exist
        #table = """CREATE TABLE IF NOT EXISTS feedbacks(id_feed INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, feed TEXT)"""
        # cursor.execute(table)

        # insert
        data = "INSERT INTO feedbacks VALUES ( NULL, '{0}','{1}')".format(
            name, feed)

        cursor.execute(data)
        connection.commit()
        connection.close()

        dispatcher.utter_message(text="Terima kasih atas Feedbacknya")
        return []


class ActionSaveName(Action):
    def name(self) -> Text:
        return "action_savename"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entity = tracker.latest_message['entities']
        value = ""
        for x in entity:
            print(tracker.latest_message)
            if x['entity'] == 'name':
                value = x['value']
                dispatcher.utter_message(
                    text=f"hi {value}, ada yang bisa saya bantu.")
        return [SlotSet("name", value)]
