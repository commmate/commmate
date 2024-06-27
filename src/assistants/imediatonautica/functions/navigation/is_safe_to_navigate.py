from ..assistant_function import AssistantFunction


class IsSafeToNavigateFunction(AssistantFunction):
    def __init__(self):
        super().__init__(
            name="is_safe_to_navigate",
            description="Check if it's safe to navigate based on boat draft, minimum depth, and tide height.",
            parameters={
                "type": "object",
                "properties": {
                    "draft": {"type": "number", "description": "The draft of the boat."},
                    "min_depth": {"type": "number", "description": "The minimum depth of the channel, port, marina, or anchorage."},
                    "tide_height": {"type": "number", "description": "The tide height at the expected time."}
                },
                "required": ["draft", "min_depth", "tide_height"]
            }
        )

    def action(self, **kwargs):
        draft = kwargs.get('draft')
        min_depth = kwargs.get('min_depth')
        tide_height = kwargs.get('tide_height')

        if draft is None or min_depth is None or tide_height is None:
            raise ValueError("draft, min_depth, and tide_height are required")

        return {"result": (min_depth + tide_height) > draft}