define duck = Character("Rubber Duck")

label start:

    scene bg bathroom

    show bathtub_back:
        xpos 240
        ypos 240
    show character_head:
        xpos 480
        ypos 320
    show bathtub_front:
        xpos 240
        ypos 240

    jump end

label end:
    "END"
