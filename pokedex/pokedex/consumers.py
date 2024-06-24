import asyncio
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from minigame.models import Fight
from asgiref.sync import sync_to_async
import time
# from channels.db import database_sync_to_async

def get_user():
    return get_user_model()

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
        if user.online_status > 0:
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

        status = User.objects.get(username=username).online_status

        self.send(text_data=json.dumps({
            'message': f'{status}'
        }))


class FightConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.fight_id = self.scope['url_route']['kwargs']['fight_id']
        self.fight_group_name = f'fight_{self.fight_id}'

        await self.channel_layer.group_add(
            self.fight_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.fight_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']

        if action == 'click':
            await self.update_fight_state()

    async def update_fight_state(self):
        fight = await self.get_fight_object()
        fight.clicks += 1
        fight.health -= 2
        
        if fight.health <= 0:
            fight.status = 2
            await fight.victory()

        elif fight.time == 0:
            fight.status = 0
            await fight.lose()

        await sync_to_async(fight.save)()

        await self.channel_layer.group_send(
            self.fight_group_name,
            {
                'type': 'fight_update',
                'fight_state': {
                    'clicks': fight.clicks,
                    'health': fight.health,
                    'status': fight.status,
                }
            }
        )


    # async def periodic_update(self):
    #     while True:
    #         await asyncio.sleep(1)
    #         fight = await self.get_fight_object()
    #         if fight.status in [0, 2]:
    #             break
    #         fight.health = min(fight.max_health, fight.health + 1)
    #         fight.time -= 1

    #         if fight.time <= 0:
    #             fight.status = 0
    #             await fight.lose()

    #         await database_sync_to_async(fight.save)()

    #         await self.send_fight_state(fight)
    
    async def fight_update(self, event):
        fight_state = event['fight_state']

        await self.send(text_data=json.dumps({
            'clicks': fight_state['clicks'],
            'health': fight_state['health'],
            'status': fight_state['status'],

        }))

    @sync_to_async
    def get_fight_object(self):
        fight_id = int(self.fight_id)
        return Fight.objects.get(id=fight_id)
    