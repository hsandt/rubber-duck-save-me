define mc = Character("Jeremiah", color="#FF9331")
define staff = Character("Staff member", color="#D881ED")
define duck = Character("Rubber Duck", color="#FFFF00")

label start:

    # DEBUG
    # show image "bg/Screen ref.png"

    scene bg bathroom

    show bathtub_back:
        xpos 160
        ypos 240
    show bath_alarm lv1:
        xpos 680
        ypos 340
    show water lv1:
        xpos 160
        ypos 240
    show character_head lv1:
        xpos 480
        ypos 300
    show bathtub_front:
        xpos 160
        ypos 240
    show mirror:
        xpos 640
        ypos 20

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
    mc "OK, cool down... What if I applied the Rubber Duck method? I'll just state my problem in front of that fine toy, as if I was talking to a person."
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
            print("[DEBUG] ui.interact: {}".format(rv))

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
    if current_objective == "escape":
        mc "So, Rubber duck, here is the thing. I'm stuck in that bathtub and I need to get out."
        duck "..."
        mc "My legs are completely frozen, and all I can do is turn my head a bit and move my hands."
        duck "..."
        mc "If only there was some way to alert the hotel staff outside... I need something that makes enough noise."
        duck "..."
        mc "Noise? That's right, I need to trigger the alarm system! If I remember correctly, it starts when the water level is too high."
        mc "So I just need to raise the level. Thanks, rubber duck!"
        duck "..."
    elif current_objective == "reach faucet":
        mc "I want to raise the water level but I can't reach that damn faucet!"
        mc "How can I reach it?"
        duck "..."
        mc "My legs can't move so I have to stretch my arms... But they're not long enough. If only I had a way to extend my arm..."
        duck "..."
        mc "That's it! I need some kind of pole! There may be one in this bathroom. Thanks, rubber duck!"
        duck "..."
    else:
        mc "I think I got everything I need!"
    $ stop_talking()
    return

# Various interactions
label take_mop:
    $ start_talking()
    $ take_mop()
    mc "I got it!"
    $ stop_talking()
    return

label use_faucet:
    $ start_talking()
    if taken_mop:
        "You turn the faucet on."
        call water_rises
        "The goldfish-shaped bath alarm starts ringing like hell."
        $ stop_talking()
        jump ending
    else:
        mc "Uhng... I can't reach it my arms!"
        $ current_objective = "reach faucet"
        $ stop_talking()
        return

# Events
label water_rises:
    $ raise_water()
    show water lv2
    show character_head lv2
    show bath_alarm lv2
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
