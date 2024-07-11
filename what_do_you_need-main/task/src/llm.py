import openai
import os
import json
from task.src.utils import save_to_json, load_from_json
from openai import AsyncOpenAI

api_key = 'your open ai key'

client = AsyncOpenAI(api_key=api_key)

tools = [
            {
    "type": "function",
    "function": {
        "name": "extract_chat_info",
        "description": "Extracts specific information from the ongoing chat to gather high-quality leads.",
        "parameters": {
            "type": "object",
            "properties": {
                "quoted_request": {
                    "type": "string",
                    "description": "The specific service or item the user wants quoted."
                },
                "zip_code": {
                    "type": "string",
                    "description": "The user's zip code."
                },
                "address": {
                    "type": "string",
                    "description": "The user's address."
                },
                "email": {
                    "type": "string",
                    "description": "The user's email address."
                },
                "name": {
                    "type": "string",
                    "description": "The user's name."
                },
                "phone_number": {
                    "type": "string",
                    "description": "The user's phone number."
                },
                "issue_details": {
                    "type": "string",
                    "description": "Specific details about the user's issue."
                },
                "issue_picture": {
                    "type": "string",
                    "description": "A link to the picture of the issue, if provided by the user."
                },
                "additional_services": {
                    "type": "string",
                    "description": "Any additional services the user might need (e.g., landscaping, gutters)."
                },
                
            },
            "required": [
                "quoted_request",
                "zip_code",
                "address",
                "email",
                "name",
                "phone_number",
                "issue_details"
            ]
        }
    }
}

            ]



# async def search_for_documents(messages, user_id, database: ClientAPI):
#     tools = [
#             {
#     "type": "function",
#     "function": {
#         "name": "extract_chat_info",
#         "description": "Extracts specific information from the ongoing chat to gather high-quality leads.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "quoted_request": {
#                     "type": "string",
#                     "description": "The specific service or item the user wants quoted."
#                 },
#                 "zip_code": {
#                     "type": "string",
#                     "description": "The user's zip code."
#                 },
#                 "address": {
#                     "type": "string",
#                     "description": "The user's address."
#                 },
#                 "email": {
#                     "type": "string",
#                     "description": "The user's email address."
#                 },
#                 "name": {
#                     "type": "string",
#                     "description": "The user's name."
#                 },
#                 "phone_number": {
#                     "type": "string",
#                     "description": "The user's phone number."
#                 },
#                 "issue_details": {
#                     "type": "string",
#                     "description": "Specific details about the user's issue."
#                 },
#                 "issue_picture": {
#                     "type": "string",
#                     "description": "A link to the picture of the issue, if provided by the user."
#                 },
#                 "additional_services": {
#                     "type": "string",
#                     "description": "Any additional services the user might need (e.g., landscaping, gutters)."
#                 },
#                 "additional_prompts": {
#                     "type": "string",
#                     "description": "Additional information prompts that could be useful for future reference."
#                 }
#             },
#             "required": [
#                 "quoted_request",
#                 "zip_code",
#                 "address",
#                 "email",
#                 "name",
#                 "phone_number",
#                 "issue_details"
#             ]
#         }
#     }
# }

#             ]
    


#     response = await client.chat.completions.create(
#         model = 'gpt-4o',
#         temperature = 0.7,
#         messages = messages,
#         tools = tools,
#         # tool_choice = {"type": "function", "function": {"name": "query_enhancer"}}
#     )


#     print(response)
#     # enhanced_query = json.loads(response["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]).get("query_enhancer")

#     collection = database.get_collection(
#             name=user_id,
#             embedding_function=openai_ef
#         )
#     query_vector = await text_embedding(enhanced_query, user_id)

#     results=collection.query(    
#         query_embeddings=query_vector,
#         include=["documents"],
#         n_results = 5
#     )
    
#     res = ""
#     for result in results["documents"][0]:
#         res = res + result + '\n'

    
    


async def generate_response(query, user_id, messages: list):


    # file, messages = await load_from_json(user_id)

    # res = await search_for_documents(messages, user_id, database)
    messages.append(
        {
            "role":"user",
            "content":f'''
            {query}
            '''
        }
    )
    answer = await client.chat.completions.create(
        model = 'gpt-4o',
        temperature = 0.7,
        messages = messages,
        tools=tools
    )

    ai_response = answer.choices[0].message.content
    # await save_to_json(messages, query, ai_response, file, user_id)
    return ai_response
    



async def generate_response_with_image(query, user_id, messages: list, image_url):


    # file, messages = await load_from_json(user_id)

    # res = await search_for_documents(messages, user_id, database)
    messages.append(
        {
            "role":"user",
            "content":[
                 {
                      "type":"text",
                      "text":query
                 },
                 {
                      "type":"image_url",
                      "image_url":{
                           "url":f"data:image/png;base64,{image_url}"
                      }
                 }
            ]    
        }
    )
    answer = await client.chat.completions.create(
        model = 'gpt-4o',
        temperature = 0.7,
        messages = messages,
        tools=tools
    )

    ai_response = answer.choices[0].message.content

    # await save_to_json(messages, query, ai_response, file, user_id)

    return ai_response
    



# async def text_embedding(text: str, user_id : str) -> list[int]:

#         try:
#             response = await client.embeddings.create(model="text-embedding-ada-002", input=text)
#             return response.data[0].embedding
#         except Exception as e:
#             print(f"Error in text_embedding: {e} for user id {user_id}\n\n")
            
#             return []