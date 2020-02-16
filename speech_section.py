### IMPORT ###
import speech_recognition as sr
import numpy as np
import time
import pyttsx3
from read_recipe import tokenizer
import os

cwd = os.getcwd()

### PARAMETERS ###
dB_threshold = 10000  # decibel threshold
t_wait = 50    # in seconds
idle = 1000   # maximum wait time until hearing wake_word
### HELPER FUNCTIONS ###

def listen_command(threshold=dB_threshold, t_timeout=t_wait):
    """ () -> str or False
    Return the command the program listens. Return False if failed to listen/understand.
    """
    r = sr.Recognizer()
    #r.dynamic_energy_threshold = threshold    # high threshold so that program only responds to large voice
    print("Listening...")
    # starts listening once threshold reached -> stops listening when quiet
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        repeat = True
        while repeat:
            try:
                audio = r.listen(source, timeout=t_timeout)
                repeat = False
            except WaitTimeoutError:
                pass
    try:
        return r.recognize_google(audio).lower()
    except sr.UnknownValueError or sr.RequestError:
        return False


def process_command(command):
    words = np.array(command.split(' '))
    ident = ''
    action = 0
    if 'read' in words or 'recipe' in words:
        #action 1 means read the recipe
        action = 1
        ind = np.where(words == 'recipe')[0][0]
        if ind < len(words)-1:
            L_words = words.tolist()
            ident = '_'.join(L_words[ind+1:])
    elif 'all' in words and 'ingredients' in words:
        # action 1.5: read all ingredients
        action = 1.5
    elif 'next' in words:
        #action 2 means read the instruction
        action = 2
    elif 'stop' in words:
        #action 3 means stop
        action = 3
    elif 'repeat' in words:
        #action 4 means repeat recipe or instruction
        action = 4
    elif 'how' in words and ('many' in words or 'much' in words):
        #fetch the ingredient
        if 'many' in words: ind = np.where(words == 'many')[0]
        else: ind = np.where(words == 'much')[0]
        if ind <= len(words):
            ident = words[ind+1][0]
        action = 5
    else:
        #action 6 means dont understand - help the user with instructions
        action = 6
    return action, ident


def listen(wake_word, t_wait=idle):
    waiting = True
    start = time.time()    
    while waiting and time.time()-start < t_wait:
        words = str(listen_command()).split(' ')
        if wake_word in words:
            waiting = False
    return True

### MAIN FUNCTION ###

def activate(wake_word):
    
    
    image_folder = 'Images_recipes'
    path_folder=os.path.join(cwd,image_folder)
    
    recipe_list=[os.path.basename(item[0]) for item in os.walk(path_folder)]
    print(recipe_list)
    
    
    
    
    active = listen(wake_word)
    engine = pyttsx3.init()
    #machine need to tell user what to do
    welcome = 'what is up'
    engine.say(welcome)
    engine.runAndWait()
    #speak the first instruction
    recipe_found = False    # error-proof: if no recipe is mentioned
    did_all_ingredients = False 
    while active:
        command = str(listen_command())
        print('Command: '+ command)
        action, ident = process_command(command)
        if action != 1 and not recipe_found:
            engine.say('which recipe again?')
            engine.runAndWait()
        #action 1: read the recipe
        else:
            if action == 1:
                did_all_ingredients = False
                if ident == '' or ident not in recipe_list: # no recipe indicated in the instruction
                    engine.say('recipe not found, try again')
                    engine.runAndWait()
                else:
                    # now, recipe is provided: identify the relevant instructions & ingredients
                    ingredient_itr = 0
                    instruction_itr = 0
                    ingredients, instructions = tokenizer(ident)
                    #instructions = instruction_book[ident] # this is a list of instructions
                    #ingredients = ingredient_book[ident]   # this is a dictionary of ingredients
                    recipe_found = True
                    # make a list of ingredient keys
                    L_ingredient_key = [*ingredients]
                    #speak the ingredients
                    key = L_ingredient_key[ingredient_itr]
                    engine.say(key+','+ingredients[key])
                    ingredient_itr += 1
                    engine.runAndWait()
            if action == 1.5:
                did_all_ingredients = True
                for key in L_ingredient_key:
                    engine.say(key+','+ingredients[key])
                    engine.runAndWait()
                ingredient_itr = len(ingredients.keys()) + 1
            if action == 2:
                did_all_ingredients = False
                if ingredient_itr < len(ingredients.keys()):
                    key = L_ingredient_key[ingredient_itr]
                    engine.say(key+','+ingredients[key])
                    engine.runAndWait()
                    ingredient_itr += 1
                elif instruction_itr < len(instructions):
                    engine.say(instructions[instruction_itr])
                    engine.runAndWait()
                    instruction_itr += 1
                else:
                    farewell = 'you done brother'
                    engine.say(farewell)
                    engine.runAndWait()
                    active = False
            elif action == 3:
                engine.say('Stopped')
                engine.runAndWait()
                if listen(wake_word):
                    engine.say('I am back')
                    engine.runAndWait()
            elif action == 4:
                # previously asked for all ingredients
                if did_all_ingredients:
                    for key in L_ingredient_key:
                        engine.say(key+','+ingredients[key])
                        engine.runAndWait()
                # didn't ask for all ingredients
                else:
                    if ingredient_itr-1 < len(ingredients.keys()):
                        key = L_ingredient_key[ingredient_itr-1]
                        engine.say(key+','+ingredients[key])
                        engine.runAndWait()
                    else:
                        engine.say(instructions[instruction_itr-1])
                        engine.runAndWait()
            elif action == 5:
                if ident == '':
                    engine.say('expected recipe name right after recipe word')
                    engine.runAndWait()
                    break
                key = ident
                try:
                    engine.say(key+','+ingredients[key])
                except KeyError:
                    engine.say('ingredient not in recipe')
                engine.runAndWait()
            elif action == 6:
                confused = 'I do not understand'
                engine.say(confused)
                engine.runAndWait()
    return None
######## TEST BLOCK ########
if __name__ == '__main__':
    #instruction_book = {'apple': ['first do this', 'pour the water']}
    #ingredient_book = {'apple': {'eggs': '1', 'beans': '2 pounds'}}
    activate('hello')