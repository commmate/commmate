from ..assistant_function import AssistantFunction
import openai


class GetMinDepthFunction(AssistantFunction):
    def __init__(self):
        super().__init__(
            name="get_min_depth",
            description="Retrieve the minimum depth required to enter a port, channel, anchorage, or marina based on the location name.",
            parameters={
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "The name of the maritime location."
                    }
                },
                "required": ["location_name"]
            }
        )

    def action(self, **kwargs):
        location_name = kwargs.get('location_name')
        if not location_name:
            raise ValueError("location_name is required")

        question = f"What is the minimum depth of the channel to enter by boat to {location_name}?"
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response_text = response.choices[0].text.strip()
        
        try:
            min_depth = float(response_text)
        except ValueError:
            raise ValueError(f"Unable to parse minimum depth from response: {response_text}")

        return {"min_depth": min_depth}