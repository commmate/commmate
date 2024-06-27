from abc import ABC, abstractmethod

class AssistantFunction(ABC):
    def __init__(self, name, description, parameters):
        self.name = name
        self.description = description
        self.parameters = parameters

    def get_tool_definition(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    @abstractmethod
    def action(self, **kwargs):
        pass
