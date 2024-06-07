import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

def get_user():
    return get_user_model()

# Now you can use get_user() wherever you need to access the User model


class PokemonConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        User = get_user()

        user_id = self.scope['user'].id
        user = User.objects.get(pk=user_id)
        user.online_status += 1
        user.save()

        self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': 'online',
        }))

    def disconnect(self, close_code):
        User = get_user()
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
        User = get_user()
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
