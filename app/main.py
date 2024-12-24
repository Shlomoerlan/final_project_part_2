from flask import Flask
from flask_cors import CORS
from app.routes.question_1_route import question_1_bp
from app.routes.question_2_route import question_2_bp
from app.routes.question_3_route import question_3_bp
from app.routes.question_4_route import question_4_bp
from app.routes.question_5_route import question_5_bp
from app.routes.question_6_route import question_6_bp
from app.routes.question_7_route import question_7_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(question_1_bp, url_prefix='/v1')
app.register_blueprint(question_2_bp, url_prefix='/v2')
app.register_blueprint(question_3_bp, url_prefix='/v3')
app.register_blueprint(question_4_bp, url_prefix='/v4')
app.register_blueprint(question_5_bp, url_prefix='/v5')
app.register_blueprint(question_6_bp, url_prefix='/v6')
app.register_blueprint(question_7_bp, url_prefix='/v7')



if __name__ == '__main__':
    app.run(port=5001, debug=True)