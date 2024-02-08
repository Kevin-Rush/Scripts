from pptx import Presentation

# Create a presentation object
presentation = Presentation(r"C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\base_persentation.pptx")

# Slide 1 - Title slide
slide1 = presentation.slides.add_slide(presentation.slide_layouts[0])
title = slide1.shapes.title
title.text = "Improving the Performance of a Machine Learning Algorithm"

# Set the content for each slide
slides = [slide2, slide3, slide4, slide5, slide6, slide7]
content = [
    "This tutorial belongs to the series How to improve the performance of a Machine Learning Algorithm.",
    "A balanced dataset is a dataset where each output class is represented by the same number of input samples.",
    "Balancing techniques include oversampling, undersampling, class weight, and threshold.",
    "The imbalanced-learn library, part of the contrib packages of scikit-learn, is used in this tutorial.",
    "Data is imported using the pandas library, and the target class is created based on cuisine.",
    "The model is built using the Decision Tree algorithm, and evaluation metrics are calculated.",
    "The classification report and various plots are generated for the imbalanced dataset."
]

# Add content to each slide
for slide, content_text in zip(slides, content):
    content_placeholder = slide
    content_placeholder.text = content_text

# Save the presentation
presentation.save("machine_learning_presentation.pptx")