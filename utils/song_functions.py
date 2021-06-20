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
