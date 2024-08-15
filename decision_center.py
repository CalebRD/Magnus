import json
import openai

def load_settings():
    with open('decision_center_settings.json') as f:
        settings = json.load(f)
    return settings


'''def generate_reply_text(input_text, conversation, system_prompt):
    llm_prompt = input_text
    llm_reply = conversation.prompt(llm_prompt, system = system_prompt)
    return llm_reply
'''

def generate_instructions(system_prompt, user_prompt, client, print_output):
    full_response = []
    if(print_output):
        print("DMC SYSTEM: ", end="")
    stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            if(print_output):
                print(chunk.choices[0].delta.content, end="")
            
            full_response.append(chunk.choices[0].delta.content)
    
    if(print_output):
        print("\n")
    
    full_response_string  = "DMC SYSTEM: " + "".join(full_response) + "\n"
    return full_response_string