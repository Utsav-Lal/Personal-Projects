def iden(notelst):
    major = [0, 4, 7]
    minor = [0, 3, 7]
    maj7 = [0, 4, 7, 10]
    min7 = [0, 3, 7, 10]
    dim7 = [0, 3, 6, 9]
    chordlist = [major, minor, maj7, min7, dim7]
    maxamount = 0
    chord = None
    for i in chordlist:
        for j in range(0, 12):
            totamount = 0
            for n in notelst:
                if (n-j) % 12 in i:
                    totamount += 1
            if totamount > maxamount:
                maxamount = totamount
                chord = [(j+c) % 12 for c in i]


    return chord
