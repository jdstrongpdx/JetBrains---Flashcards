import sys

# global data structures used across the program
card_dict = {}
log_file = []


def main():
    """Main function for managing program"""
    global card_dict

    # if arguments passed in the command line, import file upon opening or export file upon closing
    import_file, export_file = get_filename()
    if import_file:
        import_cards()
    user_input = ""
    while user_input != "exit":                 # loop program unit user wants to exit
        printer("\nInput the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        user_input = get_input()
        if user_input == "add":                 # adds new flashcards to the program
            add()
        elif user_input == "remove":            # removes flashcards from the program
            remove()
        elif user_input == "import":            # imports a file and loads it into the card deck
            import_cards()
        elif user_input == "export":            # exports all cards from the card deck
            export_cards()
        elif user_input == "ask":               # quizzes the user on the terms/definitions from the flashcards
            ask()
        elif user_input == "exit":              # exits the program (and exports if argument passed on command line)
            if export_file:
                export_cards()
            printer("Bye bye!")
        elif user_input == "log":               # logs all user entry and print statements to the console
            log()
        elif user_input == "hardest card":      # determines the hardest card(s) and prints
            hardest_card()
        elif user_input == "reset stats":       # resets the 'mistakes' counts for all flashcards
            reset_stats()
        else:
            printer("User Input Error")         # error if user inputs a non-menu function
     
            
def get_input() -> str:
    """Receive all user input, stores inputs in the log_file, and returns the user input"""
    global log_file
    user_input = input()
    log_file.append("> " + user_input)
    return user_input


def printer(value) -> None:
    """Receive all print statements, stores outputs in the log_file, and prints statements to the console"""
    global log_file
    log_file.append(value)
    print(value)
    return


def get_filename() -> (str, str):
    """Check if filenames were passed as command-line arguments and returns results"""
    import_file, export_file = "", ""
    count = len(sys.argv)
    for index in range(1, count):
        filename = sys.argv[index].split("=")
        if "--import" in filename[0]:
            import_file = filename[1]
        elif "--export" in filename[0]:
            export_file = filename[1]
    return import_file, export_file


def add() -> None:
    """Add new flashcards to the deck ensuring unique terms and definitions for all cards"""
    global card_dict
    printer(f'The card:')
    while True:
        term = get_input()
        if term in card_dict.keys():
            printer(f'The term "{term}" already exists. Try again:')
        else:
            break
    printer(f'The definition of the card:')
    while True:
        flag = 0
        definition = get_input()
        for value in card_dict.values():
            if value['definition'] == definition:
                printer(f'The definition "{definition}" already exists. Try again:')
                flag = 1
        if not flag:
            break
    card_dict[term] = {'definition': definition, 'mistakes': 0}
    printer(f'The pair ("{term}":"{definition}") has been added.')
    return


def remove() -> None:
    """Remove a flashcard from the deck or inform user of an error."""
    global card_dict
    printer("Which card?")
    user_input = get_input()
    if user_input in card_dict.keys():
        del card_dict[user_input]
        printer("The card has been removed")
    else:
        printer(f'Can\'t remove "{user_input}": there is no such card.')
    return


def import_cards() -> None:
    """Import flashcards into the deck from a filename passed by command-line argument or user_input."""
    global card_dict
    count = 0
    import_file, export_file = get_filename()
    if not import_file:
        printer("File name:")
        import_file = get_input()
    try:
        file = open(import_file, 'r')
        for line in file:
            value = line.rstrip("\n")
            value = value.split(",")
            card_dict[value[0]] = {'definition': value[1], 'mistakes': int(value[2])}
            count += 1
        file.close()
        printer(f"{count} cards have been loaded.")
    except FileNotFoundError:
        printer("File not found.")
    return


def export_cards() -> None:
    """Export entire flashcard deck into a file with the filename passed by command-line argument or user_input."""
    global card_dict
    import_file, export_file = get_filename()
    if not export_file:
        printer("File name:")
        export_file = get_input()
    file = open(export_file, 'w')
    for key, value in card_dict.items():
        writer = key + "," + value['definition'] + "," + str(value['mistakes']) + "\n"
        file.write(writer)
    file.close()
    printer(f'{len(card_dict)} cards have been saved.')
    return


def ask() -> None:
    """Quiz the user on the definitions of terms from the flashcard deck and inform of
       correct/incorrect/or misplaced answers."""
    global card_dict
    count = 0
    printer("How many times to ask?")
    card_quantity = int(get_input())
    while count != card_quantity:
        for term, definition in card_dict.items():
            count += 1
            printer(f'Print the definition of "{term}":')
            answer = get_input()
            if definition['definition'] == answer:
                printer("Correct!")
            else:
                definition['mistakes'] += 1
                flag = 0
                for key, value in card_dict.items():
                    if answer == value['definition']:
                        question = key
                        printer(f'Wrong.  The right answer is "{definition["definition"]}", but your definition is '
                                f'correct for "{question}"')
                        flag = 1
                if not flag:
                    printer(f'Wrong. The right answer is "{definition["definition"]}".')
            if card_quantity == count:
                break
    return


def log() -> None:
    """Save the log file of all user_inputs and all print statements to a file"""
    global log_file
    printer("File name:")
    user_input = get_input()
    file = open(user_input, 'w')
    for value in log_file:
        file.write(value + "\n")
    file.close()
    printer('The log has been saved.')
    return


def hardest_card() -> None:
    """Print the card(s) with the highest number of mistakes during the ask function"""
    global card_dict
    highest = 0
    card = []
    for key, value in card_dict.items():
        if value['mistakes'] > highest:
            highest = value['mistakes']
            card = [key]
        elif value['mistakes'] == highest:
            card.append(key)
    if highest == 0:
        printer("There are no cards with errors.")
    elif len(card) == 1:
        printer(f'The hardest card is "{card[0]}". You have {highest} errors answering it.')
    else:
        printer(f'The hardest card is "{", ".join(card)}". You have {highest} errors answering it.')
    return


def reset_stats() -> None:
    """Reset the mistake counts of all flashcards in the deck."""
    global card_dict
    for value in card_dict.values():
        value['mistakes'] = 0
    printer("Card statistics have been reset.")
    return


if __name__ == "__main__":
    main()
