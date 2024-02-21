import requests
from sapling import SaplingClient
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import pandas as pd

def grammar_evaluation(ppxt_filepath, sapling_api_key):

    presentation = Presentation(ppxt_filepath)

    for i, slide in enumerate(presentation.slides, start=1):
 
        client = SaplingClient

        for shape in slide.shapes:

            #access the text in all types of shapes
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    paragraph_text = "".join(run.text for run in paragraph.runs)
                    #send the slide text to sapling
                    edits = client.edits(paragraph_text, session_id='test_session')

                    text = str(text)
                    edits = sorted(edits, key=lambda e: (e['sentence_start'] + e['start']), reverse=True)
                    for edit in edits:
                        start = edit['sentence_start'] + edit['start']
                        end = edit['sentence_start'] + edit['end']
                        if start > len(text) or end > len(text):
                            print(f'Edit start:{start}/end:{end} outside of bounds of text:{text}')
                            continue
                        text = text[: start] + edit['replacement'] + text[end:]
        return text