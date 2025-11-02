import os
from flask import Flask, Response
from flask_restful import Api
from flask_cors import CORS
from api.create_image import CreateImage
from api.area_crawling import areaCrawling
from api.chat_AI import ChatAI
from api.face_emotion import FaceEmotion
from api.recipeCrawling_Api import recipeCrawlingAPI
from api.text_emotion_detect import TextEmotionDetection
from api.Weather_Info import weather_info
from api.food_ocr import foodOcr
from api.OCR import inOcr
from api.recipeCrawling_csv import fileNrecipeCrawling
from api.Food_recommendation import food_recommend
from api.kin_crawling import kinCrawling
from api.wordcloud3d import wordcloudtest
from api.youtude_crawling import youtudeCrawling
from api.Exercise_recommendation import recommendExercise
from api.wrtnai_crawling import wrtnCrawling
from api.exercise_crawling import exerciseCrawling
from api.recommendMate import recommendMate
from api.ttest import ttest
from api.summary_api import summaryAPI
from api.PoseDetector import PoseDetector

from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

# 플라스크 앱 생성
app = Flask(__name__)

SWAGGER_URL = '/api/docs'
API_URL = '/api/spec'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My App",
        "version": 1.0
    }
)

app.register_blueprint(blueprint=swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# CORS에러 처리
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)


@app.route("/api/spec")
def serve_openapi_yaml():
    with open(os.environ.get("SWAGGER_YAML_PATH"), "r", encoding="utf-8") as f:
        return Response(f.read(), mimetype="application/yaml")


api.add_resource(CreateImage, '/CreateIm')
api.add_resource(areaCrawling, '/areaCrawling')
api.add_resource(ChatAI, '/ChatAI')
api.add_resource(recipeCrawlingAPI, '/recipeCrawlingAPI')
api.add_resource(TextEmotionDetection, '/diary')
api.add_resource(weather_info, '/weatherInfo')
api.add_resource(foodOcr, '/foodOcr')
api.add_resource(inOcr, '/ocr')

api.add_resource(fileNrecipeCrawling, '/fileNrecipeCrawling')
api.add_resource(FaceEmotion, '/test')
api.add_resource(food_recommend, '/food_recommend')
api.add_resource(kinCrawling, '/kinCrawling')
api.add_resource(wordcloudtest, '/wordcloud')
api.add_resource(youtudeCrawling, '/youtudeCrawling')
api.add_resource(recommendExercise, '/recommendExercise')
api.add_resource(wrtnCrawling, '/wrtnCrawling')
api.add_resource(exerciseCrawling, '/exerciseCrawling')
api.add_resource(recommendMate, '/recommendMate')
api.add_resource(ttest, '/ttest')
api.add_resource(summaryAPI, '/summaryAPI')
api.add_resource(PoseDetector, '/PoseDetector')
api.decorators = [CORS()]

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
