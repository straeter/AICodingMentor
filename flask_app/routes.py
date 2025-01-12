from flask import Blueprint, render_template, request, current_app, jsonify

from challenge.get_challenge import get_challenge_stream
from challenge.get_feedback import get_feedback_stream

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home', methods=['GET'])
def home():
    args = request.form

    return render_template(
        'home.html',
        page_title="AI Security Engineer - Home",

    )


@main.route('/get_challenge', methods=['POST'])
def get_challenge():
    data = request.json
    response_stream = get_challenge_stream(**data)
    return response_stream


@main.route('/get_feedback', methods=['POST'])
def get_feedback():
    data = request.json
    feedback_stream = get_feedback_stream(**data)
    return feedback_stream
