

import random


file = 'key.txt'
#This holds the current state of the cipher. It holds all the rotor connections and positions, and the reflector and plugboard connections.

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', \
            'u', 'v', 'w', 'x', 'y', 'z']
#Used for reference to the order of the letters

rotor1move = 0
rotor2move = 0
rotor3move = 0
#Positions of the three rotors

rotor1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', \
            'u', 'v', 'w', 'x', 'y', 'z']
rotor2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', \
            'u', 'v', 'w', 'x', 'y', 'z']
rotor3 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', \
            'u', 'v', 'w', 'x', 'y', 'z']
#These are the connections of all the rotors. If you put g through one of them, you would get the 7th letter of the list as g is the 7th letter of the alphabet. The current rotor arrangements are presets.

reflector = {0:25, 1:24, 2:23, 3:22, 4:21, 5:20, 6:19, 7:18, 8:17, 9:16, 10:15, \
             11:14, 12:13, 13:12, 14:11, 15:10, 16:9, 17:8, 18:7, 19:6, 20:5, \
             21:4, 22:3, 23:2, 24:1, 25:0}
#This holds the connections of the reflector. For each a:b pair, the ath letter connected to the reflector gets sent to the bth letter.

inputbinds = {
    'a': 'b',
    'b': 'a',
    'c': 'd',
    'd': 'c',
    'e': 'f',
    'f': 'e',
    'g': 'h',
    'h': 'g'
}
#This is the plugboard. For each pair, the first letter is changed to the second.

def shuffleall():
  # this function shuffles all the presets to create a random one.
    global rotor1
    global rotor2
    global rotor3
    global reflector
    global rotor1
    global rotor2
    global rotor3
    global inputbinds
    inputbinds = {}
    numbers = list(range(26))
    random.shuffle(rotor1)
    random.shuffle(rotor2)
    random.shuffle(rotor3)
    #randomly sets up the rotors.
    
    reflectorcreate = {}
    while len(numbers) > 0:
        a = random.randint(0, len(numbers) - 1)
        b = random.randint(0, len(numbers) - 1)
        while a == b:
            b = random.randint(0, len(numbers) - 1)
        reflectorcreate[numbers[a]] = numbers[b]
        reflectorcreate[numbers[b]] = numbers[a]
        del numbers[a]
        if a > b:
            del numbers[b]
        elif a < b:
            del numbers[b - 1]
    reflector = reflectorcreate
    #creates the reflector pairs such that no number is connected to two different open

    numbers = list(range(26))
    for x in range(8):
        a = random.choice(numbers)
        b = random.choice(numbers)
        while a == b:
            b = random.choice(numbers)
        inputbinds[alphabet[a]] = alphabet[b]
        inputbinds[alphabet[b]] = alphabet[a]
        del numbers[numbers.index(a)]
        del numbers[numbers.index(b)]
    #does the same thing with the plugboard, but not with all letters (only 8)

    f = open(file, 'w')
    f.write("")
    f.close()
    #resets the current setup
    save()
    #saves the new key


def save():
  #writes in all the information about the enigma setup
    global rotor1
    global rotor2
    global rotor3
    global reflector
    global rotor1move
    global rotor2move
    global rotor3move
    global inputbinds
    f = open(file, 'w')
    f.write(str({"1st Rotor":rotor1, "1st Rotor Position":rotor1move, "2nd Rotor":rotor2, "2nd Rotor Position":rotor2move, "3rd Rotor":rotor3, "3rd Rotor Position":rotor3move, \
                 "Reflector Connections":reflector, "Plugboard Connections":inputbinds}))
    f.close()


def load():
  #loads the information about the setup into the code
    global rotor1
    global rotor2
    global rotor3
    global reflector
    global rotor1move
    global rotor2move
    global rotor3move
    global inputbinds
    f = open(file, 'r')
    a = eval(f.read())
    rotor1 = a["1st Rotor"]
    rotor2 = a["2nd Rotor"]
    rotor3 = a["3rd Rotor"]
    rotor1move = a["1st Rotor Position"]
    rotor2move = a["2nd Rotor Position"]
    rotor3move = a["3rd Rotor Position"]
    reflector = a["Reflector Connections"]
    inputbinds = a["Plugboard Connections"]


def codeletter(letter):
  #codes a letter into another
    global rotor1
    global rotor2
    global rotor3
    global reflector
    global rotor1move
    global rotor2move
    global rotor3move
    global inputbinds
    currentletter = letter
    l = False

    for i in inputbinds:
        if i == currentletter:
            l = True
    if l == True:
        currentletter = inputbinds[currentletter]
    #sends letter through plugboard
    
    currentletter = rotor1[alphabet.index(currentletter)]
    currentletter = rotor2[alphabet.index(currentletter)]
    currentletter = rotor3[alphabet.index(currentletter)]
    #Goes through 3 rotors
    
    currentletter = alphabet[(reflector[(alphabet.index\
                                             (currentletter)+rotor3move)%26]+\
                                   rotor3move)%26]
    #goes through reflector

    currentletter = alphabet[rotor3.index(currentletter)]
    currentletter = alphabet[rotor2.index(currentletter)]
    currentletter = alphabet[rotor1.index(currentletter)]
    #back through the rotors
    
    l = False
    for i in inputbinds:
        if i == currentletter:
            l = True
    if l == True:
        currentletter = inputbinds[currentletter]
    #back through the plugboard

    return currentletter


def switch():
  #Turns the rotor by moving the last letter of the list to the beginning
    global rotor1
    global rotor2
    global rotor3
    global reflector
    global rotor1move
    global rotor2move
    global rotor3move
    global inputbinds
    if True:

        rotor1move += 1
        rotor1move = rotor1move % 26
        k = rotor1[len(rotor1) - 1]
        del rotor1[len(rotor1) - 1]
        rotor1.insert(0, k)
        if rotor1move == 0:
          #Each time a rotor makes a complete turn, the next one moves
            rotor2move += 1
            rotor2move = rotor2move % 26
            k = rotor2[len(rotor2) - 1]
            del rotor2[len(rotor2) - 1]
            rotor2.insert(0, k)
            if rotor2move == 0:
                rotor3move += 1
                rotor3move = rotor3move % 26
                k = rotor3[len(rotor3) - 1]
                del rotor3[len(rotor3) - 1]
                rotor3.insert(0, k)

   


def codephrase():
    global rotor1
    global rotor1move
    global rotor2
    global rotor2move
    global rotor3
    global rotor3move
  #puts it all together to code a phrase. The method for coding and decoding are the same.
    nonletterlist = [" ", ".", ",", "'", "!", '''"''', "?", ":", ";", "-", "(", ")"]
  #these just get coded into themselves as they are not letters.
    phrase = input("What would you like to code/decode? ")
    #gets phrase to code/decode

    f = open(file, 'r')
    a = f.read()
    f.close()
    if a != "":
      load()
    save()
    #automatically loads in the key
    
    oldrotor1 = rotor1[:]
    oldrotor1move = rotor1move
    oldrotor2 = rotor2[:]
    oldrotor2move = rotor2move
    oldrotor3 = rotor3[:]
    oldrotor3move = rotor3move
    #holds on to the old data for decoding
    
    codedphrase = ""
    #finished phrase

    phrase = phrase.lower()
    #lowercases the phrase for easy coding

    for i in phrase:
        k = False
        for j in nonletterlist:
          if i == j:
            k = True
        #checks if character is a letter or not
        if k == True:
          #if character is not a letter it just sends it through
            codedphrase += i
        else:
            i.lower()
            g = codeletter(i)
            #codes letters one by one
            
            switch()
            #rotates rotors
            
            codedphrase += g
            #adds letter in

    print('Code:', codedphrase)
    #gives you the code
    
    rotor1 = oldrotor1
    rotor1move = oldrotor1move
    rotor2 = oldrotor2
    rotor2move = oldrotor2move
    rotor3 = oldrotor3
    rotor3move = oldrotor3move
    #resets key

def userinput():
  print("Some additional information:")
  print("The key right now is a random key, and has been saved into the file 'key.txt'.")
  print("The next time you run the program, the key will be saved.")
  print("However, if you want to use a new key but still want to save the old one, you can get the key by pressing k and copying it somewhere before changing the key.")
  print("You can then go back and put the new key in later when you want it.")
  shuffleall()
  while True:
    print("Type 'c' to code/decode, 'k' to get the current key, or 'n' to change the key.")
    g = input("- ")
    if g == 'c':
      codephrase()
    elif g == 'n':
      print("Type 'r' for a random key or 's' to enter in a specific key.")
      h = input("- ")
      if h == 'r':
        shuffleall()
      elif h == 's':
        k = input("Paste key here: ")
        f = open('key.txt', 'w')
        f.write(k)
        f.close()
    elif g == 'k':
      print('Key:', str({'1st Rotor':rotor1, '1st Rotor Position':rotor1move, '2nd Rotor':rotor2, '2nd Rotor Position':rotor2move, '3rd Rotor':rotor3, '3rd Rotor Position':rotor3move, \
                 'Reflector Connections':reflector, 'Plugboard Connections':inputbinds}))
    #gives you the key that was used

userinput()
#starts the program
