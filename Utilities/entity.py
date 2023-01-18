from threading import Thread


class Entity(Thread):
    def __init__(self):
        # Call the thread constructor
        super().__init__()

    # Run method remain to be overrided
    def run(self):
        pass
