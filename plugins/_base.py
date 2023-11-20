class Plugin(object):

    def __init__(self, configuration):
        self._config = configuration

    def setup(self):
        # Override to run tasks on initialization
        return

    def handle(self, directive: str, *args, **kwargs) -> dict:
        response = {"error": f"Unsupported directive: {directive}"}        
        if hasattr(self, f"_cmd_{directive}"):
            response = getattr(self, f"_cmd_{directive}")(**kwargs)            
        return response
