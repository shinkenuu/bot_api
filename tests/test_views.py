from datetime import datetime
from uuid import UUID, uuid4
from unittest import TestCase

import mock

from app import app, db


class MessageViewTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.serialized_message = {
            'id': '67ade836-ea2e-4992-a7c2-f04b696dc9ff',
            'conversationId': '7665ada8-3448-4acd-a1b7-d688e68fe9a1',
            'timestamp': '2018-11-16T23:30:57.000000Z',
            'from': '16edd3b3-3f75-40df-af07-2a3813a79ce9',
            'to': '36b9f842-ee97-11e8-9443-0242ac120002',
            'text': 'Gostaria de saber meu saldo',
        }

        self.deserialized_message = {
            'message_uuid': UUID('67ade836-ea2e-4992-a7c2-f04b696dc9ff'),
            'conversation_uuid': UUID('7665ada8-3448-4acd-a1b7-d688e68fe9a1'),
            'timestamp': datetime(2018, 11, 16, 23, 30, 57, 0),
            'sender_uuid': UUID('16edd3b3-3f75-40df-af07-2a3813a79ce9'),
            'receiver_uuid': UUID('36b9f842-ee97-11e8-9443-0242ac120002'),
            'text': 'Gostaria de saber meu saldo',
        }

    def tearDown(self):
        db.messages.delete_many({})

    @mock.patch('views._validate_uuid')
    def test_get_message_calls_validate_uuid(self, mock_validate_uuid):
        uuid = uuid4()
        mock_validate_uuid.return_value = uuid

        self.client.get('/messages/' + str(uuid))

        mock_validate_uuid.assert_called_once_with(str(uuid))

    @mock.patch('views._validate_uuid')
    def test_get_conversation_messages_calls_validate_uuid(self, mock_validate_uuid):
        uuid = uuid4()
        mock_validate_uuid.return_value = uuid

        self.client.get('/messages?conversationId=' + str(uuid))

        mock_validate_uuid.assert_called_once_with(str(uuid))

    def test_get_unspecified_conversation_uuid_returns_400(self):
        response = self.client.get('/messages')
        self.assertEqual(response.status_code, 400)

    def test_get_message_with_invalid_uuid_returns_400(self):
        response = self.client.get('/messages/invalid-uuid')
        self.assertEqual(response.status_code, 400)

    def test_get_existing_message_returns_the_message(self):
        noisy_message = self.deserialized_message.copy()
        noisy_message['message_uuid'] = uuid4()

        db.messages.insert_many([self.deserialized_message, noisy_message])

        response = self.client.get('/messages/' + str(self.deserialized_message['message_uuid']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.serialized_message)

    def test_get_non_existing_message_returns_404(self):
        random_uuid = str(uuid4())
        response = self.client.get('/messages/' + random_uuid)
        self.assertEqual(response.status_code, 404)

    def test_get_messages_from_conversation_with_invalid_uuid_returns_400(self):
        response = self.client.get('/messages?conversationId=invalid-uuid')
        self.assertEqual(response.status_code, 400)

    def test_get_messages_from_existing_conversation_returns_all_messages_from_conversation(self):
        message_from_same_conversation = self.deserialized_message.copy()
        message_from_same_conversation['text'] = 'Alou?'

        message_from_another_conversation = self.deserialized_message.copy()
        message_from_another_conversation['conversation_uuid'] = uuid4()

        db.messages.insert_many([self.deserialized_message,
                                 message_from_same_conversation,
                                 message_from_another_conversation])

        serialized_message_from_same_conversation = self.serialized_message.copy()
        serialized_message_from_same_conversation['text'] = 'Alou?'

        expected_payload = [
            self.serialized_message,
            serialized_message_from_same_conversation,
        ]

        response = self.client.get(
            '/messages?conversationId=' + str(message_from_same_conversation['conversation_uuid']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_payload)

    def test_get_messages_from_non_existing_conversation_returns_404(self):
        random_uuid = str(uuid4())
        response = self.client.get('/messages?conversationId=' + random_uuid)
        self.assertEqual(response.status_code, 404)

    def test_post_new_message_persists_message_and_returns_201(self):
        response = self.client.post('/messages', json=self.serialized_message)

        self.assertEqual(response.status_code, 201)

        persisted_message = db.messages.find_one({'message_uuid': self.deserialized_message['message_uuid']})
        persisted_message.pop('_id')

        self.assertEqual(persisted_message, self.deserialized_message)

    def test_post_invalid_message_schema_returns_400(self):
        message_with_invalid_schema = self.serialized_message.copy()
        message_with_invalid_schema['unknown_field'] = message_with_invalid_schema.pop('id')

        response = self.client.post('/messages', json=message_with_invalid_schema)

        self.assertEqual(response.status_code, 400)


class BotViewTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.serialized_bot = {
            'id': '36b9f842-ee97-11e8-9443-0242ac120002',
            'name': 'Aureo',
        }

        self.deserialized_bot = {
            'bot_uuid': UUID('36b9f842-ee97-11e8-9443-0242ac120002'),
            'name': 'Aureo',
        }

    def tearDown(self):
        db.bots.delete_many({})

    def test_post_new_bot_persists_bot_and_returns_201(self):
        response = self.client.post('/bots', json=self.serialized_bot)

        self.assertEqual(response.status_code, 201)

        persisted_bot = db.bots.find_one({'bot_uuid': self.deserialized_bot['bot_uuid']})
        persisted_bot.pop('_id')

        self.assertEqual(persisted_bot, self.deserialized_bot)

    def test_post_existing_bot_do_not_persist_and_returns_400(self):
        bot_with_same_uuid = self.deserialized_bot.copy()
        bot_with_same_uuid['name'] = 'Random name to differentiate'

        db.bots.insert_one(self.deserialized_bot)

        response = self.client.post('/bots', json=bot_with_same_uuid)

        self.assertEqual(response.status_code, 400)

        persisted_bot = db.bots.find_one({'bot_uuid': self.deserialized_bot['bot_uuid']})
        self.assertEqual(persisted_bot, self.deserialized_bot)

    def test_post_invalid_bot_schema_returns_400(self):
        invalid_bot = self.serialized_bot.copy()
        invalid_bot['unknown_field'] = invalid_bot.pop('id')

        response = self.client.post('/bots', json=invalid_bot)

        self.assertEqual(response.status_code, 400)

    def test_get_existing_bot_returns_the_bot(self):
        noisy_bot = self.deserialized_bot.copy()
        noisy_bot['name'] = 'Another bot not to be returned'

        db.bots.insert_many([self.deserialized_bot, noisy_bot])

        response = self.client.get('/bots/' + str(self.deserialized_bot['bot_uuid']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.serialized_bot)

    def test_get_non_existing_bot_returns_404(self):
        response = self.client.get('/bots/' + str(self.deserialized_bot['bot_uuid']))
        self.assertEqual(response.status_code, 404)

    def test_get_bot_with_invalid_uuid_returns_400(self):
        response = self.client.get('/bots/invalid-uuid')
        self.assertEqual(response.status_code, 400)

    def test_put_existing_bot_updates_bot_and_returns_202(self):
        db.bots.insert_one(self.deserialized_bot)

        self.serialized_bot['name'] = 'Different name'

        response = self.client.put('/bots/' + self.serialized_bot['id'], json=self.serialized_bot)

        self.assertEqual(response.status_code, 202)

        updated_bot = db.bots.find_one({'bot_uuid': self.deserialized_bot['bot_uuid']})

        self.assertEqual(updated_bot['name'], self.serialized_bot['name'])

    def test_put_non_existing_bot_returns_404(self):
        response = self.client.put('/bots/' + self.serialized_bot['id'], json=self.serialized_bot)
        self.assertEqual(response.status_code, 404)

    def test_put_bot_with_invalid_uuid_returns_400(self):
        self.serialized_bot['id'] = 'invalid-uuid'
        response = self.client.put('/bots/' + self.serialized_bot['id'], json=self.serialized_bot)
        self.assertEqual(response.status_code, 400)

    def test_put_bot_with_invalid_schema_returns_400(self):
        db.bots.insert_one(self.deserialized_bot)

        self.serialized_bot['unknown_field'] = self.serialized_bot.pop('name')

        response = self.client.put('/bots/' + self.serialized_bot['id'], json=self.serialized_bot)

        self.assertEqual(response.status_code, 400)

    def test_delete_existing_bot_deletes_bot_and_returns_204(self):
        db.bots.insert_one(self.deserialized_bot)

        response = self.client.delete('/bots/' + self.serialized_bot['id'])
        self.assertEqual(response.status_code, 204)

        self.assertIsNone(db.bots.find_one({'bot_uuid': UUID(self.serialized_bot['id'])}))

    def test_delete_non_existing_bot_returns_404(self):
        response = self.client.delete('/bots/' + self.serialized_bot['id'])
        self.assertEqual(response.status_code, 404)

    def test_delete_bot_with_invalid_uuid_returns_400(self):
        db.bots.insert_one(self.deserialized_bot)

        self.serialized_bot['id'] = 'invalid-uuid'

        response = self.client.delete('/bots/' + self.serialized_bot['id'])

        self.assertEqual(response.status_code, 400)
