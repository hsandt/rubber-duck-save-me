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
    # play music
    $ start_talking()
    window show
    mc "Uh..."
    mc "Is somebody here?"
    mc "I can't move my legs anymore... And my arms are not strong enough to drag me out of the bathtub!"
    mc "That's not good... I need to find a way to get out, or I will drown!"
    window hide
    pause 1.0
    $ stop_talking()
    while True:
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

label rubber_duck:
    "hello"
    return

label use_faucet:
    "You turn the faucet on."
    call water_rises
    jump ending

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
    # stop music fadeout 1.0
    pause 1.0
    $ stop_talking()
