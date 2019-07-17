init -1 python:

    # The current objective advances as puzzles are solved. They allow us to determine the next Rubber Duck hint.
    # List of objectives:
    # escape
    # reach faucet
    store.current_objective = "escape"
    store.is_talking = False
    store.taken_mop = False
    store.water_level = 1

    def start_talking():
        store.is_talking = True
        # hack to fix cursor not reset when rolling forward into dialogue with mouse hovering interactable object
        # (it only works with start because the python statement is executed before the first line of dialogue)
        config.mouse = None

    def stop_talking():
        store.is_talking = False

    def take_mop():
        store.taken_mop = True
        store.current_objective = "use mop on faucet"

    def raise_water():
        store.water_level = 2
