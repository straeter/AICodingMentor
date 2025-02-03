from flask_app.simple_db import db_update_challenge
from utils.gpt import llm


def get_feedback_prompt(assignment: str, attempt: str, p_language: str, language: str, difficulty: str,
                        code: str = None, **kwargs):
    code_snippet = ""
    if code:
        code_snippet: str = f"""
Code for the challenge:
{code}
"""

    prompt = f"""
You are an AI assistant that creates programming challenges in programming language {p_language} for a student who speaks {language}.

This was the challenge you gave the user that had difficulty level {difficulty}/5 (1 is easy for beginners and 5 is hard for experts):
##### Begin of challenge
{assignment}
{code_snippet}
##### End of challenge

This was the solution from the user:
##### Begin of solution
{attempt}
##### End of solution

Please provide feedback to the user. If the user's solution is correct, start your feedback with 'Correct!', otherwise you should give the users hints on how to improve their solution (without telling them directly the correct solution).
If the solution is correct, but you see some room for improvement or you see some bad programming habits, you should also give this feedback after you have written 'Correct!'.
The feedback should be short and specific to the errors / missing code (do not give a whole recipe etc.) and it should adapt to the user's level of programming knowledge indicated by the difficulty {difficulty}/5.
Start now with the assessment and feedback in language {language}:
"""
    return prompt


def get_feedback_stream(model="gpt-4o-mini", **kwargs):
    challengeId = kwargs.get("challengeId")
    attempt = kwargs.get("attempt")
    prompt = get_feedback_prompt(**kwargs)
    response_stream = llm.chat(prompt, stream=True, temperature=0.1, model=model)
    total_response = ""
    for event in response_stream:
        chunk = event.choices[0].delta.content
        if chunk:
            total_response += chunk
            yield chunk

    db_update_challenge(
        challengeId,
        attempt=attempt,
        feedback=total_response,
        status="solved" if total_response.startswith("Correct!") else "attempting",
    )

    yield "§END§"
