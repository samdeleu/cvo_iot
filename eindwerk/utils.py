""" Een aantal handige utility functies """
def pp(msg, var):
    print(f"{msg}: type({type(var)})-{var}")
    
    
if __name__ == "__main__":
    a = 123
    pp("Message", a)