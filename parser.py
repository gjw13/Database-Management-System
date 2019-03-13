# testing command prompt

def tokenizer(cmd):
    # takes in sql command in string form
    # returns a list of tokens
    tokens = cmd.split(" ")
    print(tokens)
    return tokens

def main():
    cmd = ""
    while cmd != "quit":
        cmd = raw_input("> ")
        tokens = tokenizer(cmd)


main()
