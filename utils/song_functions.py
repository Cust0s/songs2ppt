import sys

# define keys that require sharps
sharp_keys = ("g", "em", "d", "bm", "a", "f#m", "e", "c#m", "b", "g#m", "f#", "d#m", "c#", "a#m", "c", "am")

# n.1 symbolises sharps and n.2 symbolises flats
# values are unique
notes = {
        "A": 1,
        "A#": 2.1,
        "Bb": 2.2,
        "B": 3,
        "C": 4,
        "C#": 5.1,
        "Db": 5.2,
        "D": 6,
        "D#": 7.1,
        "Eb": 7.2,
        "E": 8,
        "F": 9,
        "F#": 10.1,
        "Gb": 10.2,
        "G": 11,
        "G#": 12.1,
        "Ab": 12.2
}


def read_file(file_path):
    """
    Reads the file from the argument file path and stores its
    contents in a structured manner.
    :param file_path: The file path to the .song file
    :return: Structured data of the song
    """
    with open(file_path) as f:
        # initialize the list that contains all the lyrics and chords
        slides = [[]]

        # index for latest slide
        cur_slide = 0
        title = f.readline().replace('\n', '')
        artist = f.readline().replace('\n', '')
        key = f.readline().replace('\n', '')
        line = f.readline().replace('\n', '')

        while line:
            if line[0] != '#':      # ignore comment lines
                line_purpose = int(line[0])
                if line_purpose == 0:
                    # put following lines in new slide
                    # advance slide index
                    cur_slide += 1
                    # add new slide to list
                    slides.append([])
                else:
                    slides[cur_slide].append([line_purpose, line[1:]])

            line = f.readline().replace('\n', '')

            # list of slides
            # slides = [slide1, slide2, slide3]
            # list of main content lines for each slides (chords and lyrics mixed)
            # slide1 = [line1, line2, line3]
            # store each line and also the number indicating its function
            # line1 = [number, string]

    return slides, title, artist, key


def change_key(song, actual_key, desired_key):
    """
    Takes the song data and transposes the chords before returning the full song data with transposed chords.
    :param actual_key: The key of the song in the library
    :param song: Slide data for a single song
    :param desired_key: The desired key to transpose to.
    :return: The transposed song data in the same format as the input song data
    """

    # make user input conform to capitalization of notes
    desired_key = desired_key.lower().capitalize()
    actual_key = actual_key.lower().capitalize()

    # get the index number for both keys
    desired_index = -1
    actual_index = -1

    for note in notes:
        # get the index for the desired key
        if note == desired_key:
            desired_index = int(notes.get(note))
        # get the index for the actual key
        if note == actual_key:
            actual_index = int(notes.get(note))

    # Todo: check whether desired key requires sharps or flats
    is_sharp = True

    # calculate number of half steps to transpose
    difference = desired_index - actual_index   # calculate difference
    if actual_index > desired_index:
        difference = difference + 12            # adjust difference for rollover. E.g., G to A# (11 to 2)

    # loop through each slide and line of the song to transpose the chord lines
    for i in range(0, len(song)):           # for slide in slides
        for j in range(0, len(song[i])):    # for line in slide
            if song[i][j][0] == 2:          # line is a chord line

                # extract the notes from the chord string into a list including the offset for each song
                # song[i][j][0] is the line designation. E.g., 2 -> chord line, 3 -> lyrics line
                # song[i][j][1] is the actual string of chords
                chords = extract_notes(song[i][j][1])
                # using the list of chords, transpose each chord one by one
                returned = transpose_chords(chords, difference, is_sharp)
                # using the list of chords with their offset, create a new chord string and save it into the song
                song[i][j][1] = new_chord_string(returned)

    # return the modified song
    return song


def extract_notes(line):
    """
    Takes a string of chords and separates it into a list of chords. Each chord is a list with its beginning index (to
    guarantee that it can line up again after transposing) as well as the chord as a string.
    :param line: The line containing chords
    :return: A list of the chords of the input line. Each chord is paired with its offset [offset, chord]
    """
    this_start_index = -1     # records the start index of the new chord
    this_chord = ""     # records the string that becomes the new chord (char by char)
    new_chord = True    # flag to indicate the next char to belong to a new chord
    chords = []         # list of chord lists. Each chord has (start index, chord string)

    line += " "         # add an extra space at the end to invoke the chords.append() method one last time at the end
    for i in range(0, len(line)):
        if line[i] == " ":      # if the current char is a space
            if not new_chord:
                new_chord = True  # If a space occurs, this means that the old chord is finished and a new one is coming
                chords.append([this_start_index, this_chord])
            pass
        else:
            if new_chord:
                this_start_index = i    # record the start index of this new chord
                this_chord = ""         # reset the chord string
                new_chord = False       # set the flag to false
            this_chord += line[i]       # add char to the chord string

    return chords


def transpose_chords(chords, difference, is_sharp):
    """
    Takes a list of chords and transposes them one by one.
    :param chords: A list of chords. Each chord is a list of [offset, chord]
    :param difference: The amount of half-steps to transpose upwards
    :param is_sharp: Flag to indicate whether to use sharps or flats with the new key
    :return: A list identical in structure and size to the input chords list, with transposed chords
    """

    for i in range(0, len(chords)):
        chord = chords[i]
        # if the chord is double, then split it. E.g., A/C#
        split_chord = chord[1].split('/')
        for j in range(0, len(split_chord)):
            half_chord = split_chord[j]
            # process each split chord as if it were it's own chord
            if len(half_chord) == 1:
                # a one long chord is always a base chord
                base_chord = transpose_helper(half_chord, difference, is_sharp)
                # print(f"orig: {half_chord}, new: {base_chord}")
            else:
                # if the second char is either 'b' or '#', it is part of the base chord
                if half_chord[1] == 'b' or half_chord[1] == '#':
                    base_chord = transpose_helper(half_chord[:2], difference, is_sharp)
                    base_chord += half_chord[2:]    # add the trailing chars to the new base chord. E.g. A# + sus2
                    # print(f"orig: {half_chord}, new: {base_chord}")
                else:
                    base_chord = transpose_helper(half_chord[0], difference, is_sharp)
                    base_chord += half_chord[1:]    # add the trailing chars to the new base chord. E.g. A + sus2
                    # print(f"orig: {half_chord}, new: {base_chord}")
            split_chord[j] = base_chord

        # combine the split chords again
        new_chord = ""
        for half_chord in split_chord:
            new_chord += half_chord + "/"   # add the slash at the end of every split chord
        chords[i][1] = new_chord[:-1]       # remove the very last slash again

    return chords


def transpose_helper(chord, difference, is_sharp):
    """
    Transposes a single base chord for the transpose_chords function.
    :param is_sharp: Flag that indicates if sharps or flats are used in desired key
    :param difference: The number of half steps to transpose (always up)
    :param chord: A single base chord as string. E.g., "A" or "Ab" or "A#"
    :return:
    """

    # get the index value for the current base note
    try:
        actual_index = int(notes.get(chord))
    except TypeError:
        print(f"Error in transpose_helper. Base chord unknown. Given value: {chord}\n"
              f"Correct the chord in the song file and try again!")
        sys.exit()
    # add transpose the value
    desired_index = actual_index + difference
    # if the index overflowed, let it loop back to 1
    if desired_index > 12:
        desired_index -= 12

    # flats and sharps are differentiated by float values
    # n.1 = sharp
    # n.2 = flat
    if is_sharp:
        desired_index += 0.1
    else:
        desired_index += 0.2

    # returns the string of the transposed base note from the notes dictionary based on the desired index
    # the notes dictionary has unique values
    return get_key(desired_index)


def get_key(val):
    """
    Returns the key for a given value in the notes dictionary. Modified to look for keys with integer value first, and
    then a key with float value if no integer value matched. Values in the notes dictionary are unique.
    :param val: The value to look for. Must be a float
    :return: The key for the given value or ??? if something went wrong
    """
    # first check for values without sharps or flats (with int)
    for key, value in notes.items():
        if int(val) == value:
            return key
    # if first search failed, search for sharps or flats (with float)
    for key, value in notes.items():
        if val == value:
            return key

    # something went wrong. Print ??? for the chord instead
    return "???"


def new_chord_string(chords):
    """
    Takes a list of chords, each chord structured: [offset, chord], and creates a viable string for the powerpoint.
    Using the offset, it is guaranteed that the transposed chord starts in the same position as the old chord relative
    to the beginning of the line. This is only true if the transposed chord does not significantly grow in size.
    :param chords: List of transposed chords, structured: [offset, chord]
    :return: A string with proper chord spacing
    """
    new_string = ""
    for chord_object in chords:
        offset = chord_object[0]
        chord = chord_object[1]
        # calculate the amount of leading spaces
        leading_spaces = offset - len(new_string)   # find out how many leading spaces to print
        # if the current string ends later than the current chord's offset indicates, add the new chord after that
        if leading_spaces < 0:
            leading_spaces = 0
        # add an extra space after each chord to guarantee at least 1 space between each chord
        new_string += leading_spaces * " " + chord + " "

    return new_string
