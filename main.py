from parser import *
from table import *
from database import *

def main():
    # Set up the table list - TODO: needs to be able to be accessed from eval (protected var?)
    database = load_relations()
    database = restore_state()
    # for relation in relationList:
    #     if relation in database.relationList:
    #         do_nothing = True
    #     else:
    #         database.relationList.append(relation)
    # this operates under the assumption that relations with the same names
    # contain the exact same information and will not be added to the

    cmd = ""
    prompt = "> "
    cmd_list = []
    while cmd != "quit":
        cmd = raw_input(prompt)
        cmd_list.append(cmd)
        database,tokens = parse_expression(cmd,database)
    save_state(database)




main()
