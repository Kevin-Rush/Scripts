import requests
from sapling import SaplingClient
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import pandas as pd
from pptx import Presentation

def grammar_evaluation(ppxt_filepath, sapling_api_key):

    presentation = Presentation(ppxt_filepath)
    client = SaplingClient(api_key=sapling_api_key)

    for i, slide in enumerate(presentation.slides, start=1):
        for shape in slide.shapes:

            #access the text in all types of shapes
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:                        
                        run_text = run.text
                        edits = client.edits(run_text, session_id='test_session')

                        if run_text == "Legal Disclaimers":
                            continue
                        elif edits["edits"] != []:
                            print(f'Slide: {i}')
                            print(f'run_text: {run_text}')
                            print(f'Edits: {edits["edits"]}')
                            for edit in edits["edits"]:
                                start = edit['sentence_start'] + edit['start']
                                end = edit['sentence_start'] + edit['end']
                                if start > len(run_text) or end > len(run_text):
                                    print(f'Edit start:{start}/end:{end} outside of bounds of text:{run_text}')
                                    continue
                                run_text = run_text[: start] + edit['replacement'] + run_text[end:]
                            run.text = run.text.replace(run.text, run_text)
    #save the edited presentation to a file with the same path but a slightly different name
    presentation.save(ppxt_filepath[:-5] + "_edited.pptx")
    print("Grammar evaluation complete")

#open the file sapling_api_key.txt and read the api key
with open("C:/Users/kevin/Documents/Coding/Scripts/sapling_api_key.txt", "r") as file:
    sapling_api_key = file.read()

response = grammar_evaluation("C:/Users/kevin/Downloads/course/Week 1 - GAI.pptx", sapling_api_key)

print(response)