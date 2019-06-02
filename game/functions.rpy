init -1 python:

    store.is_talking = False
    store.water_level = 1

    def start_talking():
        store.is_talking = True

    def stop_talking():
        store.is_talking = False

    def raise_water():
        store.water_level = 2
