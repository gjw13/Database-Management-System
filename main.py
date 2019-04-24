from parser import *
from table import *
from database import *

def main():
    #database = load_relations()
    database = restore_state()

    cmd = ""
    prompt = "> "
    cmd_list = []
    try:
        while cmd != "quit":
            cmd = raw_input(prompt)
            cmd_list.append(cmd)
            database,tokens = parse_expression(cmd,database)
        save_state(database)
    except:
        save_state(database) # save state even if error occurs
        print("An unknown error occurred.")




main()
