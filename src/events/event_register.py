# event_register.py
from event_handler import EventHandler

class EventRegister:
    def __init__(self, client):
        self.events = {}
        self.openai_client = client

    def register_event(self, event_function):
        self.events[event_function.name] = event_function

    def get_registered_events(self):
        return self.events

    def build_registration_tools(self):
        tools = []
        for event_function in self.events.values():
            tools.append(event_function.get_json_definition())
        return tools

    def build_event_handler(self):
        return EventHandler(self.openai_client, self.get_registered_events())
