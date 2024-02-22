from colorama import Fore
from openai import OpenAI
import ppxt_visual_eval

def evaluate(df, api_key):
    # This function takes a dataframe and an API key and returns a list of responses from the GPT-3.5 model

    client = OpenAI()
    client.api_key = api_key

    #add the column 'Response' to the dataframe
    df['Response'] = ""

    #iterate over the dataframe
    print(f"{Fore.GREEN}---------------------Evaluation has Started---------------------{Fore.RESET}")
    total_tokens = 0
    for i, row in df.iterrows():
        
        messages_highview = [
            {"role": "system", "content": "You are an expert educational course designer and you excel at organizing information in the most logical flow to ensure the best learning experience for the students. You are also excellent at thinking of the perfect titles and subtitles to capture the essence of the content in a professional and academic tone. Your final masterful skill is you are able to write the perfect transition sentences to move from one topic to the next in the briefest and most effective way. Due to your expertise, you always get asked to help review other people's work and provide feedback. Your feedback is normally constructive and actionable and you always provide 3 specific pieces of feedback for every slide you review, 2 negative and 1 positive, unless you are specifically asked for a certain type of response. However, most importantly, you do not say anything that is unhelpful. You always provide feedback that is actionable and constructive, and if there's nothing to say, you say all good!"},
        ]

        messages_lowview = [
            {"role": "system", "content": "You are an expert educational course writer and you excel at presenting information in a clear and concise manner for the high school level. You pride yourself on your academic professionalism and you NEVER use any extravegant phrasing (extravegant phrasing includes but is not restricted to: 'delve', 'utilize', 'the art and science of', 'enter the world of', etc.). You excel at knowing when a slide has too little text, and needs additional information, or when a slide has too much text and needs to be simplified and how to use the notes section to excellently balance a slide. Due to your expertise, you always get asked to help review other people's work and provide feedback. Your feedback is normally constructive and actionable and you always provide 3 specific pieces of feedback for every slide you review, 2 negative and 1 positive, unless you are specifically asked for a certain type of response. However, most importantly, you do not say anything that is unhelpful. You always provide feedback that is actionable and constructive, and if there's nothing to say, you say all good!"},
        ]
        messages_activity = [
            {"role": "system", "content": "You are an expert educational activity planner and you excel at creating engaging and interactive activities for students to complete. You are able to write clear and concise instructions for activities and you are able to provide the perfect amount of information to ensure the students can complete the activity without any issues. You are also always able to think of the best discussion questions that will stimulate lively conversations because they do not get students to simply report on information, but to take on opinions and support those opinions. Due to your expertise, you always get asked to help review other people's work and provide feedback. Your feedback is normally constructive and actionable and you always provide 3 specific pieces of feedback for every slide you review, 2 negative and 1 positive, unless you are specifically asked for a certain type of response. However, most importantly, you do not say anything that is unhelpful. You always provide feedback that is actionable and constructive, and if there's nothing to say, you say all good!"},
        ]
        
        slide_type = row['Slide Type']
        
        # Make different calls to chatgpt based on slide_type
        if slide_type == "Recap" or slide_type == "Legal" or slide_type == "Bibliography":
            response = "Ignored"
        elif slide_type == 'Title':
            messages_highview.append({"role": "user", "content": "Hello, can you tell me if this is a good slide title? If it's good, say 'It's good' and nothing else, but if it's bad, tell me exactly why in one sentence and give me an alternative title around the same length if not shorter. Slide Title: " + row['Title']})
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages_highview,
            )
            messages_highview.pop()
            total_tokens += response.usage.total_tokens
            response = response.choices[0].message.content
        
        elif slide_type == 'Agenda':
            messages_highview.append({"role": "user", "content": "Hello, can you please evaluate my agenda slide? Let me know what you think about: 1) The overall flow 2) The naming of the specific sections Slide. Title: " + "Hello, can you please evaluate my content slide? Slide Title: " + str(row['Title']) + " Slide Contents: " + str(row['Slide Text']) + " Slide Notes: " + str(row['Notes Text']) + "If it's"})
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages_highview,
            )
            messages_highview.pop()
            total_tokens += response.usage.total_tokens
            response = response.choices[0].message.content
        
        elif slide_type == 'Transition':
            messages_highview.append({"role": "user", "content": "Hello, can you please evaluate my transition slide? If it's good, say 'It's good' and nothing else, but if it's bad, tell me exactly why in one sentence and give me an alternative transition around the same length if not shorter. Slide Contents: " + row['Slide Text']})
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages_highview,
            )
            messages_highview.pop()
            total_tokens += response.usage.total_tokens
            response = response.choices[0].message.content
        
        elif slide_type == 'Discussion':
            messages_activity.append({"role": "user", "content": "Hello, can you please evaluate my discussion questions? If they're good, say 'They're good' and nothing else, but if they're bad, tell me why and give me some alternatives. Slide Title: " + "Hello, can you please evaluate my content slide? Slide Title: " + str(row['Title']) + " Slide Contents: " + str(row['Slide Text']) + " Slide Notes: " + str(row['Notes Text'])})
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages_activity,
            )
            messages_activity.pop()
            total_tokens += response.usage.total_tokens
            response = response.choices[0].message.content
        
        elif slide_type == 'Activity':
            messages_activity.append({"role": "user", "content": "Hello, can you please evaluate my activity questions? Slide Title: " + "Hello, can you please evaluate my content slide? Slide Title: " + str(row['Title']) + " Slide Contents: " + str(row['Slide Text']) + " Slide Notes: " + str(row['Notes Text'])})
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages_activity,
            )
            messages_activity.pop()
            total_tokens += response.usage.total_tokens
            response = response.choices[0].message.content
            
        elif slide_type == 'Content' and row['Slide Text'] == "":
            if i < 9:
                response = ppxt_visual_eval.run('ppxt_images/slide_0'+str(i+1)+'.jpg', api_key)
                total_tokens += response['usage']["total_tokens"]
                response = response['choices'][0]['message']['content']
            else: 
                response = ppxt_visual_eval.run('ppxt_images/slide_'+str(i+1)+'.jpg', api_key)
                total_tokens += response['usage']["total_tokens"]
                response = response['choices'][0]['message']['content']
        else:
            messages_lowview.append({"role": "user", "content": "Hello, can you please evaluate my content slide? Slide Title: " + "Hello, can you please evaluate my content slide? Slide Title: " + str(row['Title']) + " Slide Contents: " + str(row['Slide Text']) + " Slide Notes: " + str(row['Notes Text'])})
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages_lowview,
            )
            messages_lowview.pop()
            total_tokens += response.usage.total_tokens
            response = response.choices[0].message.content

        #add the response to the column 'Response' in the df
        df.at[i, 'Response'] = response
        #print(response)
        percentage = int((i / len(df)) * 100)
        loading_bar = '#' * (percentage // 2 + 2) + '-' * (50 - percentage // 2)
        print(f"\r[{loading_bar}] {percentage}%", end='')
    print()
    print(f"{Fore.RED}---------------------Total Tokens Used: {total_tokens}---------------------{Fore.RESET}")
    print()

    return df
