from ..assistant_function import AssistantFunction
import googlemaps

class GetCoordinatesFunction(AssistantFunction):
    def __init__(self):
        super().__init__(
            name="get_coordinates",
            description="Retrieve the latitude and longitude for a given maritime location.",
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
        
        gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        geocode_result = gmaps.geocode(location_name)

        if not geocode_result:
            raise ValueError(f"No results found for location: {location_name}")
        
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return {"lat": lat, "lng": lng}