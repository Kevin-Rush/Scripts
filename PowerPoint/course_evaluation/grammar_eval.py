import requests
from sapling import SaplingClient

def grammar_evaluation(df, sapling_api_key):

    #remove the columns slide number and slide type
    df = df.drop(columns=['Slide Number', 'Slide Type', 'Slide Title'])
    #replace all entries of no info with ""
    df = df.replace("No Subtitle", "")
    df = df.replace("No Content", "")
    df = df.replace("No Notes", "")

    #before sending to sapling, remove all links
    df = df.replace(r'http\S+', '', regex=True).replace(r'www\S+', '', regex=True)

    #run through each row of the dataframe and send the slide text to sapling
    for i, row in df.iterrows():
        
        client = SaplingClient(api_key=sapling_api_key)
        edits = client.edits('Lets get started!', session_id='test_session')

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