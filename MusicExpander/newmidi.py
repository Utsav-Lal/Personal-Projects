from midiutil.MidiFile import MIDIFile
import random
import numpy as np
import pretty_midi
import math
from iden import iden
import sys

notes = []
notes2 = []
# file = 'nuclear_fusion.midi'
file = None
if file is None:
    if len(sys.argv) != 1:
        file = sys.argv[1]
    else:
        file = input("Enter file name: ")
midi_data = pretty_midi.PrettyMIDI(file)
midi_data2 = pretty_midi.PrettyMIDI(file)
print("duration:",midi_data.get_end_time())
print(f'{"note":>10} {"start":>10} {"end":>10}')
for instrument in midi_data.instruments:
    print("instrument:", instrument.program);
    for note in instrument.notes:
        print(f'{note.pitch:10} {note.start:10} {note.end:10}')
        notes.append((note.pitch, note.start, note.end))

for instrument in midi_data2.instruments:
    print("instrument:", instrument.program);
    for note in instrument.notes:
        print(f'{note.pitch:10} {note.start:10} {note.end:10}')
        notes2.append((note.pitch, note.start, note.end-note.start))


timestep = 0.125



# create your MIDI object
mf = MIDIFile(2)     # only 1 track
track = 0   # the only track

time = 0    # start at the beginning
mf.addTrackName(track, time, "crazytrack")
mf.addTempo(track, time, 120)

# mf.addTrackName(1, time, "maintrack")
# mf.addTempo(1, time, 120)

# add some notes
channel = 0
volume = 100

end = 0
for i in notes:
    if i[2] > end:
        end = i[2]

length = int(end/timestep)+5

notesdict = {}
for i in range(length):
    notesdict[i] = []

for i in notes:
    #mf.addNote(track, channel, i[0], i[1], i[2], volume)
    for x in range(math.ceil(i[1]/timestep), math.floor(i[2]/timestep)):
        notesdict[x].append(i[0])


# outnotelist = []
# prevlist = []
# newlist = []
# chorddict = {}
# for i in notesdict:
#     chorddict[i] = iden(notesdict[i])
#     newlist = []
#     if chorddict[i] is not None:
#         for y in range(0, 5):
#             center = (random.choice(notesdict[i])//12)*12
#             pitch = (random.choice(chorddict[i])+int(np.random.normal(0, 0.001))*12+center) % 120
#             newlist.append(pitch)
#             if pitch not in prevlist or random.randint(0, 100) > 80:
#                 #mf.addNote(track, channel, pitch, i*timestep, timestep, volume)
#                 newnote = [pitch, i*timestep, timestep]
#                 outnotelist.append(newnote)
#                 newlist.append(newnote)
#             else:
#                 ournote = None
#                 for i in prevlist:
#                     if i == pitch
#     prevlist = newlist

outnotelist = []
prevlist = []
newlist = []
chorddict = {}
for i in notesdict:
    chorddict[i] = iden(notesdict[i])
    newlist = []
    if chorddict[i] is not None:
        for y in range(0, 5):
            example = random.choice(notesdict[i])
            center = (example//12)*12
            pitch = (random.choice(chorddict[i])+int(np.random.normal(0, 0.001))*12+center) % 120
            if pitch % 12 != example % 12:
                pitch = (random.choice(chorddict[i])+int(np.random.normal(0, 0.001))*12+center) % 120
            inthing = False
            place = None
            for j in prevlist:
                if j[0] == pitch:
                    inthing = True
                    place = j
                    break
            if not inthing or random.randint(0, 100) > 80:
                #mf.addNote(track, channel, pitch, i*timestep, timestep, volume)
                newnote = [pitch, i*timestep, timestep]
                outnotelist.append(newnote)
                newlist.append(newnote)
            else:
                place[2] += timestep
                newlist.append(place)
        for k in prevlist:
            if k not in newlist and k[0] % 12 in chorddict[i] and random.randint(1, 4) > 1:
                k[2] += timestep


    prevlist = newlist

for i in outnotelist:
    mf.addNote(track, channel, i[0], i[1], i[2], volume)






# for i in notes:
#     mf.addNote(track, channel, i[0], i[1], i[2], volume)

#     for y in range(0, 5):

#             a = random.randrange(0, 16)
#             if a < 8:
#                 pitch = (int(np.random.normal(0, 0.001))*12 + i[0]) % 120
#             elif a < 12:
#                 pitch = (int(np.random.normal(0, 0.001))*12 + i[0]+3) % 120
#             else:
#                 pitch = (int(np.random.normal(0, 0.001))*12 + i[0]-5) % 120
#             time1 = np.random.uniform(i[1], i[1]+i[2])
#             time2 = np.random.uniform(i[1], i[1]+i[2])
#             if 0 <= pitch and pitch <= 127:
#                 mf.addNote(track, channel, pitch, min(time1, time2), abs(time1-time2), volume)

# for i in notes2:
#     mf.addNote(1, channel, i[0], i[1], i[2], 50)


# pitch = 60           # C4 (middle C)
# time = 0             # start on beat 0
# duration = 1         # 1 beat long
# mf.addNote(track, channel, pitch, time, duration, volume)

# pitch = 64           # E4
# time = 2             # start on beat 2
# duration = 1         # 1 beat long
# mf.addNote(track, channel, pitch, time, duration, volume)

# pitch = 67           # G4
# time = 4             # start on beat 4
# duration = 1         # 1 beat long
# mf.addNote(track, channel, pitch, time, duration, volume)

# write it to disk
while True:
    try:
        with open("output_chorded.mid", 'wb') as outf:
            mf.writeFile(outf)
        break
    except:
        pass
