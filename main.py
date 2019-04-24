from parser import *
from table import *
from database import *

def main():
    #database = load_relations()
    database = restore_state()

    cmd = ""
    prompt = "> "
    cmd_list = []
    while cmd != "quit":
        cmd = raw_input(prompt)
        cmd_list.append(cmd)
        database,tokens = parse_expression(cmd,database)
    save_state(database)




main()
