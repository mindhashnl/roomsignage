from channels.generic.websocket import WebsocketConsumer
import json


class ScreenConsumer(WebsocketConsumer):
    def connect(self):
        print('CONNECTED!!')
        self.accept()

    def disconnect(self, close_code):
        print("DISCONNECTED!!")
        pass

    def receive(self, text_data):
        print("DID RECEIVE!")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
