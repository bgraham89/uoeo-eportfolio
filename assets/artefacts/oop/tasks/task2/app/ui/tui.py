'''Functions to improve the text-based ui'''
from time import sleep

sleeptime = 1

def ux_print(message, wait=1):
    '''Prints a message and adds a wait so humans can keep up.'''
    print(message)
    sleep(wait * sleeptime)

def get_string(prompt):
    '''Asks for a response'''
    response = input(prompt)
    sleep(sleeptime)
    return response

def get_bool(prompt):
    '''Asks for something to intepret asa bool'''
    response = input(prompt)
    sleep(sleeptime)
    return response[0] in ("y", "Y") if response else False

def get_choice(prompt, options):
    '''Asks for a choice from options'''
    response = input(prompt)
    sleep(sleeptime)
    err_message = "I'm sorry, but that wasn't a valid option."
    options_message = f"Your options are: {options}"
    retry_prompt = "would you like to try again?"
    if response not in options:
        ux_print(err_message)
        if get_bool(retry_prompt):
            ux_print(options_message)
            return get_choice(prompt, options)
        else:
            return False
    else:
        return response


