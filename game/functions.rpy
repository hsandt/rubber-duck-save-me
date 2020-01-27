# Unlike 02_data.rpy, we use functions for store variables

init -1 python:
    from collections import deque

    # v1: list of discovered topics, from the most recent (relevant) to the oldest
    # They must cover all unlocked topics.
    # A topic is discovered when the corresponding item is picked or seen.
    # In v2, we'll be able to select topic with an icon-based interface,
    #   this won't be needed anymore.
    store.topics_by_priority = deque(["escape"])

    # v2: unlocked topics remain in same order, and will be selected manually
    # This value will replace topics_by_priority
    # store.unlocked_topics = ["escape"]

    # The unlocked topics are filled when the character sees or picks a new item,
    # or via a Rubber Duck hint
    # Full list:
    # - escape
    # - alarm
    # - faucet
    # - mop
    # - mirror
    # - cloth

    # The topic progression dict tells how far the player advanced in a topic
    #   (or tried and failed).
    # Each value is [progression_index: integer, dirty: bool]
    # progression_index:
    # - 0: topic discovered (item picked or seen), but did not ask Rubber Duck about it yet
    # - N=1+: asked Rubber Duck N times about this topic
    # Note that solving the puzzle part related to a topic may make the Rubber Duck
    #   ignore N and skip to some conclusion sentence like "Mirror is already cleaned!"
    # dirty:
    # - True: the character has not talked to Rubber Duck on this topic,
    #   at this progression yet
    # - False: hint has already been given on this topic, at this progression
    store.topic_progression = {
        "escape": (0, True),  # must start dirty for initial hint
        "alarm": (0, False),
        "faucet": (0, False),
        "mop": (0, False),
        "mirror": (0, False),
        "cloth": (0, False)
    }

    def auto_pick_topic():
        """
        v1 only: Auto-pick topic with highest priority (relevance) with a new hint,
        else pick just pick the highest priority topic.

        """
        # v1: auto-topic-picking:
        #   find the first topic by priority (last item seen or picked)
        #   for which hint is new
        assert(store.topics_by_priority)

        # if you cannot find a new hint to say during the loop, default to most relevant
        # (highest priority)
        picked_topic = store.topics_by_priority[0]

        for topic in store.topics_by_priority:
            _progression_index, dirty = store.topic_progression[topic]
            if dirty:
                # hint is new => say it now
                picked_topic = topic
                break

        return picked_topic

    def get_hint_label(topic):
        progression_index, dirty = store.topic_progression[topic]

        # the 2nd+ time you get a hint, just play the shorter version instead
        recall_suffix = "_recall" if not dirty else ""
        return "hint_{}_{}{}".format(topic, progression_index, recall_suffix)

    def call_hint(topic):
        # get hint label before removing dirty flag
        # (so it uses the proper value when checking for initial vs recall label)
        hint_label = get_hint_label(topic)

        # now remove dirty flag
        old_progression_index, _old_dirty = store.topic_progression[topic]
        store.topic_progression[topic] = (old_progression_index, False)

        # say the hint
        return renpy.call(hint_label)

    def unlock_topic(topic, progression_index):
        """
        Unlock new topic for Rubber Duck at given progression index, v1: at highest priority
        v1: If topic was already unlocked, it is simply moved to top priority
        v2: Topic order won't change after it is added

        If topic is already unlocked, progression index is simply maxed to the new index
        (it never decreases)

        However, dirty flag is only set if topic is new or progression index has changed.

        """
        dirty = False

        # don't want to use .index + try-except ValueError, so a little suboptimal but fine
        if topic in store.topics_by_priority:
            store.topics_by_priority.remove(topic)
        else:
            # topic is new, so always dirty entry
            dirty = True

        # pushing to list front requires making new list, suboptimal again, but fine
        store.topics_by_priority.appendleft(topic)

        # if we progressed in the topic, mark it dirty
        old_progression_index, _old_dirty = store.topic_progression[topic]
        if not _old_dirty and not dirty and progression_index > old_progression_index:
            dirty = True

        store.topic_progression[topic] = (progression_index, dirty)


    # Hint tracking (actions tried)
    store.tried_reach_faucet_with_hand = False

    # Progression flag/numbers
    store.cleaned_mirror = False
    store.taken_mop = False
    store.taken_cloth = False
    store.soaked_cloth = False
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

    def take_cloth():
        store.taken_cloth = True
        store.current_objective = "soak cloth"

    def soak_cloth():
        store.soaked_cloth = True
        store.current_objective = "clean mirror"

    def take_mop():
        store.taken_mop = True
        store.current_objective = "reach faucet"

    def raise_water():
        store.water_level = 2
