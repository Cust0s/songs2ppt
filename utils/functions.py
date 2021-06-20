from pathlib import Path


def define_base_path():
    """
    Defines the base path used in the project
    :return: The base path of the project
    """
    base_path = Path(__file__).resolve().parent.parent
    return base_path


def check_lib_dir(lib_path):
    """
    Checks if song library exists. Creates new directory
    if it does not exist.
    :param lib_path: The path of the song library
    """
    if not lib_path.exists():
        print("Song library does not exist. Creating new library...")
        try:
            lib_path.mkdir(parents=False, exist_ok=False)
        except FileNotFoundError:
            print("Creating song library directory failed because the expected parent directory does not exist.")
            return False
        except FileExistsError:
            print("A fatal error occurred trying to create the song library directory.")
            return False
    return True


def get_all_songs(lib_dir):
    """
    Searches the songs directory for songs. Creates a list with all the
    available songs.
    :param lib_dir: The directory for the song library
    :return: A list of tuples containing song name, artist and file path
    """
    song_paths = lib_dir.glob('*.song')  # get all song file paths

    song_list = []
    # read song name and artist from each file
    # and store it in list oprint(line)f tuples
    for fp in song_paths:
        with open(fp) as f:
            title = f.readline().rstrip('\n')
            artist = f.readline().rstrip('\n')
            song_list.append((title, artist, fp))

    return song_list


def print_songs(song_list, table_name):
    """
    Takes a list of tuples of songs and prints them with
    indexing numbers
    :param table_name: The table title to print
    :param song_list: A list of tuples (title, artist)
    """

    # ToDo: Add max title and artist name e.g. | My longe... |

    # find the longest title for padding purposes
    max_title = 0
    max_artist = 0
    # get the max number of index digits
    max_index = len(str(len(song_list) + 1))
    for song in song_list:
        if len(song[0]) > max_title:
            max_title = len(song[0])
        if len(song[1]) > max_artist:
            max_artist = len(song[1])

    # total line length without the leading and trailing pipe '|'
    total_line_len = max_index + max_title + max_artist + 8

    # create horizontal table lines
    line = "+" + "-" * (max_index + 2) + "+" + "-" * (max_title + 2) + "+" + "-" * (max_artist + 2) + "+"
    # print table name
    print("+" + "-" * total_line_len + "+")
    print(f"| {table_name.ljust(total_line_len-1)}|")
    print(line)

    # print each song with index, title and artist
    i = 1
    for song in song_list:
        # add trailing spaces to title
        title = song[0].ljust(max_title)
        # add leading spaces to index
        index = str(i).rjust(max_index)

        artist = song[1].ljust(max_artist)

        # i | title | artist
        print(f"| {index} | {title} | {artist} |")
        i += 1
    # print horizontal table line
    print(line)


def add_song(song_list):
    """
    Prints the complete song list and prompts the user to enter
    the index of the song to add. Returns the song to add.
    Includes input validation.
    :param song_list: The total song list to print
    :return: The selected song
    """
    # print the song list
    print_songs(song_list, "Available Songs")

    # prompt for the desired index and validate the user input
    while True:
        try:
            selected_index = int(input("Enter the number of the song to add: "))
            if selected_index not in range(1, len(song_list) + 1):
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid index number from the list! ", end='')

    return song_list[selected_index-1]


def user_continue():
    """
    Prompt the user if they want to continue selecting songs.
    Includes input validation.
    :return: True or False, depending on user choice
    """
    while True:
        try:
            reply = input("Do you want to add another song? (y/n) ").lower()
            if len(reply) > 1:
                raise ValueError
            if ord(reply) == 121:   # reply was 'y'
                return True
            elif ord(reply) == 110:   # reply was 'n'
                return False
            else:
                raise ValueError
        except ValueError:
            print("Please select only 'y', 'Y', 'n' or 'N'")
