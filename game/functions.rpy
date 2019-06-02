init -1 python:

    store.is_talking = False

    def start_talking():
        store.is_talking = True

    def stop_talking():
        store.is_talking = False
