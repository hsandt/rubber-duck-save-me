define mc = Character("Jeremiah", color="#FF9331")
define staff = Character("Staff member", color="#D881ED")
define duck = Character("Rubber Duck", color="#FFFF00")

label start:
    call initialize_store
    call show_initial_scene
    return

label initialize_store:

    # v1: list of discovered topics, from the most recent (relevant) to the oldest
    # They must cover all unlocked topics.
    # A topic is discovered when the corresponding item is picked or seen.
    # In v2, we'll be able to select topic with an icon-based interface,
    #   this won't be needed anymore.
    # Note: deque is imported in functions.rpy
    define topics_by_priority = deque(["escape"])

    # v2: unlocked topics remain in same order, and will be selected manually
    # This value will replace topics_by_priority
    # store.unlocked_topics = ["escape"]

    # The unlocked topics are filled when the character sees or picks a new item,
    # or via a Rubber Duck hint
    # Full list:
    # - escape
    # - alarm
    # - faucet
    # - mirror

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
    define topic_progression = {
        "escape": (0, True),  # must start dirty for initial hint
        "alarm": (0, False),
        "faucet": (0, False),
        "mirror": (0, False)
    }

    # Progression flag/numbers
    define cleaned_mirror = False
    define taken_mop = False
    define taken_cloth = False
    define soaked_cloth = False
    define water_level = 1

    # Interaction state
    define is_talking = False

    return

label show_initial_scene:
    scene bg bathroom

    show bathtub_back:
        xpos 160
        ypos 240
    show water lv1:
        xpos 160
        ypos 240
    show character_head lv1:
        xpos 480
        ypos 300
    show bathtub_front:
        xpos 160
        ypos 240

    show screen bathroom

    jump intro

label intro:
    play music bathroom

    $ start_talking()
    window show
    mc "Uh..."
    mc "Is somebody here?"
    mc "I can't move my legs anymore... And my arms are not strong enough to drag me out of the bathtub!"
    mc "That's not good... I need to find a way to get out, or I will drown!"
    window hide
    pause 1.0
    window show
    mc "OK, cool down... What if I applied the method of Rubber Duck debugging? I'll just state my problem in front of that fine toy, as if I was talking to a person."
    mc "Hopefully, it will help me find a solution."
    window hide
    $ stop_talking()
    jump free_interaction

# Interaction loop
label free_interaction:
    $ game_over = False

    while not game_over:
        python:
            # to support redo actions when going forward in history
            roll_forward = renpy.exports.roll_forward_info()

            try:
                # in general, rv will be None in this game (but it receives a value if we use a ChoiceReturn)
                rv = renpy.ui.interact(mouse="menu", type="menu", roll_forward=roll_forward)
            except (renpy.game.JumpException, renpy.game.CallException) as e:
                rv = e

            # save action for roll forward
            renpy.exports.checkpoint(rv)

            # no-transition parameter on basic interactions (optional)
            if renpy.config.implicit_with_none:
                renpy.game.interface.do_with(None, None)

            # transfer call/jump for interactions sending user to another label
            if isinstance(rv, (renpy.game.JumpException, renpy.game.CallException)):
                raise rv

    return

# Rubber duck hints
label rubber_duck:
    $ start_talking()
    $ topic = auto_pick_topic()  # v1
    $ hint_label = call_hint(topic)
    $ stop_talking()
    return

# we assume all hints below are surrounded by start/stop_talking so we don't need to
# surround them again

label hint_escape_0:
    mc "So, Rubber duck, here is the thing. I'm stuck in that bathtub and I need to get out."
    duck "..."
    mc "My legs are completely frozen, and all I can do is turn my head a bit and move my arms."
    duck "..."
    mc "I need some way to alert the hotel staff outside... Something that makes a lot of noise."
    duck "..."
    mc "Hey! What about this fish-shaped alarm?"
    duck "..."
    return

label hint_escape_0_recall:
    mc "I could use the alarm to escape, right?"
    duck "..."
    return

label hint_alarm_0:
    mc "The bath alarms only rings when sensing some danger. It can't detect that I'm stuck here though. What could it sense then?"
    duck "..."
    mc "Since it's hanging at the top of the bathtub, I assume it can only detect water when it's high enough."
    duck "..."
    mc "But if it goes too high, danger... That's it! All I need to do is raise the water level! Thanks, rubber duck!"
    duck "..."
    return

label hint_alarm_0_recall:
    mc "Basically if I manage to raise the water level, I'll be safe, right?"
    duck "..."
    return

label hint_faucet_0:
    mc "My legs can't move, and I can't reach the faucet with my arms alone..."
    duck "..."
    mc "Yeah, that's right. I need some tool to extend range."
    duck "..."
    mc "Like a pole or something."
    duck "..."
    return

label hint_faucet_0_recall:
    mc "I need to find some kind of pole to reach the faucet's handles..."
    return

label hint_faucet_1:
    mc "The faucet is still too far for my arms alone. But maybe I can use that mop to push the handles from here?"
    duck "..."
    return

label hint_faucet_1_recall:
    mc "Maybe I can use that mop to push the faucet's handles?"
    duck "..."
    return

label hint_mirror_0:
    mc "I can't see anything in the mirror, it's too dirty. But I guess if it was cleaner, it would show the area behind me."
    duck "..."
    mc "So how do I clean that thing?"
    duck "..."
    mc "Well, I guess a quick wipe with a sponge or cloth would do it good."
    duck "..."
    return

label hint_mirror_0_recall:
    mc "I could use a sponge or a cloth to clean the mirror, right?"
    duck "..."
    return

label hint_mirror_1:
    mc "That cloth is too dry to clean hard dirt on the mirror. How can I solve that?"
    duck "..."
    mc "Soaking it would make it work better, I guess. But where do I find water?"
    duck "..."
    mc "Oh, of course."
    return

label hint_mirror_1_recall:
    mc "I'll just soak that cloth in a volume of water. Do you mind if borrow you some?"
    duck "..."
    return

label hint_mirror_2:
    pass
    # fallthrough

label hint_mirror_2_recall:
    mc "I should try the soaked cloth on the mirror now."
    duck "..."
    return

label hint_mirror_3:
    pass
    # fallthrough

label hint_mirror_3_recall:
    mc "I did a nice job, didn't I?"
    duck "..."
    return

# Various interactions
label look_bath_alarm:
    $ start_talking()
    # v1: assume water level is 1, since the game currently ends as soon as you get drowned
    mc "The bath alarm displays \"SAFE\". It will ring if it detects a danger."
    $ stop_talking()
    $ unlock_topic("alarm", 0)
    return

label look_darkness:
    $ start_talking()
    mc "I can't turn my head more than 90 degrees in that direction, so I'm not sure what's behind me."
    $ stop_talking()
    return

label look_mirror:
    $ start_talking()
    if not cleaned_mirror:
        if taken_cloth:
            if soaked_cloth:
                mc "Let's clean this with the cloth."
                # TODO: rubbing SFX
                $ clean_mirror()
                mc "Ah, that's better. I can see behind me without breaking my neck now."
                $ unlock_topic("mirror", 3)
            else:
                # TODO: rubbing SFX
                mc "Hmm... I'm trying to clean the mirror with the cloth, but it's too dry to work."
                $ unlock_topic("mirror", 1)
        else:
            mc "Too much mist and dirt on this mirror, I can't see anything."
            # FIXME: store var not saved (but saved if modified in call_hint directly)
            $ unlock_topic("mirror", 0)
    elif taken_mop:
        mc "I see nothing me in my back."
    else:
        mc "I can see a mop behind me."
    $ stop_talking()
    return

label take_cloth:
    $ start_talking()
    $ take_cloth()
    mc "I got a microfiber cloth."
    $ stop_talking()
    return

label soak_cloth:
    $ start_talking()
    $ soak_cloth()
    mc "Let's soak that cloth!"
    # todo: SFX
    mc "Here we go! Ready to clean."
    $ stop_talking()
    $ unlock_topic("mirror", 2)
    return

label take_mop:
    $ start_talking()
    $ take_mop()
    mc "I got the mop!"
    $ stop_talking()
    $ unlock_topic("faucet", 1)
    return

label use_faucet:
    $ start_talking()
    if taken_mop:
        "You push the faucet's handles with the mop and somewhat manage to turn it on."
        # TODO FX: hit faucet handles, faucet turn on
        call water_rises
        "The goldfish-shaped bath alarm starts ringing like hell."
        $ stop_talking()
        jump ending
    else:
        mc "Uhng... I can't reach it my arms!"
        $ stop_talking()
        $ unlock_topic("faucet", 0)
        return

# Events
label water_rises:
    $ raise_water()
    show water lv2
    show character_head lv2
    show faucet_water:
        xpos 960
        ypos 300
    # if you don't indicate a transition, images above will have no transition whereas the duck from screen bathroom will dissolve
    # (seems to be set in options.rpy config, but not sure how to change this)
    # so always set a transition (whether instant or dissolve) so both types of images follow it and are updated in sync
    with dissolve
    return

label ending:
    $ start_talking()
    window show
    staff "Hello? Is there somebody?"
    mc "Yes! I'm stuck in the bath and I can't move my legs! Can you get me out of here?"
    staff "Ok, just a moment. I need to find a way to open the door."
    # play sound break_door
    window hide
    pause 1.0
    window show
    staff "Are you alright??"
    mc "Yeah, thank you... I was about to dro-- *blub blub blub*"
    staff "Hey, hold on! Hold on!!"
    hide screen bathroom
    show overlay black
    with dissolve
    "Jeremiah was saved in extremis from an imminent death."
    "He was grateful, of course, to his incredible wits, but also to the rubber duck, a small being that helped him to formulate his problem and find innovative solutions."
    "He also promised never to stay in a freezing cold bath again."
    window hide

    stop music fadeout 1.0

    pause 1.0
    $ stop_talking()
    $ game_over = True
    return
