
# 定义API Key和Secret Key
APP_ID = '40079341'     #ID短号
API_KEY = '0f5GrnbmAHsksnagaUDpFW3l'  #无规律很长
SECRET_KEY = 'P4MNGHY2m17X3QUUiOaFcxnqhcgSnCTL'   #无规律很长

import base64
import requests
import face_recognition

class FaceAnalysis:
    def __init__(self, app_id='40079341', api_key='0f5GrnbmAHsksnagaUDpFW3l', secret_key='P4MNGHY2m17X3QUUiOaFcxnqhcgSnCTL'):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = self.get_access_token()

    def get_access_token(self):
        # 获取access_token
        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}'
        response = requests.get(host)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception("Failed to get access token")

    def analyze_face(self, image_data):
        # 将图片文件转换为base64编码
        base64_data = base64.b64encode(image_data)

        # 调用百度API进行人脸识别
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        params = {
            "image": base64_data,
            "image_type": "BASE64",
            "face_field": "age,beauty,expression,face_shape,gender,glasses,emotion,face_type,spoofing",
            "face_type": "LIVE"
        }
        request_url = request_url + "?access_token=" + self.access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response.status_code == 200:
            face_result = response.json()
            return face_result['result']['face_list'][0]
        else:
            raise Exception("Failed to analyze the face")

