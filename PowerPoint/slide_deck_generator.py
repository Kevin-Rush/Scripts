from pptx import Presentation
import json

# Create a presentation object
presentation = Presentation(r"C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\base_presentation.pptx")
json_file = r"C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\generative_ai_presentation_script.json"

#read in the script from the json file
with open(json_file, 'r') as file:
    content = json.load(file)

content = content["slides"]

for i in range(len(content)):
    slide = presentation.slides.add_slide(presentation.slide_layouts[4])
    title = slide.shapes.title
    title.text = content[i]['title']

    slide_subtitle = slide.shapes[1]
    slide_subtitle.text = content[i]['subtitle']

    slide_content = slide.shapes[2]
    slide_content.text = content[i]['content']

# Save the presentation
presentation.save("generated_presentation.pptx")