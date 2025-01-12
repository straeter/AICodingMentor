from utils.gpt import llm


def get_prompt(description: str, p_language: str, language: str, difficulty: int, length: int):
    description_snippet = f"""
The user has provided a small description of the topic that he wants to learn / be challenged on:
### Start of description
{description}
### End of description""" if description else ""

    prompt = f"""
You are an AI assistant that creates programming challenges in programming language {p_language} for a student who speaks {language}.

Here are some categories of challenges:
- the user has to write a small function or script or code snippet
- the user has to extend a function or script or code snippet
- the user has to debug a function or script or code snippet
- the user has to document a function

{description_snippet}

The user has set the difficulty level of the challenge to {difficulty} on a scale from 1 (easy for beginners) to 5 (hard for experts).
The user has set the length of the challenge to {length} on a scale from 1 (short and quick) to 5 (long and involved).

Do not use any syntax / environment hints like ```python ... ```.
It is ok to expect knowledge of common non-standard libraries like numpy, torch etc. if the context and difficulty is appropriate and especially if the user requests it.

Please create the programming challenge in the following order:

- assignment (describe what the user has to do, make it clear if the user should write code, extend code or correct code, start right away with the assignment and not with a title)
- !!!!! (5 exclamation marks to separate the assignment from the code)
- problem code (the code that the user has to extend or correct -> if the user has to write some code from scratch, leave this part blank. )
- ????? (5 question marks to seperate the code snippet from the solution)
- solution (a correct solution to the code with comments explaining the code)
- §§§§§ (5 section signs to separate the solution from the hint)
- hint (a hint to help the user solve the challenge)

### Start example (programming language Python, difficulty level 1 (easy), description: basics)

Please write a small function to return the length of a string
!!!!!
?????
def string_length(string):
    return len(string)
§§§§§
Remember the python function that calculates the length of a string.

### End example

Please create now a programming challenge for the user with parameters programming language {p_language}, difficulty level {difficulty}/5, length {length}/5, description '{description}' and write everything in language {language}:
"""
    return prompt


def get_challenge_stream(**kwargs):
    prompt = get_prompt(**kwargs)
    response_stream = llm.chat(prompt, stream=True, temperature=1.0)
    for event in response_stream:
        chunk = event.choices[0].delta.content
        if chunk:
            yield chunk
    yield "&&&"
