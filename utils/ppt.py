from pptx import Presentation


# Todo: split ppt creation into lyrics and chord presentations
# Todo: Add transpose feature
# Todo: make lyrics version in normal font

# 0 = new slide indicator
# 1 = paragraph type (i.e., chorus, verse)
# 2 = chords
# 3 = lyrics
# 4 = paragraph type for chords only

def create_lyrics_ppt(data):
    my_presentation = Presentation("dewg_template_chords.pptx")
    for song in data:
        slides = song[0]
        title = song[1]
        artist = song[2]
        key = song[3]

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

    my_presentation.save("test2.pptx")

