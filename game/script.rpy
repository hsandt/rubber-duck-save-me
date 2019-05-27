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
    show character_head:
        xpos 480
        ypos 300
    # show rubber_duck:
    #     xpos 800
    #     ypos 360
    show bathtub_front:
        xpos 160
        ypos 240

    show screen bathroom

    jump intro

label intro:
    # play music
    $ is_talking = True
    mc "Uh..."
    mc "Is somebody here?"
    mc "I can't move my legs anymore... And my arms are not strong enough to drag me out of the bathtub!"
    mc "That's not good... I need to find a way to get out, or I will drown!"
    $ is_talking = False
    window hide
    pause 1.0
    jump ending

label rubber_duck:
    "hello"
    return

label ending:
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
    show overlay black with dissolve
    "Jeremiah was saved in extremis from an imminent death."
    "He was grateful, of course, to his incredible wits, but also to the rubber duck, a small being that helped him to formulate his problem and find innovative solutions."
    "He also promised never to stay in a freezing cold bath again."
    window hide
    # stop music fadeout 1.0
    pause 1.0
