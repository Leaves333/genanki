import genanki
from jisho_api.word import Word

#define some useful functions
def concat_definitions(defs):
    string = ''
    for i in range(len(defs) - 1):
        string += defs[i] + "; "
    string += defs[-1]
    return string

#define some useful constants
card_model = genanki.Model(
    490490490,
    'pain peko',
    fields=[
        {'name': 'target'},
        {'name': 'sentence'},
        {'name': 'reading'},
        {'name': 'definition'},
    ],
    templates=[
        {
        'name': 'word -> def',
        'qfmt': '{{target}}<div class=uwu>{{sentence}}</div>',
        'afmt': '{{FrontSide}}<hr id=answer><div class=reading>{{reading}}</div><div class=def>{{definition}}</div>',
        },
    ],
    css='.card{ font-family: times; font-size: 40px; text-align: center; color: black; background-color: white; } .uwu{ font-size:25px; margin: 10px; } .def{ font-size: 25px; margin: 25px; } .accent{ font-size: 25px; margin: -10px; } .reading{ top: 10px; }')

deck = genanki.Deck(
    490490490,
    'pain peko')

#create a temp file for dumping errored cards
with open('tmp.txt', 'w') as file:
    pass

with open('list.txt', 'r', encoding="utf-8") as file:
    sentence = ''
    for line in file:

        if sentence == '':
            sentence = line
            continue

        r = Word.request(line)

        data_index = 0
        if (len(r.data) > 1):
            print()
            print(f'found multiple matches for: {line}context: {sentence}')
            #print(f'')

            match_found = False
            while (data_index < len(r.data)):
                word = r.data[data_index].japanese[0]
                print(f'is it: {word.word} ({word.reading})', end = '\r')
                inp = input()
                if inp == 'y' or inp == ' ':
                    match_found = True
                    break
                data_index += 1

            if not match_found:
                print(f"you've gone through all the matches, throwing {line[:-1]} into the error bin")
                with open('tmp.txt', 'a', encoding="utf-8") as tmp:
                    tmp.write(sentence + line)
                continue

        elif (len(r.data) == 0):
            print(f'found no matches for: {line}')
            with open('tmp.txt', 'a', encoding="utf-8") as tmp:
                tmp.write(sentence + line)
            continue

        uwu = r.data[data_index]
        word = uwu.japanese[0].word

        sense_index = 0
        if (len(uwu.senses) > 1):
            print()
            print(f'found multiple definitions for: {word}')
            print(f'context: {sentence}')

            match_found = False
            while (sense_index < len(uwu.senses)):
                definitions = uwu.senses[sense_index].english_definitions
                print(f'do you mean: {concat_definitions(definitions)}', end = '\r')
                inp = input()
                if inp == inp == 'y' or inp == ' ':
                    match_found = True
                    break
                sense_index += 1

            if not match_found:
                print(f"you've gone through all the definitions, throwing {line[:-1]} into the error bin")
                with open('tmp.txt', 'a', encoding="utf-8") as tmp:
                    tmp.write(sentence + line)
                continue

        #generate an anki card
        word = uwu.japanese[0].word
        reading = uwu.japanese[0].reading

        if word == None:
            word = reading
            reading = ''

        definition = concat_definitions(uwu.senses[sense_index].english_definitions)

        note = genanki.Note(model=card_model, fields=[word, sentence, reading, definition])
        deck.add_note(note)

        sentence = ''

genanki.Package(deck).write_to_file('output.apkg')

with open("list.txt", 'w', encoding="utf-8") as list_file:
    with open("tmp.txt", 'r', encoding="utf-8") as tmp_file:
        list_file.write(tmp_file.read())

with open("tmp.txt", 'w', encoding="utf-8") as tmp_file:
    pass