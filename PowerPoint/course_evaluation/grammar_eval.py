import requests
from sapling import SaplingClient
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import pandas as pd

def grammar_evaluation(ppxt_filepath, sapling_api_key):

    presentation = Presentation(ppxt_filepath)
    client = SaplingClient(api_key=sapling_api_key)

    for i, slide in enumerate(presentation.slides, start=1):
        for shape in slide.shapes:

            #access the text in all types of shapes
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    paragraph_text = "".join(run.text for run in paragraph.runs)
                    #send the slide text to sapling
                    edits = client.edits(paragraph_text, session_id='test_session')
                    edits = sorted(edits, key=lambda e: (e['sentence_start'] + e['start']), reverse=True)
                    for edit in edits:
                        start = edit['sentence_start'] + edit['start']
                        end = edit['sentence_start'] + edit['end']
                        if start > len(text) or end > len(text):
                            print(f'Edit start:{start}/end:{end} outside of bounds of text:{text}')
                            continue
                        text = text[: start] + edit['replacement'] + text[end:]
        return text
    

#open the file sapling_api_key.txt and read the api key
with open("C:/Users/kevin/Documents/Coding/Scripts/sapling_api_key.txt", "r") as file:
    sapling_api_key = file.read()

response = grammar_evaluation("C:/Users/kevin/Downloads/course/Week 9 - GAI.pptx", sapling_api_key)

print(response)