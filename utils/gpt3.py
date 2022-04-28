import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def query_gpt3(prompt):
    gpt_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
            )
    return gpt_response["choices"][0]["text"]

def extract_keywords(question):
    """
    Returns list of 10 keywords of the question.
    E.g. ['deploy', 'contract', 'problem', 'create', 'hardhat', 'command', 'mumbai', 'scripts']
    """
    query = f"""
        Question asked: {question} \n
        11 keywords in this question: \n
        web3
    """
    gpt3_response = query_gpt3(query)
    keywords = gpt3_response.split('\n')
    parsed_keywords = list(filter(lambda x: x != '' and ' ' not in x and ':' not in x, [word.strip() for word in keywords]))
    print("keywords: ", parsed_keywords)
    return parsed_keywords[0:11]

example_q_1 = """
Hi! I have been creating a contract for several days and have used the command 
"npx hardhat run scripts/deploy.js --network mumbai" dozens of times to create 
test contracts. But unfortunately since yesterday despite the fact that I did not 
change anything in the configuration, no contract is deployed. You have to know that 
when I run the command it sometimes writes "13 Solidity scripts compiled successfully" 
and it also creates the Artifacts folder, but it never goes any further and the 
contract is not depolished... Any ideas how to solve this?
"""

#print(extract_keywords(example_q_1))