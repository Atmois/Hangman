import random, json, colorama, hashlib
#_____________________________________________________________# Variables - DO NOT CHANGE THESE WHATSOEVER, IT WILL 100% BREAK SOMETHING
run = True 
lives = 6
wordaddlist = []
entered_letters = []
#_____________________________________________________________# Functions
#==================================# Login
def login():
    global username
    while run:
        try:
            username = input("\nEnter your username: ")
            #==================================# Username Check
            if usernamecheck(username):
                password = input("Enter your password: ")
                #==================================# Password Check
                if acccheck(username, password):
                    print("Login successful!")
                    options()
                #==================================# Invalid Password
                else:
                    print("\n\033[38;5;9mInvalid password.\033[0;0m")
                    raise ValueError
            #==================================# Invalid Username
            else:
                print("\n\033[38;5;9mUsername not found.\033[0;0m")
                raise ValueError
        except ValueError:
            pass
#==================================# Play the Game
def play():
    global lives
    file = open("wordsto.txt", "r")
    data = file.read()
    wordlist = data.split("\n")
    file.close()
    selectedword = random.choice(wordlist)
    answer = "_" * len(selectedword) # Output
    while run:
        try:            
            #==================================# Info
            showlives(lives)
            print("\nYou have", lives, "lives!")
            print("Letters you have guessed:", sorted(entered_letters))
            print("Your current guess is:", answer,"\n")
            #==================================# Enter Letter
            letterchoice = input("Please input a letter in the English Alphabet to guess: ")
            letterchoice = letterchoice.lower()
            lettersonlyletterchoice = letterchoice.isalpha()
            #==================================# Already Entered Letter
            if letterchoice in entered_letters:
                print("\033[38;5;9mThis letter has already been entered.\033[0;0m")
                raise ValueError          
            elif lettersonlyletterchoice == False:
                print("\033[38;5;9mThis is not a letter in the English Alphabet.\033[0;0m")
                raise ValueError
            #==================================# More than 1 letter long 
            if len(letterchoice) > 1:
                print("\033[38;5;9mPlease enter a singular letter.\033[0;0m")
                raise ValueError          
            #==================================# Check for the letter
            elif any(ltr in letterchoice for ltr in selectedword):
                entered_letters.append(letterchoice)
                found = []
                #==================================# Update answer variable
                for x in range(0, len(selectedword)):
                    if selectedword[x] == letterchoice:
                        found.append(x)
                    for x in range(0,len(found)):
                        answer = list(answer)
                        y = found[x]
                        answer[y] = selectedword[y]
                        answer = ''.join(answer)
                print("\033[38;5;220mThis letter is in the word!\033[0;0m")    
            #==================================# Wrong Letter                  
            else:
                entered_letters.append(letterchoice)
                lives = lives - 1
                print("\n\033[38;5;220mThis letter is not in the word. You have lost a life.\033[0;0m")
            #==================================# Player Lose
            if lives == 0:
                print("\n\033[38;5;220mGame over. The word was", selectedword + ".\033[0;0m\n")
                showlives(lives)
                lives == 6      
                options()
            #==================================# Player Win
            elif '_' not in answer:
                print("\n\033[38;5;10mYou won.\033[0;0m")
                score = lives
                addlb(username, int(score))
                options()      
        except ValueError:
            pass
#==================================# Add User to leaderboard
def addlb(name, score):
    with open('leaderboard.json', 'r+') as lb:
        data = json.load(lb)
        leaderboard = data['lb']
        #==================================# Checks if Username Exists
        for entry in leaderboard:
            if entry["name"] == name:
                if score > entry["score"]:
                    entry["score"] = score
                break
        #==================================# Adds score if it doesn't
        else:
            leaderboard.append({"name": name, "score": score})
        data['lb'] = leaderboard
        lb.seek(0)
        json.dump(data, lb, indent=2)
        lb.truncate()
        options()
#==================================# Load, Sort & Print Leaderboard
def loadlb():
  with open('leaderboard.json', 'r+') as lb:
    data = json.load(lb)
    data['lb'] = sorted(data['lb'], key=lambda x: x['score'], reverse=True) # What actually sorts it
    lb.seek(0)  
    json.dump(data, lb, indent=2)
    lb.truncate() 
    with open('leaderboard.json') as lb:
        data = json.load(lb)
        print('\nScore | Name')
        for p in data['lb']:
            print(p['score'], '|', p['name']) # Prints Leaderboard
    options()
#==================================# Check if Username Exists
def usernamecheck(username):
    with open("logins.json", "r") as file:
        logins = json.load(file)
    for entry in logins:
        decoded_username = entry["username"]
        if username == decoded_username:
            return True
    return False
#==================================# Check if Account Exists
def acccheck(username, password):
    with open("logins.json", "r") as file:
        logins = json.load(file)
    for entry in logins:
        decoded_username = entry["username"]
        decoded_password = entry["password"]
        if decoded_username == username and hashlib.sha256(password.encode()).hexdigest() == decoded_password:
            return True
    return False    
#==================================# Add New Login
def newuser():
    while run:
        try:
            #==================================# Asks for new Username
            with open("logins.json", "r") as file:
                logins = json.load(file)
            username = input("\nNew Username: ")
            #==================================# Checks if username already exists
            for entry in logins:
                if entry["username"] == username:
                    print("\033[38;5;9mUsername already exists.\033[0;0m")
                    raise ValueError
            #==================================# Asks for and Checks Password Strength
            while run:
                try:
                    #==================================# Variables
                    strength = 0
                    onlyletters = False
                    onlylower = False
                    onlynumbers = False
                    onlyupper = False
                    toolong = False
                    tooshort = False
                    #==================================# Password Checks
                    password = input("Password: ")
                    onlyletters = password.isalpha() # Only Letters
                    onlynumbers = password.isnumeric() # Only Numbers
                    onlyupper = password.isupper() # Only Upper Case
                    onlylower = password.islower() # Only Lower Case
                    if len(password) < 6: # Not too Short
                        tooshort = True
                        toolong = False
                    elif len(password) > 12: # Not too Long
                        toolong = True 
                        tooshort = False
                    else:
                        tooshort = False
                        toolong = False
                    #==================================# Length Errors
                    if toolong == True:
                        print("\033[38;5;9mPassword is over 12 characters, please try again.\033[0;0m\n")
                        raise ValueError
                    elif tooshort == True:
                        print("\033[38;5;9mPassword is under 6 characters, please try again.\033[0;0m\n")
                        raise ValueError      
                    if onlylower == False and onlyupper == False:
                        strength = strength + 1
                    if onlyletters == False and onlynumbers == False:
                        strength = strength + 1
                    if strength == 0:
                        #==================================# Strength Confirmation
                        carryon = input("\033[38;5;9mYour password is weak, would you like to continue (Y/N): \033[0;0m")
                    elif strength == 1:
                        carryon = input("\033[38;5;220mYour password is medium strength, would you like to continue (Y/N): \033[0;0m")
                    elif strength == 2:
                        carryon = input("\033[38;5;10mYour password is strong, would you like to continue (Y/N): \033[0;0m")
                    carryon = carryon.lower()
                    if carryon == "n":
                        print("")
                        raise ValueError
                    #==================================# Continue
                    elif carryon == "y":
                        break
                    else:
                        print("\033[38;5;9mPlease enter Y or N.\033[0;0m\n")
                        raise ValueError
                except ValueError:
                    pass
            #==================================# Saves new Login
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            new_entry = {"username": username, "password": password_hash}
            logins.append(new_entry)
            with open('logins.json', 'w') as file:
                json.dump(logins, file, indent=4)
            acc()
        except ValueError:
            pass
#==================================# View Word List
def viewwords():
    file = open("wordsto.txt", "r")
    data = file.read()
    wordlist = data.split("\n")
    wordcount = len(wordlist)
    print("\nThere are", wordcount, "entries in the database.")
    print("\n", wordlist)
    editoptions()
#==================================# Visual Life Output
def showlives(lives):
    if lives == 0:
        print("  +---+")
        print("  |   |")
        print("  O   |")
        print(" /|\  |")
        print(" / \  |")
        print("=======")        
    elif lives == 1:
        print("\n  +---+")
        print("  |   |")
        print("  O   |")
        print("      |")
        print("      |")
        print("=======")
    elif lives == 2:
        print("\n  +---+")
        print("  |   |")
        print("      |")
        print("      |")
        print("      |")
        print("=======")                  
    elif lives == 3:                          
        print("\n  +---+")
        print("      |")
        print("      |")
        print("      |")
        print("      |")
        print("=======")                    
    elif lives == 4:  
        print("\n      +")
        print("      |")
        print("      |")
        print("      |")
        print("      |")
        print("=======")
    elif lives == 5:
        print("\n       ")
        print("       ")
        print("       ")
        print("       ")
        print("       ")
        print("=======")
    elif lives == 6:
        pass
#==================================# Remove word from database
def removeword():
    removeword = input("\nPlease select a word to remove: ")
    removeword = removeword.lower()
    #==================================# Find word in database + find line number
    with open('wordsto.txt', 'r') as file:
        lines = file.readlines()
    existingword = False
    updated_lines = []
    for line in lines:
        if removeword not in line:
            updated_lines.append(line)
        else:
            existingword = True
    if existingword:
        with open('wordsto.txt', 'w') as file:
            file.writelines(updated_lines) # Removes word
        print("\033[38;5;10m The word", removeword, "has been removed from the database.\033[0;0m")
    else:
        print("\033[38;5;9mThe word", removeword, "is not in the database.\033[0;0m")
    editoptions()
#==================================# Add word to database
def addword():
    while run:
        try:
            newword = input("\nPlease enter a word that is less than 24 characters to be entered into the database: ")
            newword = newword.lower()
            newwordlencheck = len(newword)
            lettersonlycheck = newword.isalpha()
            #==================================# Duplicate Check
            file = open("wordsto.txt", "r")
            data = file.read()
            wordlist = data.split("\n")
            file.close()
            if newword in wordlist:
                existingword = True
            else:
                existingword = False
            #==================================# Incorrect Entry Outputs
            if newwordlencheck > 24 or newwordlencheck < 1:
                print("Please enter a word less than 24 characters long or enter a word.\033[0;0m")
                raise ValueError
            elif lettersonlycheck == False:
                print("\033[38;5;9mPlease only enter characters.\033[0;0m")
                raise ValueError
            elif existingword == True:
                print("\033[38;5;9mThis word already exists in the database.\033[0;0m")
                existingword = False
                raise ValueError
            else:
                wordaddlist.append(newword)
                with open('wordsto.txt', 'a') as file:
                    for item in wordaddlist:
                        file.write("\n" + item)
                        file.close()
                    print('Done')
                    editoptions()
        except ValueError:
            print("")
#==================================# Login or Create Account
def acc():
    accoption = input("\nLogin (Login) or Create Account (Create): ")
    accoption = accoption.lower()
    while run:
        try:
            if accoption == "login":
                login()
            elif accoption == "create":
                newuser()
            else:
                raise ValueError
        except ValueError:
            print("\033[38;5;9mInvalid Option\033[0;0m")
            acc()
#==================================# Mode Selector
def options():
    while run:    
        try:
            mode = input("\nPlease select if you would like play the game (Play), see the Leaderboard (LB), edit the list of words (Edit) or end the code (End): ") 
            mode = mode.lower() 
            #_____________________________________________________________# Editmode Selector
            if mode == "edit": 
                editoptions()
            elif mode == "play":
                play()
            elif mode == "lb":
                loadlb()
            elif mode == "end":
                quit()
            else:
                raise ValueError
        except ValueError:
            print("\033[38;5;9mPlease enter a valid mode.\033[0;0m")
#==================================# Edit Mode Selector
def editoptions():
    while run:
        try:
            editmode = input("\nPlease select what you would like to edit, to add a entry (Add), to remove a entry (Remove), go to main menu (Menu) or to view the list (View): ") 
            editmode = editmode.lower()
            if editmode == "add":
                addword()
            elif editmode == "remove":
                removeword()
            elif editmode == "view":
                viewwords()
            elif editmode == 'menu':
                options()
            else:
                raise ValueError
        except ValueError:
            print("\033[38;5;9mPlease enter a valid Edit Mode.\033[0;0m")
#_____________________________________________________________# What Starts the Code
acc()