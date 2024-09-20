import os
import logging
from RealtimeTTS import CoquiEngine


class Engine:
    """Singleton class for the CoquiEngine instance."""

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.engine = CoquiEngine(
            local_models_path=path + "/../models",
            level=logging.ERROR,
        )
        self.engine.set_voice("Luis Moray")

    @staticmethod
    def get_instance():
        """Get the CoquiEngine instance."""
        if not hasattr(Engine, "instance"):
            Engine.instance = Engine()
        return Engine.instance.engine
