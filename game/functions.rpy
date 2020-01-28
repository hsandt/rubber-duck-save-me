# Unlike 02_data.rpy, we use functions for store variables

init -1 python:
    from collections import deque

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

    def unlock_topic(topic, progression_index, force_no_dirty=False):
        """
        Unlock new topic for Rubber Duck at given progression index, v1: at highest priority
        v1: If topic was already unlocked, it is simply moved to top priority
        v2: Topic order won't change after it is added

        If topic is already unlocked, progression index is simply maxed to the new index
        (it never decreases)

        However, dirty flag is only set if topic is new or progression index has changed.

        In addition, no_dirty is an optional flag you use to make sure the new topic+progression
        in not considered new/important when added.
        This is useful when you need to update the hint to show some progression,
        but the hint content itself is not important compared to other active topics.

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
        # if it was already dirty, keep it dirty
        old_progression_index, _old_dirty = store.topic_progression[topic]
        if _old_dirty or not dirty and progression_index > old_progression_index:
            dirty = True

        # may revert flag set above, but easier to read than if injected
        # in each condition above
        if force_no_dirty:
            dirty = False

        store.topic_progression[topic] = (progression_index, dirty)

    def start_talking():
        store.is_talking = True
        # hack to fix cursor not reset when rolling forward into dialogue with mouse hovering interactable object
        # (it only works with start because the python statement is executed before the first line of dialogue)
        config.mouse = None

    def stop_talking():
        store.is_talking = False

    def clean_mirror():
        store.cleaned_mirror = True

    def take_cloth():
        store.taken_cloth = True

    def soak_cloth():
        store.soaked_cloth = True

    def take_mop():
        store.taken_mop = True

    def raise_water():
        store.water_level = 2
