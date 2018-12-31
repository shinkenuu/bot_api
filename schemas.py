from marshmallow import fields, Schema, EXCLUDE


class BotSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    bot_uuid = fields.UUID(required=True, data_key='id')
    name = fields.Str(required=True)


class MessageSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    message_uuid = fields.UUID(required=True, data_key='id')
    conversation_uuid = fields.UUID(required=True, data_key='conversationId')
    timestamp = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S.%fZ')
    sender_uuid = fields.UUID(required=True, data_key='from')
    receiver_uuid =  fields.UUID(required=True, data_key='to')
    text = fields.Str(required=True)
