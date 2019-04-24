from parser import *
from table import *
from database import *

def main():
    # Set up the table list - TODO: needs to be able to be accessed from eval (protected var?)
    database = load_relations()
    test_table = restore_state()

    cmd = ""
    prompt = "> "
    cmd_list = []
    while cmd != "quit":
        cmd = raw_input(prompt)
        cmd_list.append(cmd)
        database,tokens = parse_expression(cmd,database)
    save_state(database)




main()
