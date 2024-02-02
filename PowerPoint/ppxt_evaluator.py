from pptx import Presentation

def evaluate_ppxt(ppxt_filepath):
    presentation = Presentation(ppxt_filepath)

    for i, slide in enumerate(presentation.slides, start=1):
        slide_number = i
        title = "No Title"
        for shape in slide.shapes:
            if shape.is_placeholder and shape.placeholder_format.idx == 0:  # idx 0 is the title placeholder
                title = shape.text
                break

        # Accessing text within the slide with Markdown formatting
        slide_text = ""
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        slide_text += "* " + run.text + "\n"

        # Accessing notes within the slide with Markdown formatting
        notes_text = ""
        if slide.has_notes_slide:
            notes_slide = slide.notes_slide
            for paragraph in notes_slide.notes_text_frame.paragraphs:
                for run in paragraph.runs:
                    notes_text += "* " + run.text + "\n"

        # Evaluate the slide using chatgpt
        # Your evaluation logic goes here

        # Print the slide information
        print(f"Slide Number: {slide_number}")
        print(f"Title: {title}")
        print(f"Slide Text: {slide_text}")
        print(f"Notes Text: {notes_text}")
        print()

# Usage
ppxt_file = "C:/Users/kevin/Downloads/Intel AI for Workforce TTT AEAI.pptx"
evaluate_ppxt(ppxt_file)