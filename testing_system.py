import llm
import openai
import chat
import decision_center
import json

# okay fresh start/final draft

#Variables
client = openai.OpenAI(api_key="")
#client = openai.OpenAI(api_key="")
conversation_context = ""
DMC_system_prompt = ""
NL_system_prompt = ""
user_prompt = ""
nl_settings = chat.load_settings()
dmc_settings = decision_center.load_settings()



#start the loop
i = 1;
while(i < 21):
    print("-------------------------------------------------------")
    with open('tester.json') as f:
        test_settings = json.load(f)

    conversation_context = "\n".join(test_settings['context'])

    #print("USER: ", end='')
    #user_input = "USER: " + input()
    user_input = "THIS IS A TEST, PLEASE RESPOND TO THE CONTEXT AS IF IT IS OUR CURRENT CONVERSATION"
    conversation_context += user_input + "\n"
    

    #QOL exit command
    if user_input.lower() == "exit":
        break

    #DMC
    DMC_system_prompt = dmc_settings['system_prompt'] + "CURRENT CONVERSATION CONTEXT: \n" + conversation_context + "AVAILABLE INSTRUCTIONS(CHOOSE FROM THESE ONLY): " + "".join(dmc_settings['available_instructions'])+ "RULES(FOLLOW THESE WHILE LISTING INSTRUCTIONS): " + "".join(dmc_settings['rules']) + "\n" + "RELEVANT MEMORIES(USE THESE TO INFORM DECISIONS): " + "\n".join(test_settings['relevant_memories']) + "\n" + "CURRENT TIME: " + test_settings["current_time"] + "\n" + "CURRENT USER: " + dmc_settings["current_user"] + "\n"
    
    #generate instructions, print for now
    instructions = decision_center.generate_instructions(DMC_system_prompt, user_input, client, False)
    
    conversation_context += instructions
    print("RESULTS OF TEST " + str(i) + ":")
    print("DMC: ", instructions)
    #update json file

    #Generate filal output
    NL_system_prompt = nl_settings['system_prompt'] + nl_settings['personality'] + "CURRENT CONVERSATION CONTEXT: \n" + conversation_context + "\n"
    
    #print("NL PROMPT: ", NL_system_prompt)
    
    magnus_response = chat.generate_natural_output(NL_system_prompt, "EXECUTE THE FOLLOWING INSTRUCTiONS: " + instructions, client, False)
    conversation_context += magnus_response
    print("\n")
    print("NLP: ", magnus_response)

    #json.dump(test_settings, f)
    i += 1


