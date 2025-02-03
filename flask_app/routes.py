from flask import Blueprint, render_template, request, current_app, jsonify, stream_with_context, Response

from challenge.get_challenge import get_challenge_stream
from challenge.get_feedback import get_feedback_stream
from flask_app.simple_db import db_get_challenge, db_delete_challenge

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home', methods=['GET'])
def home():
    challengeId = request.args.get("challengeId")
    if challengeId:
        challenge = db_get_challenge(challengeId)
    else:
        challenge = None

    return render_template(
        'home.html',
        page_title="AICodingMentorg - Home",
        challenge=challenge
    )


@main.route('/get_challenge', methods=['POST'])
def get_challenge():
    data = request.json
    model=current_app.config["LLM_MODEL"]
    response_stream = get_challenge_stream(model=model, **data)
    # return response_stream

    return Response(stream_with_context(response_stream), mimetype='text/plain')


@main.route('/get_feedback', methods=['POST'])
def get_feedback():
    data = request.json
    model=current_app.config["LLM_MODEL"]
    feedback_stream = get_feedback_stream(model=model, **data)
    return feedback_stream


# @main.route('/history', methods=['GET'])
# def home():
#     return render_template(
#         'history.html',
#         page_title="AICodingMentorg - History",
#         challenges=challenges
#     )

@main.route('/challenge/delete/<challengeId>', methods=['POST'])
def delete_challenge(challengeId):
    success = db_delete_challenge(challengeId)
    if success:
        return jsonify({"message": "Challenge deleted successfully"}, 201)
    else:
        return jsonify({"message": "Challenge not found"}, 404)
