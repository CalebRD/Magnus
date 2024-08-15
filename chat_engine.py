import llm
import openai
import chat
import decision_center
'''def initialize_conversation():
        #create the bot conversation
        model = llm.get_model("nous-hermes-llama2-13b")
        model.key = ''
        conversation = model.conversation()
        return conversation

conversation = initialize_conversation()
    #get settings
nl_settings = chat.load_settings()
dmc_settings = decision_center.load_settings()
dmc_system_prompt = dmc_settings['system_prompt'].join(str(x) for x in dmc_settings['available_instructions']) + "You are named Magnus. You are speaking to  " + dmc_settings["current_user"] + "\n"
nl_system_prompt = nl_settings['system_prompt'] + nl_settings['personality'] + "You are named Magnus. You are speaking to  " + nl_settings["current_user"] + "\n" 


while True:
    print("You: ", end='')
    user_input = input()
    #print("Magnus: ", end='')

    if user_input.lower() == "exit":
        break
        
    dmc_output = decision_center.generate_reply_text(user_input, conversation, dmc_system_prompt)
    print("DMC: ", dmc_output)
    
    nl_system_prompt += dmc_output

    reply_text = chat.generate_reply_text(user_input, conversation, nl_system_prompt)
    print("NLP: ", reply_text)
    print("\n")
    
'''
# okay fresh start/final draft

#Variables
client = openai.OpenAI(api_key="")
conversation_context = ""
DMC_system_prompt = ""
NL_system_prompt = ""
user_prompt = ""
nl_settings = chat.load_settings()
dmc_settings = decision_center.load_settings()

#start the loop
while True:

    if(len(conversation_context) > 5000):
        conversation_context = conversation_context[len(conversation_context) - 5000: len(conversation_context)]

    print("USER: ", end='')
    user_input = "USER: " + input()
    conversation_context += user_input + "\n"
    

    #QOL exit command
    if user_input.lower() == "exit":
        break

    #DMC
    DMC_system_prompt = dmc_settings['system_prompt'] + "CURRENT CONVERSATION CONTEXT: \n" + conversation_context + "AVAILABLE INSTRUCTIONS(CHOOSE FROM THESE ONLY): " + "".join(dmc_settings['available_instructions'])+ "RULES(FOLLOW THESE WHILE LISTING INSTRUCTIONS): " + "".join(dmc_settings['rules']) + "\n"
    
    #generate instructions, print for now
    instructions = decision_center.generate_instructions(DMC_system_prompt, user_input, client, True)
    print("\n")
    conversation_context += instructions

    #Generate filal output
    NL_system_prompt = nl_settings['system_prompt'] + nl_settings['personality'] + "CURRENT CONVERSATION CONTEXT: \n" + conversation_context + "\n"
    
    #print("NL PROMPT: ", NL_system_prompt)
    
    magnus_response = chat.generate_natural_output(NL_system_prompt, "EXECUTE THE FOLLOWING INSTRUCTiONS: " + instructions, client, True)
    conversation_context += magnus_response
    print("\n")

