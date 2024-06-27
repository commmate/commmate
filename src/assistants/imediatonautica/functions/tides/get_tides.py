from ..assistant_function import AssistantFunction
import requests


class GetTidesFunction(AssistantFunction):
    def __init__(self):
        super().__init__(
            name="get_tide_data",
            description="Get tide data for the specified coordinates and time.",
            parameters={
                "type": "object",
                "properties": {
                    "lat": {"type": "number", "description": "Latitude of the location."},
                    "lng": {"type": "number", "description": "Longitude of the location."},
                    "start_time": {"type": "string", "description": "Start time for the tide data in ISO 8601 format."},
                    "end_time": {"type": "string", "description": "End time for the tide data in ISO 8601 format."}
                },
                "required": ["lat", "lng", "start_time", "end_time"]
            }
        )

    def action(self, **kwargs):
        lat = kwargs.get('lat')
        lng = kwargs.get('lng')
        start_time = kwargs.get('start_time')
        end_time = kwargs.get('end_time')

        if not lat or not lng or not start_time or not end_time:
            raise ValueError("lat, lng, start_time, and end_time are required")

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