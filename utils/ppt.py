from pptx import Presentation

# Todo: make lyrics version in normal font

# 0 = new slide indicator
# 1 = paragraph type (i.e., chorus, verse)
# 2 = chords
# 3 = lyrics
# 4 = paragraph type for chords only


def create_lyrics_ppt(data):
    """
    Creates the lyrics ppt file. This excludes slides for chords only
    structure elements (e.g., Instrumental, Interlude) and excludes
    the chords lines.
    :param data: The complete data for all selected songs
    """
    my_presentation = Presentation("dewg_template_lyrics.pptx")
    for song in data:
        slides = song[0]
        title = song[1]
        # artist = song[2]
        # key = song[3]

        for slide in slides:
            content_string = ""
            structure_text = ""
            # flag to skip lines when structure type = 4
            skip_flag = False
            for line in slide:
                if line[0] == 4:
                    # skip slide of this type (i.e., interlude, instrumental)
                    skip_flag = True
                elif line[0] == 1:
                    skip_flag = False       # reset skip flag as the following lines are needed
                    structure_text += line[1]
                    structure_text += " & "
                    pass
                elif line[0] == 2:
                    # skip chord lines
                    pass
                elif not skip_flag:
                    content_string += line[1]
                    content_string += "\n"
            if not skip_flag:

                # create new slide
                this_slide = my_presentation.slides.add_slide(my_presentation.slide_layouts[0])
                # add song title to top right placeholder
                this_slide.placeholders[10].text = title

                # add main content to the slide
                this_slide.placeholders[1].text = content_string
                this_slide.placeholders[0].text = structure_text[:-3]

    my_presentation.save("presentation_lyrics.pptx")


def create_chords_ppt(data):
    """
    Creates the chords ppt file. This includes slides for chords only
    structure elements (e.g., Instrumental, Interlude) and includes
    the chords lines.
    :param data: The complete data for all selected songs
    """

    # Todo: Add current song key to top right corner
    # Todo: Make lyrics text gray to focus on chords ->
    #  https://stackoverflow.com/questions/24729098/text-color-in-python-pptx-module

    my_presentation = Presentation("dewg_template_chords.pptx")
    for song in data:
        slides = song[0]
        title = song[1]
        # artist = song[2]
        # key = song[3]

        for slide in slides:
            # create new slide
            this_slide = my_presentation.slides.add_slide(my_presentation.slide_layouts[0])
            # add song title to top right placeholder
            this_slide.placeholders[10].text = title

            content_string = ""
            structure_text = ""
            for line in slide:
                if line[0] == 1 or line[0] == 4:
                    structure_text += line[1]
                    structure_text += " & "
                else:
                    content_string += line[1]
                    content_string += "\n"

            # add main content to the slide
            this_slide.placeholders[1].text = content_string
            this_slide.placeholders[0].text = structure_text[:-3]

    my_presentation.save("presentation_chords.pptx")
