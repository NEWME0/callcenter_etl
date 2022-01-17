from marshmallow import Schema, fields


class ExtensionAgentSchema(Schema):
    """ExtensionAgent Schema"""

    pbx_id = fields.String(required=True)
    fullname = fields.String(required=True)
    extension = fields.String(required=True)


class ExtensionGroupSchema(Schema):
    """ExtensionGroup Schema"""
