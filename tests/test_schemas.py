from bson import ObjectId
from datetime import datetime
from unittest import TestCase
from uuid import UUID

from schemas import BotSchema, MessageSchema


class BotSchemaTestCase(TestCase):
    def test_deserialization(self):
        serialized_bot = {
            'id': '36b9f842-ee97-11e8-9443-0242ac120002',
            'name': 'Aureo',
        }

        deserialized_bot = BotSchema().load(serialized_bot)

        self.assertEqual(deserialized_bot['bot_uuid'], UUID('36b9f842-ee97-11e8-9443-0242ac120002'))
        self.assertEqual(deserialized_bot['name'], 'Aureo')
        
    def test_serialization(self):
        deserialized_bot = {
            '_id': ObjectId(),
            'bot_uuid': '36b9f842-ee97-11e8-9443-0242ac120002',
            'name': 'Aureo',
        }

        serialized_bot = BotSchema().dump(deserialized_bot)

        self.assertEqual(serialized_bot['id'], '36b9f842-ee97-11e8-9443-0242ac120002')
        self.assertEqual(serialized_bot['name'], 'Aureo')


class MessageSchemaTestCase(TestCase):
    def test_deserialization(self):
        serialized_message = {
            'id': '4085e1c9-842f-4274-a617-70a1e2023e2e',
            'conversationId': '7665ada8-3448-4acd-a1b7-d688e68fe9a1',
            'timestamp': '2018-11-16T23:30:52.691722Z',
            'from': '36b9f842-ee97-11e8-9443-0242ac120002',
            'to': '16edd3b3-3f75-40df-af07-2a3813a79ce9',
            'text': 'Oi! Como posso te ajudar?'
        }

        deserialized_message = MessageSchema().load(serialized_message)

        self.assertEqual(serialized_message['id'], '4085e1c9-842f-4274-a617-70a1e2023e2e')
        self.assertEqual(deserialized_message['conversation_uuid'], UUID('7665ada8-3448-4acd-a1b7-d688e68fe9a1'))
        self.assertEqual(deserialized_message['timestamp'], datetime(2018, 11, 16, 23, 30, 52, 691722))
        self.assertEqual(deserialized_message['sender_uuid'], UUID('36b9f842-ee97-11e8-9443-0242ac120002'))
        self.assertEqual(deserialized_message['receiver_uuid'], UUID('16edd3b3-3f75-40df-af07-2a3813a79ce9'))
        self.assertEqual(deserialized_message['text'], 'Oi! Como posso te ajudar?')

    def test_serialization(self):
        deserialized_message = {
            '_id': ObjectId(),
            'message_uuid': '4085e1c9-842f-4274-a617-70a1e2023e2e',
            'conversation_uuid': '7665ada8-3448-4acd-a1b7-d688e68fe9a1',
            'timestamp': datetime(2018, 11, 16, 23, 30, 52, 691722),
            'sender_uuid': '36b9f842-ee97-11e8-9443-0242ac120002',
            'receiver_uuid': '16edd3b3-3f75-40df-af07-2a3813a79ce9',
            'text': 'Oi! Como posso te ajudar?'
        }

        serialized_message = MessageSchema().dump(deserialized_message)

        self.assertEqual(serialized_message['id'], '4085e1c9-842f-4274-a617-70a1e2023e2e')
        self.assertEqual(serialized_message['conversationId'], '7665ada8-3448-4acd-a1b7-d688e68fe9a1')
        self.assertEqual(serialized_message['timestamp'], '2018-11-16T23:30:52.691722Z')
        self.assertEqual(serialized_message['from'], '36b9f842-ee97-11e8-9443-0242ac120002')
        self.assertEqual(serialized_message['to'], '16edd3b3-3f75-40df-af07-2a3813a79ce9')
        self.assertEqual(serialized_message['text'], 'Oi! Como posso te ajudar?')
