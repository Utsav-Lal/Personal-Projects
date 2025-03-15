from midiutil.MidiFile import MIDIFile
import random
import numpy as np
import pretty_midi
import math
from iden import iden
import sys


# Handles the input file
file = None
if file is None:
    if len(sys.argv) != 1:
        file = sys.argv[1]
    else:
        file = input("Enter file name: ")


# Collects all the notes in the midi file
notes = []
midi_data = pretty_midi.PrettyMIDI(file)
for instrument in midi_data.instruments:
    for note in instrument.notes:
        notes.append((note.pitch, note.start, note.end))


# Timestep - how small the new notes can be
timestep = 0.125



# Sets up the track
mf = MIDIFile(2)
track = 0

time = 0
mf.addTrackName(track, time, "crazytrack")
mf.addTempo(track, time, 120)

channel = 0
volume = 100


# Finds the length of the piece
end = 0
for i in notes:
    if i[2] > end:
        end = i[2]

length = int(end/timestep)+5


# Generates a dictionary of nodes at each time interval
notesdict = {}
for i in range(length):
    notesdict[i] = []

for i in notes:
    for x in range(math.ceil(i[1]/timestep), math.floor(i[2]/timestep)):
        notesdict[x].append(i[0])


# Expands the song by adding new notes within the chords of the time intervals
outnotelist = []
prevlist = []
newlist = []
chorddict = {}
for i in notesdict:
    chorddict[i] = iden(notesdict[i])
    newlist = []
    if chorddict[i] is not None:

        # If the previous notes still fit have a high chance of making them longer
        for k in prevlist:
            if k not in newlist and k[0] % 12 in chorddict[i] and random.randint(1, 4) > 1:
                k[2] += timestep
                newlist.append(k)

        # Creates new notes
        for y in range(0, 5):
            # Generates pitch out of allowed notes in chord - makes notes closer to the notes in the original music
            example = random.choice(notesdict[i])
            center = (example//12)*12
            pitch = (random.choice(chorddict[i])+int(np.random.normal(0, 0.001))*12+center) % 120
            if pitch % 12 != example % 12:
                pitch = (random.choice(chorddict[i])+int(np.random.normal(0, 0.001))*12+center) % 120

            # Makes sure note has not already been added
            placed = False
            for j in newlist:
                if j[0] == pitch:
                    placed = True
                    break
            if not placed:
                # Checks if note was there in the previous step
                inthing = False
                place = None
                for j in prevlist:
                    if j[0] == pitch:
                        inthing = True
                        place = j
                        break

                # if it is not there, it is repeated, and it is also repeated by a small chance if it is
                if not inthing or random.randint(0, 100) > 80:
                    newnote = [pitch, i*timestep, timestep]
                    outnotelist.append(newnote)
                    newlist.append(newnote)
                else:  # extend the previous notes
                    place[2] += timestep
                    newlist.append(place)
        
    prevlist = newlist


# Write all the notes
for i in outnotelist:
    mf.addNote(track, channel, i[0], i[1], i[2], volume)



# Write it to ourput file
while True:
    try:
        with open("output_chorded.mid", 'wb') as outf:
            mf.writeFile(outf)
        break
    except:
        pass
