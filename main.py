from parser import *
from table import *

def main():
    # Set up the table list - TODO: needs to be able to be accessed from eval
    table_list = []

    cmd = ""
    prompt = "> "
    cmd_list = []
    while cmd != "quit":
        cmd = raw_input(prompt)
        cmd_list.append(cmd)
        tokens = parse_expression(cmd)




main()
