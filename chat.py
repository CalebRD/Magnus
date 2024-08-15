import json

def load_settings():
    with open('speech_settings.json') as f:
        settings = json.load(f)
    return settings


'''def generate_reply_text(input_text, conversation, system_prompt):
    llm_prompt = input_text
    llm_reply = conversation.prompt(llm_prompt, system = system_prompt)
    return llm_reply'''

def generate_natural_output(system_prompt, user_prompt, client, print_output):
    full_response = []
    
    #Print tag
    if(print_output):
        print("NL SYSTEM: ", end="")

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
    
    full_response_string  = "NL SYSTEM: " + "".join(full_response)
    return full_response_string
