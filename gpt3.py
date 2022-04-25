import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def query_gpt3(prompt):
    gpt_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        # logprobs=5,
        stop=["\n"],
    )
    return gpt_response["choices"][0]["text"]