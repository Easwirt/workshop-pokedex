import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

User = get_user_model()

class PokemonConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        user_id = self.scope['user'].id
        user = User.objects.get(pk=user_id)
        user.online_status += 1
        user.save()

        self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': 'online',
        }))

    def disconnect(self, close_code):
        user_id = self.scope['user'].id
        user = User.objects.get(pk=user_id)
        if(user.online_status > 0):
            user.online_status -= 1
        user.save()
        self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': 'offline',
        }))

    def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get('username')
        status = data.get('status')

        # You can handle the received username and status here
        print(f'Received username: {username}, status: {status}')
        status = User.objects.get(username=username).online_status

        # Optionally, send a response back to the client
        self.send(text_data=json.dumps({
            'message': f'{status}'
        }))
