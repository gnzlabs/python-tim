class Plugin(object):

    def __init__(self, configuration):
        self._config = configuration

    def setup(self):
        # Override to run tasks on initialization
        return

    def handle(self, directive: str, *args, **kwargs) -> dict:
        raise NotImplementedError()
