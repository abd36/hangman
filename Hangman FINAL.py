from tkinter import *
from random import choice
from pygame import mixer
from time import clock

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MIXER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mixer.pre_init(frequency=50000)
mixer.init()
incorrects = mixer.Sound('{0}/incorrects.wav'.format(sys.path[0]))
corrects = mixer.Sound('{0}/corrects.wav'.format(sys.path[0]))
notes = mixer.Sound('{0}/notes.wav'.format(sys.path[0]))
losts = mixer.Sound('{0}/losts.wav'.format(sys.path[0]))
wons = mixer.Sound('{0}/wons.wav'.format(sys.path[0]))
mixer.music.load('{0}/music.mp3'.format(sys.path[0]))
mixer.music.set_volume(1)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def chooseword():
    global listofwords
    global word
    word = choice(listofwords)
    listofwords.remove(word)
    word = list(word)

    global wordlabellist
    for l in word:
        wordlabellist.append('_ ')

def restart():
    mixer.music.play()
    global guessed
    guessed = []
    global incorrect
    incorrect = 0
    global wordlabellist
    wordlabellist = []
    global word
    word = ''
    chooseword()
    wordlabel.configure(text="".join(wordlabellist))
    bglabel.configure(image=bgimage)
    note.configure(text='a new game, with a new word')
    notes.play()
    letterguess.configure(state='normal')
    global state
    state = True
    global currenttime
    currenttime = 0
    timer()

def exist():
    mixer.music.stop()
    root.destroy()

def clear(x):
    letterguess.delete(0,END)

def guess(x):
    global score
    global incorrect 
    global state
    score = 0
    letter = letterguess.get()
    letter = letter.lower()
    clear(1)
    positions = []

    if (letter.isalpha() == True): #if it's a letter
        if (len(letter) == 1): #if it's one letter
            if (letter not in guessed): #if the letter hasn't been already guessed
                guessed.append(letter)
                note.configure(text='')
                if (letter in word): #if the letter is in the word
                    corrects.play()
                    note.configure(text='')
                    for n, wordl in enumerate(word):
                        if (wordl == letter):
                            positions.append(n)
                    for p in positions:
                        wordlabellist[p] = letter
                elif (letter not in word):
                    incorrect += 1
                    incorrects.play()
            elif (letter in guessed):
                notes.play()
                note.configure(text="you've guessed the letter '{0}' already".format(letter))
        else:
            notes.play()
            note.configure(text="one letter bruv, just one...")
    else:
        notes.play()
        note.configure(text="well, it's got to be a letter, right?")

    if wordlabellist[0] != '_ ':
        wordlabellist[0] = wordlabellist[0].upper()   
    wordlabel.configure(text="".join(wordlabellist))

    if incorrect == 1:
        bglabel.configure(image=bgimage1)
    elif incorrect == 2:
        bglabel.configure(image=bgimage2)
    elif incorrect == 3:
        bglabel.configure(image=bgimage3)
    elif incorrect == 4:
        bglabel.configure(image=bgimage4)
    elif incorrect == 5:
        bglabel.configure(image=bgimage5)
    elif incorrect == 6:
        global totalincorrect
        totalincorrect += 1
        totalincorrectlabel.configure(text="incorrect: {0}".format(totalincorrect))
        word[0] = word[0].upper()
        wordlabel.configure(text=''.join(word))
        bglabel.configure(image=bgimage6)
        letterguess.configure(state='readonly')
        mixer.music.stop()
        losts.play()
        state = False

    for l in wordlabellist:
        if (l != '_ '):
            score += 1
    if (score == len(wordlabellist)):
        note.configure(text="meh, you guessed 'em anyways, no real skill...")
        mixer.music.stop()
        wons.play()
        state = False
        letterguess.configure(state='readonly')
        global totalscore
        totalscore += 1
        totalscorelabel.configure(text="score: {0}".format(totalscore))
        
def timer():
    totaltime = 86
    global currenttime
    global state
    if (state):
        if currenttime == totaltime:
            word[0] = word[0].upper()
            wordlabel.configure(text=''.join(word))
            bglabel.configure(image=bgimage6)
            mixer.music.stop()
            note.configure(text="out of time :(")
            losts.play()
            letterguess.configure(state='readonly')
            state = False
        else:
            currenttime += 1
            root.after(1000, timer)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ WORDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wordlabellist = []
listofwords = ['Ruckus', 'Insurgent', 'Shenanigans', 'Flummox', 'Abyss', 'Akimbo', 'Avenue', 'Awkward', \
               'Caliph', 'Crypt', 'Cycle', 'Fjord', 'Glyph', 'Gnarly', 'Jinx', 'Jukebox', 'Kayak', 'Klutz', \
               'Onyx', 'Phlegm', 'Psyche', 'Queue', 'Rhythm', 'Twelfth', 'Wave', 'Wyvern', 'Yummy', 'Zygote']
for item in listofwords:
    if len(item) > 11:
        listofwords.remove(item)
listofwords = [x.lower() for x in listofwords]

word = ''
chooseword()
guessed = []
score = 0
incorrect = 0
totalscore = 0
totalincorrect = 0

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TKINTER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root = Tk()
root.wm_title('Trachea Tweaker')
root.geometry('{}x{}'.format(600,800))
mixer.music.play(0)
state = True
currenttime = 0
timer()

bgimage = PhotoImage(file='{0}/bg.gif'.format(sys.path[0]))
bgimage1 = PhotoImage(file='{0}/bg1.gif'.format(sys.path[0]))
bgimage2 = PhotoImage(file='{0}/bg2.gif'.format(sys.path[0]))
bgimage3 = PhotoImage(file='{0}/bg3.gif'.format(sys.path[0]))
bgimage4 = PhotoImage(file='{0}/bg4.gif'.format(sys.path[0]))
bgimage5 = PhotoImage(file='{0}/bg5.gif'.format(sys.path[0]))
bgimage6 = PhotoImage(file='{0}/bg6.gif'.format(sys.path[0]))
bglabel = Label(root, image=bgimage)
bglabel.place(x=0, y=0, relwidth=1, relheight=1)

totalscorelabel = Label(root, text="score: {0}".format(totalscore))
totalscorelabel.place(x=3, y=750, relheight=0.03, relwidth=0.18)

totalincorrectlabel = Label(root, text="incorrect: {0}".format(totalincorrect))
totalincorrectlabel.place(x=3, y=770, relheight=0.03, relwidth=0.2175)

quitbutton = Button(root, text='Quit', command=exist)
quitbutton.pack(side=BOTTOM, pady=6)

restartbutton = Button(root, text='Restart', command=restart)
restartbutton.pack(side=BOTTOM, pady=3)

note = Label(root, text="you have 'till the end of the song (1min25secs), good luck :)")
note.pack(side=BOTTOM, pady=5)

letterguess = Entry(root, bd=5, font=('Helvettica', 14))
letterguess.pack(side=BOTTOM, pady=5)
letterguess.insert(0, 'guesses go here')
letterguess.bind('<Return>', guess)
letterguess.bind('<Button-1>', clear)


wordlabel = Label(root, text="".join(wordlabellist), font=('Helvettica', 36))
wordlabel.pack(side=BOTTOM, pady=10)

root.mainloop()
