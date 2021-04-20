from topRec import authorListCurrent

def nameInputFunc():
    name = input("\nEnter an author's name:\n")
    max = 3
    for i in range(max-1):
        if name not in authorListCurrent():
            name = input("\nWarning:\nThis name is not in the current author list.\nPlease try again:\n")
        else:
            break
    return name

def newName():
    nd = input("\nDo you want to check for an author's recommendation list? (y/n):\n")
    max = 3
    for i in range(max):
        if nd == "y" or nd == "yes" or nd == "yeah" or nd == "Y" or nd == "Yes" or nd == "Yeah":
            return True
        elif nd == "n" or nd == "no" or nd == "nope" or nd == "N" or nd == "No" or nd == "Nope":
            return False
        elif nd == "q" or nd == "quit" or nd == "Q" or nd == "Quit":
            print("Thank you for trying our program!")
            quit()
        if i < max - 1:
            nd = input("\nThis is not a valid input, please try again or press q to quit:\n")
        else:
            print("Too many failed attempts.")
    return False

def newDataFunc():
    nd = input("\nDo you want to update the comment data? (y/n):\n")
    max = 3
    for i in range(max):
        if nd=="y" or nd=="yes" or nd=="yeah" or nd=="Y" or nd=="Yes" or nd=="Yeah":
            return True
        elif nd=="n" or nd=="no" or nd=="nope" or nd=="N" or nd=="No" or nd=="Nope":
            return False
        elif nd=="q" or nd=="quit" or nd=="Q" or nd=="Quit":
            print("Thank you for trying our program!")
            quit()
        if i < max-1:
            nd = input("\nThis is not a valid input, please try again or press q to quit:\n")
        else:
            print("Too many failed attempts.")
    return False