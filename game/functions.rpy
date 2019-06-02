init -1 python:

    store.is_talking = False
    store.water_level = 1

    def start_talking():
        store.is_talking = True
        # hack to fix cursor not reset when rolling forward into dialogue with mouse hovering interactable object
        # (it only works with start because the python statement is executed before the first line of dialogue)
        config.mouse = None

    def stop_talking():
        store.is_talking = False

    def raise_water():
        store.water_level = 2
