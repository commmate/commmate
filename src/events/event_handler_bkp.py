import os
import requests
from openai import AssistantEventHandler
from typing_extensions import override
import json
import googlemaps
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    organization=os.getenv('OPENAI_ORGANIZATION_ID'),
    project=os.getenv('OPENAI_PROJECT_ID')
)

# Load API keys from environment variables
STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Define the functions
def get_coordinates(location_name):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    
    geocode_result = gmaps.geocode(location_name)

    if not geocode_result:
        raise ValueError(f"No results found for location: {location_name}")
    
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return {"lat": lat, "lng": lng}

def get_tide_data(lat, lng, start_time, end_time):
    response = requests.get(
        'https://api.stormglass.io/v2/tide/extremes/point',
        params={
            'lat': lat,
            'lng': lng,
            'start': start_time,
            'end': end_time
        },
        headers={'Authorization': STORMGLASS_API_KEY}
    )
    return response.json()

def is_safe_to_navigate(draft, min_depth, tide_height):
    return {"result": (min_depth + tide_height) > draft}

def get_min_depth(location_name):
    question = f"What is the minimum depth of the channel or ancorage space to enter by boat to {location_name}?"

    stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

    response = OpenAI.Completion.create(
        engine="davinci-codex",
        prompt=question,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print(response)

    response_text = response.choices[0].text.strip()
    
    try:
        min_depth = float(response_text)
    except ValueError:
        raise ValueError(f"Unable to parse minimum depth from response: {response_text}")

    return {"min_depth": min_depth}

class EventHandler(AssistantEventHandler):
    def __init__(self, client):
        self.client = client
        super().__init__()

    @override
    def on_event(self, event):
        # Retrieve events that are denoted with 'requires_action'
        # since these will have our tool_calls
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            # Extract the JSON string from the arguments attribute
            arguments_json = tool.function.arguments

            # Parse the JSON string to a dictionary
            if arguments_json:
                arguments_dict = json.loads(arguments_json)

            if tool.function.name == "get_coordinates":
                location_name = arguments_dict.get('location_name')
                output = get_coordinates(location_name)
                tool_outputs.append({"tool_call_id": tool.id, "output": json.dumps(output)})  # Convert output to JSON string
            elif tool.function.name == "get_tide_data":
                lat = arguments_dict.get('lat')
                lng = arguments_dict.get('lng')
                start_time = arguments_dict.get('start_time')
                end_time = arguments_dict.get('end_time')
                output = get_tide_data(lat, lng, start_time, end_time)
                tool_outputs.append({"tool_call_id": tool.id, "output": json.dumps(output)})  # Convert output to JSON string
            elif tool.function.name == "is_safe_to_navigate":
                draft = arguments_dict.get('draft')
                min_depth = arguments_dict.get('min_depth')
                tide_height = arguments_dict.get('tide_height')
                output = is_safe_to_navigate(draft, min_depth, tide_height)
                tool_outputs.append({"tool_call_id": tool.id, "output": json.dumps(output)})  # Convert output to JSON string
            elif tool.function.name == "get_min_depth":
                location_name = arguments_dict.get('location_name')
                output = get_min_depth(location_name)
                tool_outputs.append({"tool_call_id": tool.id, "output": json.dumps(output)})  # Convert output to JSON string

        # Submit all tool_outputs at the same time
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use the submit_tool_outputs_stream helper
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.client),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()
