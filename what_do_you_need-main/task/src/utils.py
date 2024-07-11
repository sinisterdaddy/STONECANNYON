import json


system_prompt = {"role": "system", 
                 "content":'''
You are Wordpress Chatbot. You have data about a website saved in a vector store which has been scraped. It contains information about all the blogs and other articles present on the website. 
The user will ask questions which may refer to a particular article or other aspects of the website. With every user's query, you will be provided with the relevant documents that have been fetched according to the user's query.
If the document contains relevant information according to the user's query, answer the query based on the retrieved documents. For other irrelevant queries such as salutations or general knowledge, answer according to your own knowledge. 
'''}

async def load_from_json(user_id):
    with open ('users.json', 'r') as f:
        file = json.load(f)

    for user in file:
        if user_id == user['user_id']:
            messages = user['messages']

    return file, messages




async def save_to_json(messages: list, query : str, ai_response : str, file, user_id):
    messages.append(
        {
            "role":"assistant",
            "content":ai_response
        }
    )
    
    messages[-2] = {
        "role":"user",
        "content":query
    }

    for user in file:
        if user_id == user['user_id']:
            user['messages'] = messages



    with open('users.json','w') as f:
        json.dump(file , f, indent=4)