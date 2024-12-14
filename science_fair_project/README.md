Made in Spring 2022 for school science fair - won second place!

This program allows the simulation of the evolution of dot creatures at different mutation rates. The populations are printed to a separate file. Tkinter is required, and this runs in python.

Environment: Bushes for food and water pools are spread throughout the map, and they change in the amount of food produced and size respectively over the simulation. When food is eaten (red circle is gone), it takes some time to replenish (red circle comes back).
Large grey predators occasionally spawn that have a hunger meter - when it goes out, they chase dot animals and turn red.

Traits:
    Speed - moves faster but uses more resources
    Vision - How far away things are visible to the dot, but uses more resources
    Hunger tolerance - how much hunger must be depleted before the dot seeks food
    Thirst tolerance - the same but for thirst
    minturn/maxturn - amount of change in direction when wandering

Each trait has a genotype, with two values given by parents, and a phenotype, what is expressed, which is an average of the genotype

States in order of precedence:
    Run - run away from predator - dot turns white
    Go to water - when it sees water and is thirsty, go to it - turns blue
    Go to food - same but for food - turns yellow
    Mate - when it sees another dot ready to mate, go toward it and mate - turns pink
    Wander - passive motion - dot is black

When mating, a few new dots are created with a genotype having one gene from each parent. The genes are changed slightly depending on the mutation rate. The parents lose resources.

Information:
    Circle - vision radius
    White bar - age - dot dies when it runs out
    Yellow bar - hunger - white vertical is hunger tolerance
    Blue bar - thirst - same for thirst tolerance
    Pink bar - readiness to mate

Dots die when:
    They run out of food
    They run out of water
    They are caught by the predator
    They die of old age

