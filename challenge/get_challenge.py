from flask_app.simple_db import db_save_challenge
from utils.gpt import llm


def get_prompt(description: str, p_language: str, language: str, difficulty: int, length: int):
    description_snippet = """
The user has provided a small description of the topic that he wants to learn / be challenged on:
### Start of description
{description}
### End of description""" if description else ""

    prompt = (r"""
You are an AI assistant that creates programming challenges in programming language {p_language} for a student who speaks {language}.

Here are some categories of challenges:
- the user has to write a function or script or code snippet from scratch
- the user has to extend a function or script or code snippet
- the user has to debug a function or script or code snippet
- the user has to document a function or script or code snippet

{description_snippet}

The user has set the difficulty level of the challenge to {difficulty} on a scale from 1 (easy for beginners) to 5 (hard for experts).
To be more precise: easy comes with a more verbose hint, more hand holding in the problem code and more common programming problems and standard code elements.
Hard problems are for experts where the problem is more challenging but also the user is expected to know most of the standard programming elements and libraries that are used.

The user has set the length of the challenge to {length} on a scale from 1 (short and quick) to 5 (long and involved) - but this applies to the length and required time of the solution, the assignment itself is usually short.

In general, be creative and do not use always the standard coding challenges.

Do not use any syntax / environment hints like ```{p_language} ... ```.
It is ok to expect knowledge of common non-standard libraries like numpy, torch etc. if the context and difficulty is appropriate and especially if the user requests it.

Please create the programming challenge in the following order:

- assignment (describe what the user has to do, make it clear if the user should write code, extend code or correct code, start right away with the assignment and not with a title)
- §TITLE§ (use this signal word to indicate that the title starts now)
- a title for the challenge (it should be long enough so that you do not generate too similar challenges in the future) -> no extra formatting
- §CODE§ (use this signal word to indicate that the problem code starts now)
- problem code (the code that the user has to extend or correct -> if the user has to write some code from scratch, leave this part blank or just write down an empty function, class etc.)
- §SOLUTION§ (use this signal word to indicate that the solution code starts now)
- solution (a correct solution code with comments explaining the code)
- §HINT§ (use this signal word to indicate that the hint starts now)
- hint (a hint to help the user solve the challenge)

### Start example 1 (programming language python, difficulty 1 (easy), length 1 (short), description: basics)

Please write correct the function string_length that calculates the length of a string.
§TITLE§
Function to calculate the length of a string
§CODE§
# Wrong function to correct
def string_length(string):
    return length(string)
§SOLUTION§
# Correct function 
def string_length(string):
    return len(string)
§HINT§
Remember the python function that calculates the length of a string.

### End example 1

### Start example 2 (programming language javascript, difficulty 3 (medium), length 3 (medium), description: arrays)

Please create a function named `mergeAndSortArrays` that takes two arrays of numbers as arguments. The function should merge the two arrays into one, eliminate any duplicates, and return the merged array sorted in ascending order. Ensure that you handle edge cases, such as when one or both arrays are empty. 
§TITLE§
Function to merge and sort arrays
§CODE§
// Write now your function:
function mergeAndSortArrays() {
}
§SOLUTION§
function mergeAndSortArrays(arr1, arr2) {
    // Merge the arrays using the spread operator
    const mergedArray = [...arr1, ...arr2];
    
    // Create a new Set to eliminate duplicates
    const uniqueArray = [...new Set(mergedArray)];
    
    // Sort the unique array in ascending order
    return uniqueArray.sort((a, b) => a - b);
}
§HINT§
Remember to use the spread operator to merge the arrays and the Set object to eliminate duplicates.

### End example 2

Please create now a programming challenge for the user with parameters programming language {p_language}, difficulty level {difficulty}/5, length {length}/5, description '{description}' (if any) and write everything in language {language}:
"""
              .replace("{p_language}", p_language)
              .replace("{language}", language)
              .replace("{difficulty}", str(difficulty))
              .replace("{length}", str(length))
              .replace("{description_snippet}", description_snippet)
              .replace("{description}", description)
              )
    return prompt


def get_challenge_stream(model="gpt-4o-mini", **kwargs):
    prompt = get_prompt(**kwargs)
    response_stream = llm.chat(prompt, stream=True, temperature=1.0, model=model)
    total_response = ""
    for event in response_stream:
        chunk = event.choices[0].delta.content
        if chunk:
            total_response += chunk
            yield chunk

    challenge = db_save_challenge(total_response, kwargs)

    yield f"§ID§{challenge.challengeId}§END§"
