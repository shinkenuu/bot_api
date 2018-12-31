from uuid import UUID

from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from app import app, db
from schemas import BotSchema, MessageSchema


# TODO create uuid_validator decorator
@app.route('/messages/<string:message_uuid>')
def get_message(message_uuid: str):
    message_uuid = _validate_uuid(message_uuid)

    if message_uuid is None:
        return jsonify({'error': 'Invalid message id'}), 400

    message = db.messages.find_one({'message_uuid': message_uuid})

    if not message:
        return jsonify({'error': 'No message with id ' + str(message_uuid)}), 404

    serialized_message = MessageSchema().dump(message)

    return jsonify(serialized_message), 200


# TODO create uuid_validator decorator
@app.route('/messages', methods=['GET'])
def get_conversation_messages():
    raw_conversation_uuid = request.args.get('conversationId')

    if not raw_conversation_uuid:
        return jsonify({'error': '"conversationId" argument was not found'}), 400

    conversation_uuid = _validate_uuid(raw_conversation_uuid)

    if conversation_uuid is None:
        return jsonify({'error': 'Invalid conversationId'}), 400

    messages_cursor = db.messages.find({'conversation_uuid': conversation_uuid})
    deserialized_messages = list(messages_cursor)

    if not deserialized_messages:
        return jsonify({'error': 'No messages from conversationId ' + str(conversation_uuid)}), 404

    serialized_messages = MessageSchema(many=True).dump(deserialized_messages)

    return jsonify(serialized_messages), 200


@app.route('/messages', methods=['POST'])
def post_message():
    raw_message = request.get_json()

    try:
        message = MessageSchema().load(raw_message)
    except ValidationError as error:
        return jsonify({'error': str(error)}), 400

    db.messages.insert_one(message)

    serialized_message = MessageSchema().dump(message)

    return jsonify(serialized_message), 201


class BotDetail(Resource):

    # TODO create uuid_validator decorator
    @staticmethod
    def get(id: str):

        bot_uuid = _validate_uuid(id)

        if bot_uuid is None:
            return {'error': 'Invalid bot id'}, 400

        bot = db.bots.find_one({'bot_uuid': bot_uuid})

        if bot is None:
            return None, 404

        serialized_bots = BotSchema().dump(bot)

        return serialized_bots

    # TODO create uuid_validator decorator
    @staticmethod
    def put(id: str):

        bot_uuid = _validate_uuid(id)

        if bot_uuid is None:
            return {'error': 'Invalid bot id'}, 400

        persisted_bot = db.bots.find_one({'bot_uuid': bot_uuid})

        if not persisted_bot:
            return None, 404

        raw_bot = request.get_json()

        try:
            bot = BotSchema().load(raw_bot)
        except ValidationError as error:
            return {'error': str(error)}, 400

        db.bots.update_one({'bot_uuid': bot_uuid}, {'$set': bot})

        serialized_bot = BotSchema().dump(bot)

        return serialized_bot, 202

    # TODO create uuid_validator decorator
    @staticmethod
    def delete(id: str):

        bot_uuid = _validate_uuid(id)

        if bot_uuid is None:
            return {'error': 'Invalid bot id'}, 400

        bot = db.bots.find_one({'bot_uuid': bot_uuid})

        if not bot:
            return None, 404

        db.bots.delete_one({'bot_uuid': bot_uuid})

        return None, 204


class BotList(Resource):

    @staticmethod
    def post():
        raw_bot = request.get_json()

        try:
            bot = BotSchema().load(raw_bot)
        except ValidationError as error:
            return {'error': str(error)}, 400

        existing_bot = db.bots.find_one({'bot_uuid': bot['bot_uuid']})

        if existing_bot:
            return {'error': 'Bot with id ' + bot['bot_uuid'] + ' already registered'}, 400

        db.bots.insert_one(bot)

        serialized_bot = BotSchema().dump(bot)

        return serialized_bot, 201


def _validate_uuid(uuid_to_validate: str):
    """
    Validate ```uuid_to_validate``` against UUID format.
    :param str uuid_to_validate:
    :return: UUID(```uuid_to_validate```) if valid, `None` otherwise
    """
    try:
        valid_uuid = UUID(uuid_to_validate)
    except ValueError:
        valid_uuid = None

    return valid_uuid
