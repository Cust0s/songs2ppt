import utils.functions as functions
import utils.ppt as ppt
import utils.song_functions as sng
import sys


def main():
    # get the base path for all future operations
    base_path = functions.define_base_path()

    # songs are always stored in the songs directory, relative to the base path
    song_lib_path = base_path / "songs/"

    # check if songs exists and create it if it doesn't
    if not functions.check_lib_dir(song_lib_path):
        sys.exit()

    # get the full list of songs available
    song_list = functions.get_all_songs(song_lib_path)

    # initialize list for selected songs
    selected_songs = []

    # sort list of available songs
    song_list.sort(key=lambda x: x[0])

    while True:
        # prompt user for a song and add it to the selection list
        selected_songs.append(functions.add_song(song_list))

        # print selection list
        functions.print_songs(selected_songs, "Selected Songs")

        # ask to add another song
        if not functions.user_continue():
            break

    print("Ended song selection")

    # Read content of selected songs
    song_data = []
    for song in selected_songs:
        song_data.append(sng.read_file(song[2]))

    # ToDo: ask user after which song to insert the "After Sermon" slide
    # sermon_after = input("Add 'sermon slide' after song number: ")

    ppt.create_lyrics_ppt(song_data)


if __name__ == "__main__":
    main()
