import os
import psycopg2

from flask import Flask, jsonify
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
application = app

DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_URI = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}'
EMAIL_CHECK_QUERY = 'SELECT COUNT(email) FROM up_users WHERE LOWER(email) = LOWER(%s)'


def is_email_verified(email):
    conn = psycopg2.connect(
        host=DATABASE_HOST,
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD)

    cursor = conn.cursor()

    cursor.execute(EMAIL_CHECK_QUERY, (email,))
    result: int = cursor.fetchone()[0]
    return result


@application.route('/check_email/<path:email>')
def check_email(email):
    result = is_email_verified(email)
    return jsonify({'user_find': bool(result)})
