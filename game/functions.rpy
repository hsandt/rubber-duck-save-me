init -1 python:

    # The current objective advances as puzzles are solved and hints are given.
    # They allow us to determine the next Rubber Duck hint.
    #
    # List of objectives, as discovered backward from the final one:
    # - escape
    # - reach faucet
    # - take pole
    # - find pole
    # - clean mirror
    # - soak cloth
    # - take cloth
    store.current_objective = "escape"

    # Progression flag/numbers
    store.cleaned_mirror = False
    store.taken_mop = False
    store.water_level = 1

    # Interaction state
    store.is_talking = False

    def start_talking():
        store.is_talking = True
        # hack to fix cursor not reset when rolling forward into dialogue with mouse hovering interactable object
        # (it only works with start because the python statement is executed before the first line of dialogue)
        config.mouse = None

    def stop_talking():
        store.is_talking = False

    def clean_mirror():
        store.cleaned_mirror = True
        store.current_objective = "take pole"

    def take_mop():
        store.taken_mop = True
        store.current_objective = "reach faucet"

    def raise_water():
        store.water_level = 2
