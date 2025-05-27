import tkinter as tk
import random
import math
import time

# Main class for the game
class DungeonGame:
    def __init__(self, root):
        # Initialize the main window and widgets
        # Images:
        self.image = tk.PhotoImage()
        # The rest:
        self.root = root
        self.root.title("dungeon BWAHHHHH")
        self.text = tk.Text(root, height=35, width=100, state='disabled', wrap='word')
        self.text.pack(padx=10, pady=10)
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
        self.submit_btn = tk.Button(root, text="Submit", command=self.on_submit)
        self.submit_btn.pack(side=tk.LEFT, padx=10, pady=(0,10))
        self.input_callback = None
        self.root.bind('<Return>', lambda event: self.on_submit())
        self.after_id = None

        # Start the game
        self.reset_game()
        self.start_game()

    def reset_game(self):
        # Reset all game variables to their initial state when game starts/restarts
        self.continuequestion = "keep going"
        self.score = 0
        self.hiddenscore = 1
        self.character = "mystery person"
        self.hp = 100
        self.maxhp = 100
        self.end = 0.00
        self.atk = 1
        self.statlist = ["hp", "end", "atk"]
        self.currentweapon = {"name":"hands", "dmg":10}
        self.currentshield = {"name":"arms", "end":0.03}
        self.inventory = {1:"", 2:"", 3:""}
        self.winchoice = ""
        self.lastevent = "event"
        self.healcounter = 0
        self.enemylist = ["slime", "skeleton", "zombie", "cave bat", "cave dweller"]
        self.enemylist2 = ["dungeon marauder", "dungeon archer", "wolf", "big slime", "evil dungeon delver"]
        self.adjlist = [
            "glittering", "worn", "battle-scarred", "damp", "brand-new", "steel", "silver", 
            "mysterious-looking", "comically large", "comically small", "silly", "paladin's", "the dragon of dorima's"
        ]
        # Character descriptions to be printed at the beginning of the game
        self.storydict = {
            "angry":{
                "character":"angry",
                "story":"brute, good at fighting but has little defense",
                "atk":1.75,
                "end":0.15,
                "weapon":{"name":"heavy handaxe", "dmg":50},
                "shield":{"name":"arms", "end":0.01},
                "inventory":{1:"small attack potion", 2:"", 3:""}
            },
            "tanky":{
                "character":"tanky",
                "story":"all-rounder, high defense and OK attack, but not the best at either",
                "atk":1.50,
                "end":0.30,
                "weapon":{"name":"arming sword", "dmg":35},
                "shield":{"name":"round shield", "end":0.15},
                "inventory":{1:"medium hp potion", 2:"", 3:""}
            },
            "sneaky":{
                "character":"sneaky",
                "story":"starts with low defense and a bad weapon, but has high potential",
                "atk":2,
                "end":0.05,
                "weapon":{"name":"small dagger", "dmg":25},
                "shield":{"name":"arm braces", "end":0.10},
                "inventory":{1:"medium attack potion", 2:"", 3:""}
            }
        }
        # Item definitions
        self.items = {
            "atk":{
                "small attack potion":0.50,
                "medium attack potion":1,
                "large attack potion":2,
            },
            "end":{
                "small endurance potion":0.15,
                "medium endurance potion":0.30,
                "large endurance potion":0.50,
            },
            "hp":{
                "small hp potion":0.25,
                "medium hp potion":0.6,
                "large hp potion":0.9
            }  
        }
        
        # vvvv Makes random items for good events vvvv
    def statrollsword(self):
        return min(random.randint(40,300), random.randint(1,300), random.randint(1,300))
    def statrollshield(self):
        return min(random.randint(1000,7000)/100, random.randint(1000,7000)/100, random.randint(1000,7000)/100)
    
    def positiveevntlist(self):
        # List of positive event text
        return {
            1:{"text":"\n----------------------------------------\nYippee! (positive event)\nA little goblin holding a tattered bag over it's shoulder skitters past, \nand a sword falls out of the bag. Pick it up? (y/n)", "effect":"dmg", "change":1},
            2:{"text":"\n----------------------------------------\nYippee! (positive event)\nAs you continue, someone carrying a heavy load passes by, \nand asks you to please take something. Help them out and take a shield? (y/n)", "effect":"end", "change":0.01}, 
            3:{"text":"\n----------------------------------------\nYippee! (positive event)\nEntering a shrine, you happen across a statue sculpted after... \nyou? It is holding a sword. Take it? (y/n)", "effect":"dmg", "change":1}, 
            4:{"text":"\n----------------------------------------\nYippee! (positive event)\nYou happen across a pedestal holding a shield. Take it? (y/n)", "effect":"end", "change":0.01},
            5:{"text":"\n----------------------------------------\nYippee! (positive event)\nA small sack lays at your feet. You open it and it contains a sword. Take it? (y/n)", "effect":"dmg", "change":1}
        }
    def negativeevntlist(self):
        # List of negative event text
        return {
            1:{"text":"\n----------------------------------------\nWomp womp.. (negative event)\nYou trip. Idiot.", "effect":"end", "change":-0.03}, 
            2:{"text":"\n----------------------------------------\nWomp womp.. (negative event)\nYou hear disembodied murmuring all around you, whispering discouraging words.", "effect":"atk", "change":-0.20},
            3:{"text":"\n----------------------------------------\nWomp womp.. (negative event)\nYou spot a tall, silhouetted, skinny creature. It stares, so you stare back. \nIt disappears for the blink of an eye, reappears, then sprints away. \nYour arm is now bent backwards.", "effect":"atk", "change":-0.60}, 
            4:{"text":"\n----------------------------------------\nWomp womp.. (negative event)\nA stinging headache hits you, and the pain makes it hard to think!", "effect":"end", "change":-0.15},
            5:{"text":"\n----------------------------------------\nWomp womp.. (negative event)\nCramp!! That hurts....", "effect":"end", "change":-0.08},
            6:{"text":"\n----------------------------------------\nWomp womp.. (negative event)\nThe ceiling trembles, and a rock falls flat on the top of your head.", "effect":"end", "change":-0.08},
            7:{"text":"\n----------------------------------------\nWomp womp.. (negative event)\nYou pull a book from a shelf you find, and its contents detail forbidden knowledge.", "effect":"atk", "change":-0.30},
            8:{"text":"\n----------------------------------------\nWomp womp.. (negative event)\nA skeleton with no arms comes sprinting out a corner full speed, right into your swinging arm, and falls apart.", "effect":"atk", "change":-0.20}
        }
        
        # Some unfinished stuff
        self.characterchoice = None

        # vvvvvvvvvvv Various print functions for diff delays vvvvvvvvvvvv  
    def printnosleep(self, *args, end='\n'):
        # Print text to the game window without delay
        self.text.config(state='normal')
        self.text.insert(tk.END, ' '.join(str(a) for a in args) + end)
        self.text.see(tk.END)
        self.text.config(state='disabled')

    def printshortsleep(self, *args, end='\n'):
        # Print text to the game window with a delay for effect
        self.text.config(state='normal')
        self.text.insert(tk.END, ' '.join(str(a) for a in args) + end)
        self.text.see(tk.END)
        self.text.config(state='disabled')
        self.root.update()  # Ensure the GUI updates before sleeping
        time.sleep(0.2)

    def print(self, *args, end='\n'):
        # Print text to the game window with a delay for effect
        self.text.config(state='normal')
        self.text.insert(tk.END, ' '.join(str(a) for a in args) + end)
        self.text.see(tk.END)
        self.text.config(state='disabled')
        self.root.update()  # Ensure the GUI updates before sleeping
        time.sleep(0.75)      

    def printlongsleep(self, *args, end='\n'):
        # Print text to the game window with a delay for effect
        self.text.config(state='normal')
        self.text.insert(tk.END, ' '.join(str(a) for a in args) + end)
        self.text.see(tk.END)
        self.text.config(state='disabled')
        self.root.update()
        time.sleep(2)

    def input(self, prompt, callback):
        # Prompt the user for input and set the callback for when they submit (button stuff)
        self.print(prompt, end='')
        self.input_callback = callback
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def on_submit(self):
        # Handles submit button and stuff even more
        if self.input_callback:
            value = self.entry.get()
            self.entry.delete(0, tk.END)
            cb = self.input_callback
            self.input_callback = None
            cb(value)

    def start_game(self):
        # Display the introduction and start the game (yes it looks ugly if i don't do it like this it doesn't print right)
        self.print("""\nHere's the run-down:\n
vvv STATS vvv
HP: If this number gets to 0, game over!
ATK: Attack, augments weapon damage
END: Endurance, helps negate enemy damage\n\n
vvv WEAPON/SHIELD vvv
WEAPON: What HURTS your enemy! Augmented by your ATK stat
SHIELD: Its endurance is added to your endurance stat directly (endurance caps at 99%)\n\n
vvv ITEMS vvv
You might find them after a battle, and you get to use 1 per turn before attacking (or running)\n\n
vvv GOAL vvv
Reach the BOTTOM of the DUNGEON!!
==================================================================================================       
Enemies will get stronger the further you go. Every 3 battles you win your HP is fully restored.
Good luck!\n""")
        self.input("Understood? (y/n) >", self.understood_input)

    def understood_input(self, value):
        if value != "y":
            self.input("UNDERSTOOD?? (y/n) >", self.understood_input)
        else:
            self.choose_character()

    def choose_character(self):
        # Show all the different character options
        self.print("\n\n-------------------Choose a character!-------------------\n")
        self.printlongsleep("======tanky======\n " + self.storydict['tanky']['story'], "\n----------------\n",
            "ATK", self.storydict['tanky']['atk'], "\n",
            "END", self.storydict['tanky']['end']*100, "%\n---------------\n",
            "Weapon:", self.storydict['tanky']['weapon']['name'], "\n",
            "Weapon damage:", self.storydict['tanky']['weapon']['dmg'], "\n---------------\n",
            "Shield:", self.storydict['tanky']['shield']['name'], "\n",
            "Shield endurance:", self.storydict['tanky']['shield']['end']*100, "%\n",
            "Starts with a medium HP potion\n\n"
            "CLASS PERK: When an enemy has more attack than your weapon, 30% chance to PARRY an attack\n\n")
        self.printlongsleep(
            "======angry======\n" + self.storydict['angry']['story'], "\n----------------\n",
            "ATK", self.storydict['angry']['atk'], "\n",
            "END", self.storydict['angry']['end']*100, "%\n---------------\n",
            "Weapon:", self.storydict['angry']['weapon']['name'], "\n",
            "Weapon damage:", self.storydict['angry']['weapon']['dmg'], "\n---------------\n",
            "Shield:", self.storydict['angry']['shield']['name'], "\n",
            "Shield endurance:", self.storydict['angry']['shield']['end']*100, "%\n", 
            "Starts with a small attack potion\n\n"
            "CLASS PERK: Any ATK increases after battle are doubled, and ATK potions have a higher impact\n\n")
        self.printlongsleep(
            "======sneaky======\n" + self.storydict['sneaky']['story'], "\n----------------\n",
            "ATK", self.storydict['sneaky']['atk'], "\n",
            "END", self.storydict['sneaky']['end']*100, "%\n---------------\n",
            "Weapon:", self.storydict['sneaky']['weapon']['name'], "\n",
            "Weapon damage:", self.storydict['sneaky']['weapon']['dmg'], "\n---------------\n",
            "Shield:", self.storydict['sneaky']['shield']['name'], "\n",
            "Shield endurance:", self.storydict['sneaky']['shield']['end']*100, "%\n"
            "Starts with a medium attack potion\n\n"
            "CLASS PERK: Higher chance to run away\n\n")
        self.input(">tanky, >angry, or >sneaky? \n(psst, try >None)\n", self.character_input)

    def character_input(self, value):
        # Assigns stats according to the character the player chose
        value = value.lower()
        if value == "sneaky":
            self.characterchoice = "sneaky"
            self.character = "sneaky"
            self.atk = self.storydict['sneaky']['atk']
            self.end = self.storydict['sneaky']['end']
            self.currentweapon = self.storydict['sneaky']['weapon'].copy()
            self.currentshield = self.storydict['sneaky']['shield'].copy()
            self.inventory = self.storydict["sneaky"]["inventory"].copy()
        elif value == "angry":
            self.characterchoice = "angry"
            self.character = "angry"
            self.atk = self.storydict['angry']['atk']
            self.end = self.storydict['angry']['end']
            self.currentweapon = self.storydict['angry']['weapon'].copy()
            self.currentshield = self.storydict['angry']['shield'].copy()
            self.inventory = self.storydict["angry"]["inventory"].copy()
        elif value == "tanky":
            self.characterchoice = "tanky"
            self.character = "tanky"
            self.atk = self.storydict['tanky']['atk']
            self.end = self.storydict['tanky']['end']
            self.currentweapon = self.storydict['tanky']['weapon'].copy()
            self.currentshield = self.storydict['tanky']['shield'].copy()
            self.inventory = self.storydict["tanky"]["inventory"].copy()
        else:
            self.print("\nYou picked... no one!\nAll enemy attacks now have a 15% chance to miss, AND you run away from fights successfully more often!\nHowever, you start with NOTHING!\nThis is the INTENDED way to play!")
            self.characterchoice = "unknown"
        self.root.after(1, self.main_game_loop)

    def main_game_loop(self):
        # Prompts for the player to continue, and if they win, then give them an option to go endless or stop.
        if self.score>60 and self.winchoice != "continue":
            self.print("YOU WIN! To achieve this you must've gotten extremely lucky, so congratulations.")
            self.input("\ntype anything to end, or \"continue\" to keep going until you die... >", self.win_continue)
            return
        self.input("\nType anything to continue, or \"stats\" to view your current stats... >\n", self.handle_main_input)

    def win_continue(self, value):
        # Handle the player's choice after winning
        if value == "continue":
            self.winchoice = "continue"
            self.main_game_loop()
        else:
            self.print("Game ended.")
            self.input("Type anything to restart. >", lambda v: self.restart_game())

    def handle_main_input(self, value):
        # Handles whatever the player inputs in the main game loop, printing stats if requested.
        if value == "stats":
            self.print("\n----------------\nscore: " + str(self.score) + "\n----------------\nhp: " + str(self.hp) + "\nmax hp: " + str(self.maxhp) + "\n----------------\natk: " + str(self.atk) + "\nend: " + str((self.end%1)*100) + "%\n----------------\ncurrent weapon: " + self.currentweapon["name"] + "\ncurrent weapon dmg: " + str(self.currentweapon["dmg"]) + "\ncurrent shield: " + self.currentshield["name"] + "\ncurrent shield end: " + str((self.currentshield["end"]%1)*100)  + "%\n----------------\nSLOT 1: " + self.inventory[1] + "\nSLOT 2: " + self.inventory[2] + "\nSLOT 3: " + self.inventory[3] + "\n----------------\n")
            self.input("\nType anything to continue... >", lambda v: self.main_game_loop())
        # After, roll for either an event or an enemy encounter. If it's an event, set lastevent to "event" so it doesn't repeat.
        else:
            eventoddroll = random.randint(1, 100)
            if eventoddroll > 50:
                self.enemyroll(self.after_enemyroll)
            else:
                if self.lastevent != "event":
                    self.evnt2roll(lambda: self.set_lastevent_and_continue("event"))
                else:
                    self.enemyroll(self.after_enemyroll)

    def set_lastevent_and_continue(self, val):
        # set last event blah blah blah
        self.lastevent = val
        self.main_game_loop()

    def after_enemyroll(self, enemyresult):
        # After player wins or loses, do all of this!
        if enemyresult == "lost":
            self.print("\n:( :( :( :( :( :( :( :(\nfinal score: " + str(self.score) + "\n:( :( :( :( :( :( :( :(\n")
            self.input("try again? (y/n) >", self.try_again)
        elif enemyresult == "ran":
            self.hiddenscore += 5
            self.lastevent = "fight"
            self.main_game_loop()
        elif enemyresult == "won":
            # If player wins... improve one stat randomly, and every 15 score (3 battles), give player prompt to improve a stat majorly.
            self.healcounter += 1
            # Score will go up and make enemies harder according to progress. Score is used for printing, hiddenscore is used for actual calculations.
            self.score += 5
            self.hiddenscore += 5
            self.print("\nNew score:", str(self.score))
            statimprove = random.choice(self.statlist)
            if statimprove == "atk":
                self.atk += round(min(round(random.uniform(0.05, 0.90), 2), round(random.uniform(0.05, 0.90), 2), round(random.uniform(0.05, 0.90), 2)), 2)
                self.atk = round(self.atk, 2)
                self.print("\n**************************\natk improved. new atk:", str(round(self.atk, 2)), "\n**************************\n-------------\n")
            elif statimprove == "end":
                self.end += round(min(round(random.uniform(0.02, 0.15), 2), round(random.uniform(0.02, 0.15), 2)), 2)
                self.end = round(self.end, 2)
                self.print("\n**************************\nend improved. new end:", str((round(self.end, 2))*100), "%\n**************************\n-------------\n")
            elif statimprove == "hp":
                hpgain = min(random.randint(20,60), random.randint(20,60))
                self.maxhp = self.maxhp + hpgain
                self.hp = self.hp + hpgain
                self.print("\n**************************\nhp improved. new max hp:", str(self.maxhp), "\n**************************\n-------------\n")
            if self.healcounter%3 == 0:
                self.print("HP RESTORED TO MAX!")
                self.hp = self.maxhp
                self.print("Pick a stat to majorly improve! You will only get this chance THREE times!\n1: atk +0.5 \n2: end +0.15\n3: hp +50")
                self.input(">", self.statchoice_input)
                return
            # Chance to find a random item after battle
            if random.randint(1,100) > 65:
                invnum = 1
                while invnum <= 3:
                    if self.inventory.get(invnum) == "":
                        strtemp = random.choice(["end", "atk", "hp"])
                        if strtemp == "atk":
                            self.inventory[invnum] = random.choice(list(self.items["atk"]))
                        elif strtemp == "end":
                            self.inventory[invnum] = random.choice(list(self.items["end"]))
                        else:
                            self.inventory[invnum] = random.choice(list(self.items["hp"]))
                        self.print("+++  YOU FOUND A", self.inventory.get(invnum).upper(), "! +++")
                        break
                    else:
                        invnum += 1
            self.main_game_loop()

    def statchoice_input(self, value):
        # Improve chosen stat every 3 battles
        try:
            statchoice = int(value)
        except:
            self.input(">", self.statchoice_input)
            return
        if statchoice == 1:
            self.atk += 0.5
            self.print("atk improved.")
        elif statchoice == 2:
            if self.end > 0.90:
                self.end = 0.99
            else:
                self.end += 0.10
            self.print("end improved.")
        elif statchoice == 3:
            self.maxhp += 50
            self.hp = self.maxhp
            self.print("hp improved.")
        self.main_game_loop()

    def try_again(self, value):
        # Try again... or not?
        while value != "y" and value != "n":
            self.input("do you want to TRY AGAIN?? (y/n) >", self.try_again)
            return
        if value == "y":
            self.reset_game()
            self.text.config(state='normal')
            self.text.delete(1.0, tk.END)
            self.text.config(state='disabled')
            self.start_game()
        else:
            self.print("Game ended.")
            self.input("Type anything to restart. >", lambda v: self.restart_game())

    def restart_game(self):
        # Restart the game from scratch
        self.reset_game()
        self.text.config(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.config(state='disabled')
        self.start_game()

    # --- GAME LOGIC FUNCTIONS ---

    def evnt2roll(self, callback):
        # Handle random events (positive or negative)
        event2 = random.randint(1,50)
        if event2 >= 20:
            eventchosen = self.positiveevntlist()[random.randint(1,5)]
            if "dmg" in eventchosen["effect"]:
                eventchosen["change"] = self.statrollsword()
                prompt = eventchosen["text"] + "\nIts damage:  " + str(eventchosen["change"]) + "\n Your current " + self.currentweapon["name"] + "'s damage: " + str(self.currentweapon["dmg"]) + "\n----------------------------------------\n>"
            elif eventchosen["effect"] == "end":
                eventchosen["change"] = round(0.01*self.statrollshield(), 2)
                prompt = eventchosen["text"] + "\nIts endurance:  " + str((eventchosen["change"]%1)*100) + "%\n Your current " + self.currentshield["name"] + "'s endurance: " + str(self.currentshield["end"]*100) + "%\n----------------------------------------\n>"
            self.input(prompt, lambda choose: self.evnt2roll_choice(choose, eventchosen, callback))
        else:
            eventchosen = self.negativeevntlist()[random.randint(1,8)]
            if eventchosen["effect"] == "atk":
                eventchosen["change"] = round((eventchosen["change"] * self.score)/20, 2)
                self.print(eventchosen["text"], "\n" + eventchosen["effect"], eventchosen["change"] )
                self.atk = round(self.atk+eventchosen["change"], 2)
                if self.atk < 1:
                    self.atk = 1
                self.print("new atk: " + str(self.atk) + "\n----------------------------------------\n")
            elif eventchosen["effect"] == "end":
                eventchosen["change"] = round((eventchosen["change"] * self.score)/15, 2)
                self.print(eventchosen["text"], "\n" + eventchosen["effect"] + " " + str(eventchosen["change"]*100) + "%")
                self.end = round(self.end+eventchosen["change"], 2)
                if self.end < 0.01:
                    self.end = 0.01
                self.print("new end: " + str(round((self.end*100), 2)) + "%\n----------------------------------------\n")
            self.root.after(100, callback)

    def evnt2roll_choice(self, choose, eventchosen, callback):
        # Takes or denies item from a positive event
        while choose != "y" and choose != "n":
            self.print("\npick an OPTION!!!\n")
            if eventchosen["effect"] == "dmg":
                prompt = eventchosen["text"] + "\nIts damage:  " + str(eventchosen["change"]) + "\n Your current " + self.currentweapon["name"] + "'s damage: " + str(self.currentweapon["dmg"]) + "\n----------------------------------------\n>"
            elif eventchosen["effect"] == "end":
                prompt = eventchosen["text"] + "\nIts endurance:  " + str(((eventchosen["change"])%1)*100) + "%\n Your current " + self.currentshield["name"] + "'s endurance: " + str(self.currentshield["end"]*100) + "%\n----------------------------------------\n>"
            self.input(prompt, lambda c: self.evnt2roll_choice(c, eventchosen, callback))
            return
        if choose == "y" and eventchosen["effect"] == "dmg":
            self.currentweapon["name"] = random.choice(self.adjlist) + " sword"
            self.print("You got a", self.currentweapon["name"])
            self.currentweapon["dmg"] = eventchosen["change"]
        elif choose == "y" and eventchosen["effect"] == "end":
            self.currentshield["name"] = random.choice(self.adjlist) + " shield"
            self.print("You got a", self.currentshield["name"])
            self.currentshield["end"] = eventchosen["change"]
        elif choose == "n":
            self.print("\nYou didn't take the item.\n")
        self.root.after(100, callback)

    def enemyroll(self, callback):
        # Generate an enemy encounter based on hiddenscore
        if self.hiddenscore > 25:
            self.printlongsleep("\n==========================\nYou come across a " + random.choice(self.enemylist2) + "!\n==========================")
            enemyatk = round(float(random.randrange(151,201))/100 * (self.hiddenscore/40), 2)
            enemyend = round(float(random.randrange(31,60))/100 * (self.hiddenscore/40), 2)
            enemywep = round(random.randint(40,50) * enemyatk, 2)
            enemyhp = math.ceil(random.randint(100,120) * (self.hiddenscore/25))
        else:
            self.printlongsleep("\n==========================\nYou come across a " + random.choice(self.enemylist) + "!\n==========================")
            enemyatk = round(float(random.randrange(100,151))/100 * (self.hiddenscore/20), 2)
            enemyend = round(float(random.randrange(5,31))/75 * (self.hiddenscore/50), 2)
            enemywep = round(random.randint(40,50) * enemyatk, 2)
            enemyhp = math.ceil(random.randint(100,120) * (self.hiddenscore/15))
        if enemyend > 1:
            enemyend = 0.90
        if enemyatk < 1:
            enemyatk = 1
        self.print("dmg: " + str(round((enemywep*enemyatk), 2)) + "\nend: " + str(round((enemyend%1), 1)*100) + "%")
        self.enemy_battle(enemyhp, enemyatk, enemyend, enemywep, callback)

    def enemy_battle(self, enemyhp, enemyatk, enemyend, enemywep, callback):
        # Starts enemy encounter, and prints their stats
        self.print("-------------\nenemy hp: " + str(enemyhp))
        self.print("your hp: " + str(self.hp) + "/" + str(self.maxhp))
        self.input("\n>Fight, >Run, or use an >Item? You can also check your >Stats beforehand. >", lambda choice: self.enemy_battle_choice(choice, enemyhp, enemyatk, enemyend, enemywep, callback))

    def enemy_battle_choice(self, battlechoice, enemyhp, enemyatk, enemyend, enemywep, callback):
        # Handle the player's choice during battle
        battlechoice = battlechoice.lower()
        if battlechoice == "stats":
            self.print("\n----------------\nscore: " + str(self.score) + "\n----------------\nhp: " + str(self.hp) + "\nmax hp: " + str(self.maxhp) + "\n----------------\natk: " + str(self.atk) + "\nend: " + str((self.end%1)*100) + "%\n----------------\ncurrent weapon: " + self.currentweapon["name"] + "\ncurrent weapon dmg: " + str(self.currentweapon["dmg"]) + "\ncurrent shield: " + self.currentshield["name"] + "\ncurrent shield end: " + str((self.currentshield["end"]%1)*100)  + "%\n----------------\nSLOT 1: " + self.inventory[1] + "\nSLOT 2: " + self.inventory[2] + "\nSLOT 3: " + self.inventory[3] + "\n----------------\n")
            self.input("\nFight, Run, or use an Item? >", lambda c: self.enemy_battle_choice(c, enemyhp, enemyatk, enemyend, enemywep, callback))
            return
        while battlechoice not in ["fight", "run", "item"]:
            self.input("(Pick one of the following options given.)\n>Fight, >Run, or use an >Item? >", lambda c: self.enemy_battle_choice(c, enemyhp, enemyatk, enemyend, enemywep, callback))
            return
        if battlechoice == "item":
            self.print("\nSLOT 1: " + self.inventory[1] + "\nSLOT 2: " + self.inventory[2] + "\nSLOT 3: " + self.inventory[3])
            self.input("\n\nType the slot the item you want to use is in (1,2,3)... >", lambda slot: self.use_item(slot, enemyhp, enemyatk, enemyend, enemywep, callback))
            return
        if battlechoice == "run":
            self.print("\n>>>>>>>>>>>\nYou try to run, and...")
            if self.character == "sneaky":
                if random.randint(1,100) >= 35:
                    self.print("You ran away swiftly.\n>>>>>>>>>>>\n")
                    callback("ran")
                    return
                else:
                    self.print("Failed.\n>>>>>>>>>>>\n")
            else:
                if random.randint(1,100) >= 60:
                    self.print("You ran away.\n>>>>>>>>>>>\n")
                    callback("ran")
                    return
                else:
                    self.print("Failed.\n>>>>>>>>>>>\n")
            self.enemy_attack(enemyhp, enemyatk, enemyend, enemywep, callback)
            return
        if battlechoice == "fight":
            criticalcheck = random.randint(1, 100)
            if criticalcheck >= 90:
                critfactor = 2
                crit = True
            else:
                critfactor = 1
                crit = False
            currentattackdmg = round(self.currentweapon["dmg"]*self.atk, 2)
            finalatk = round(((currentattackdmg*(1-enemyend))*(random.randrange(8, 13)/10))*critfactor, 2)
            enemyhp = round(enemyhp - finalatk, 2)
            if enemyhp <= 0:
                self.print("\n\n-------------")
                if crit:
                    self.print("\n***CRITICAL HIT!***")
                    self.printshortsleep("\n\n          * *\n")
                    self.printshortsleep("\n          *-*\n         *   *\n          *-*\n")
                    self.printshortsleep("\\         *-*         /\n --------*   *--------\n/         *-*         \\")
                    self.printshortsleep("\n\\                     /\n\n/                     \\")
                    self.print("\n\n\n")
                    self.printlongsleep("\n>YOU ATTACK WITH *" + str(finalatk) + "* POWER!<")
                    self.printlongsleep("\nEnemy hp left: 0")
                else:
                    self.printlongsleep(">YOU ATTACK WITH " + str(finalatk) + " POWER!<")
                    self.printlongsleep("\nEnemy hp left: 0")
                self.print("-------------\nVICTORY!")
                self.lastevent = "fight"
                callback("won")
                return
            else:
                self.print("\n\n-------------")
                if crit:
                    self.print("\n***CRITICAL HIT!***")
                    self.print("\n\n          * *\n")
                    self.print("\n          *-*\n         *   *\n          *-*\n")
                    self.print("\\         *-*         /\n --------*   *--------\n/         *-*         \\")
                    self.print("\n\\                     /\n\n/                     \\")
                    self.print("\n\n\n")
                    self.printlongsleep("\n>YOU ATTACK WITH *" + str(finalatk) + "* POWER!<")
                    self.printlongsleep("\nEnemy hp left: " + str(round(enemyhp, 2)))
                else:
                    self.printlongsleep(">YOU ATTACK WITH " + str(finalatk) + " POWER!<")
                    self.printlongsleep("\nEnemy hp left: " + str(round(enemyhp, 2)))
            self.enemy_attack(enemyhp, enemyatk, enemyend, enemywep, callback)

    def use_item(self, slot, enemyhp, enemyatk, enemyend, enemywep, callback):
        # Handle using an item from the inventory
        try:
            itemchoice = int(slot)
        except:
            self.input("\n\nType the slot the item you want to use is in (1,2,3)... >", lambda s: self.use_item(s, enemyhp, enemyatk, enemyend, enemywep, callback))
            return
        if self.inventory[itemchoice] == "":
            self.print("NOTHING buffed. Empty slot chosen.")
        else:
            catcount = 0
            while catcount <= 2:
                if catcount == 0:
                    for potion in self.items["atk"]:
                        if potion == self.inventory[itemchoice]:
                            if self.characterchoice == "angry":
                                self.atk += 2*(self.items.get("atk").get(potion))
                            else:
                                self.atk += self.items.get("atk").get(potion)
                            self.inventory[itemchoice] = ""
                            self.print("\n^^^^ ATTACK BUFFED ^^^^\nNEW ATK: " + str(self.atk) + "\n")
                elif catcount == 1:
                    for potion in self.items["end"]:
                        if potion == self.inventory[itemchoice]:
                            if self.end + (self.items.get("end").get(potion)) > 0.99:
                                self.end = 0.99
                                self.inventory[itemchoice] = ""
                                self.print("^^^^ ENDURANCE BUFFED TO MAX! ^^^^\n")
                            else:
                                self.end += self.items.get("end").get(potion)
                                self.inventory[itemchoice] = ""
                                self.print("^^^^ ENDURANCE BUFFED ^^^^\nNEW END: " + str(self.end*100) + "%\n")
                elif catcount == 2:
                    for potion in self.items["hp"]:
                        if potion == self.inventory[itemchoice]:
                            self.hp = self.maxhp * (self.items.get("hp").get(potion))
                            if self.hp > self.maxhp:
                                self.hp = self.maxhp
                            self.inventory[itemchoice] = ""
                            self.print("^^^^ HEALTH RESTORED ^^^^\nNEW HP: " + str(self.hp) + "/" + str(self.maxhp) + "\n")
                catcount += 1
        self.input(">Fight or >Run? >", lambda c: self.enemy_battle_choice(c, enemyhp, enemyatk, enemyend, enemywep, callback))

    def enemy_attack(self, enemyhp, enemyatk, enemyend, enemywep, callback):
        # Handle the enemy's attack phase
        enemycurrentattackdmg = enemywep*enemyatk
        combinedend = self.end+self.currentshield["end"]
        if combinedend > 0.99:
            combinedend = 0.99
        finalenemyatk = round((enemycurrentattackdmg*(1-combinedend))*(random.randint(8, 12)/10), 2)
        miss = False
        parry = False
        if self.characterchoice not in ["tanky", "sneaky", "angry"]:
            if (random.randint(1,100) <= 15):
                miss = True
                finalenemyatk = 0
        if self.characterchoice == "tanky" and enemywep > self.currentweapon["dmg"]:
            if random.randint(1,100) <= 30:
                parry = True
                finalenemyatk = 0
        else:
            parry = False
        self.hp = round(self.hp-finalenemyatk, 2)
        if self.hp <= 0:
            self.print(">YOU'RE HIT WITH " + str(finalenemyatk) + " POWER!<\nyour hp: " + str(self.hp))
            self.print("\nGame over.")
            callback("lost")
            return
        else:
            if miss == True:
                self.print(">>>ENEMY ATTACK EVADED>>>\n-------------\n")
            elif parry == True:
                self.print("/*\\PARRY/*\\\n-------------\n")
            else:
                self.print(">YOU'RE HIT WITH " + str(finalenemyatk) + " POWER!<\nyour hp: " + str(self.hp) + "\n-------------\n")
            self.enemy_battle(enemyhp, enemyatk, enemyend, enemywep, callback)

# Start the game if this file is run directly
if __name__ == "__main__":
    root = tk.Tk()
    game = DungeonGame(root)
    root.mainloop()