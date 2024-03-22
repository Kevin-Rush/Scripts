from pptx import Presentation

def add_alt_text_to_image(ppxt_file, slide_index, alt_text):
    # Get the specified slide
    slide = presentation.slides[slide_index]

    # Iterate through all shapes in the slide
    for shape in slide.shapes:
        if shape.shape_type == 13:  # Check if the shape is an image
            print(shape._element._nvXxPr.cNvPr.attrib.get("descr", ""))
            shape._element._nvXxPr.cNvPr.attrib["descr"] = alt_text  # Set the alt text for the image
            print(shape._element._nvXxPr.cNvPr.attrib.get("descr", ""))

    # Save the modified presentation
    presentation.save(ppxt_file)

# Usage example
ppxt_file = "C:/Users/kevin/Downloads/Week 06.pptx"
presentation = Presentation(ppxt_file)
alt_text = 'Alt text for the image'

for i in range(len(presentation.slides)):
    slide_i = i
    add_alt_text_to_image(ppxt_file, slide_i, alt_text)