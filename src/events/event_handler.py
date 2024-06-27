from openai import AssistantEventHandler
from typing_extensions import override
import json

class EventHandler(AssistantEventHandler):
    def __init__(self, client, functions):
        self.client = client
        self.functions = functions
        super().__init__()

    @override
    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            arguments_json = tool.function.arguments
            if arguments_json:
                arguments_dict = json.loads(arguments_json)

            function_name = tool.function.name
            function = self.functions.get(function_name)
            if function:
                output = function.action(**arguments_dict)
                tool_outputs.append({"tool_call_id": tool.id, "output": json.dumps(output)})

        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.client, self.functions),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()
