from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import pandas as pd

def process(ppxt_filepath):
    #this function processes a PowerPoint file and returns a dataframe with the slide number, title, slide text, and notes text

    presentation = Presentation(ppxt_filepath)

    #create an empty dataframe
    df = pd.DataFrame(columns=['Slide Number', 'Slide Type', 'Title', 'Subtitle', 'Slide Text', 'Notes Text'])

    for i, slide in enumerate(presentation.slides, start=1):
        slide_number = i

        slide_type = "No Type"
        title = "No Title"
        subtitle = "No Subtitle"
        slide_text = ""
        notes_text = ""

        for shape in slide.shapes:
            if shape.is_placeholder and shape.placeholder_format.idx == 0:  # idx 0 is the title placeholder
                title = shape.text
            
            if shape.is_placeholder and shape.placeholder_format.idx == 17:  # idx 1 is the subtitle placeholder
                print("-"*20)
            

            #if there is a text box, save the text to subtitle
            if shape.shape_type == MSO_SHAPE_TYPE.TEXT_BOX:
                if "https://www" not in shape.text: #verify it's not an image reference
                    subtitle = shape.text

            # Accessing the text within the slide
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    paragraph_text = "".join(run.text for run in paragraph.runs)
                    if paragraph_text.strip() and paragraph_text != title:  # Check if the paragraph text is not empty
                        slide_text += paragraph_text + "\n"

            if slide_text.strip() == subtitle.strip():
                subtitle = "No Subtitle"

            # Accessing the notes within the slide
            if slide.has_notes_slide:
                notes_slide = slide.notes_slide
                for paragraph in notes_slide.notes_text_frame.paragraphs:
                    notes_text += paragraph.text

            if "agenda" in title.lower():
                slide_type = "Agenda"
            elif "discussion" in title.lower():
                slide_type = "Discussion"
            elif "activity" in title.lower():
                slide_type = "Activity"
            elif subtitle == "No Subtitle" and slide_text == "":
                slide_type = "Title"
            elif subtitle == "No Subtitle" and slide_text != "":
                slide_type = "Transition"
            else:
                slide_type = "Content"

        #add slide 
        df = df.append({'Slide Number': slide_number, 'Slide Type': slide_type, 'Title': title, 'Subtitle': subtitle, 'Slide Text': slide_text, 'Notes Text': notes_text}, ignore_index=True)

    return df