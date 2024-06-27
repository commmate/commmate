import os
from openai import OpenAI
from Personal.imediatonautica.src.event.event_handler import EventHandler

# Initialize the OpenAI client
client = OpenAI(
    organization=os.getenv('OPENAI_ORGANIZATION_ID'),
    project=os.getenv('OPENAI_PROJECT_ID')
)

# Define the functions metadata for the assistant
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_coordinates",
            "description": "Retrieve the latitude and longitude for a given maritime location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "The name of the maritime location."
                    }
                },
                "required": ["location_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tide_data",
            "description": "Get tide data for the specified coordinates and time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number", "description": "Latitude of the location."},
                    "lng": {"type": "number", "description": "Longitude of the location."},
                    "start_time": {"type": "string", "description": "Start time for the tide data in ISO 8601 format."},
                    "end_time": {"type": "string", "description": "End time for the tide data in ISO 8601 format."}
                },
                "required": ["lat", "lng", "start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "is_safe_to_navigate",
            "description": "Check if it's safe to navigate based on boat draft, minimum depth, and tide height.",
            "parameters": {
                "type": "object",
                "properties": {
                    "draft": {"type": "number", "description": "The draft of the boat."},
                    "min_depth": {"type": "number", "description": "The minimum depth of the channel, port, marina, or anchorage."},
                    "tide_height": {"type": "number", "description": "The tide height at the expected time."}
                },
                "required": ["draft", "min_depth", "tide_height"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_min_depth",
            "description": "Retrieve the minimum depth required to enter a port, channel, anchorage, or marina based on the location name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "The name of the maritime location."
                    }
                },
                "required": ["location_name"]
            }
        }
    }
]

# Create the assistant
assistant = client.beta.assistants.create(
    instructions="You are a maritime navigation assistant. You help users determine the safety of navigating ports, channels, anchorages, and marinas based on tide levels and boat draft.",
    model="gpt-4o",
    tools=tools
)

# Create a new thread
thread = client.beta.threads.create()

# User asks a question
user_message = "Is it safe for a boat with a draft of 1.6m to enter Cork Marina at 12h tomorrow?"

# Add user message to the thread
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content=user_message,
)

# Stream the thread's run
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler(client)
) as stream:
    stream.until_done()
