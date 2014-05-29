def array_or_item(obj):
    """Generate a Python list for use in JSON Schema oneOf declarations"""
    return [obj, {"$ref": "#/definitions/arrayMinOne", "items": obj}]

MAPV3 = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "DPLA Metadata Application Profile v3 JSON Schema",
    "id": "http://api.dp.la/schemas/mapv3#", 
    "type": "object",
    # Recommended: store these at dereferenceable URIs
    "oneOf": [
        {"$ref": "#/definitions/item"},
        {"$ref": "#/definitions/collection"}
    ],
    "definitions": {
        "arrayMinOne": {
            "type": "array",
            "minItems": 1
        },
        "arrayOrString": {"oneOf": array_or_item({"type": "string"})},
        "collection": {
            "type": "object",
            "required": ["@id", "title"],
            "properties": {
                "@context": {"type": ["string", "object"]},
                "@id": {"type": "string", "format": "uri"},
                "_id": {"type": "string"},
                "_rev": {"type": "string"},
                "description": {"$ref": "#/definitions/arrayOrString"},
                "ingestionSequence": {"type": "number"},
                "ingestDate": {"type": "string", "format": "date-time"},
                "ingestType": {"type": "string", "enum": ["collection"]},
                "id": {"type": "string"},
                "title": {"$ref": "#/definitions/arrayOrString"}
            },
            "additionalProperties": False
        },
        "date": {
            "type": "object",
            "properties": {
                "begin": { "type": ["string", "null"] },
                "displayDate": { "type": ["string", "null"] },
                "end": { "type": ["string", "null"] }
            },
            "additionalProperties": False
        },
        "hasView": {
            "type": "object",
            "required": ["@id", "format"],
            "properties": {
                "@id": {"type": "string", "format": "uri"},
                "format": {"type": ["string", "null"]},
                "rights": {"$ref": "#/definitions/arrayOrString"}
            },
            "additionalProperties": False
        },
        "item": {
            "type": "object",
            "required": [
                "@context",
                "@id",
                "dataProvider",
                "id",
                "ingestionSequence",
                "isShownAt",
                "object",
                "originalRecord",
                "sourceResource"
            ],
            "properties": {
                "@context": {"type": ["string", "object"]},
                "@id": {"type": "string", "format": "uri"},
                "@type": {"type": "string", "enum": ["ore:Aggregation"]},
                "_id": {"type": "string"},
                "_rev": {"type": "string"},
                "admin": {"type": "object"}, # remove?
                "aggregatedCHO": {"type": "string", "format": "uri"},
                "dataProvider": {"$ref": "#/definitions/arrayOrString"},
                "hasView": {
                    "oneOf": array_or_item({"$ref": "#/definitions/hasView"})
                },
                "id": {"type": "string"},
                "ingestionSequence": {"type": "number"},
                "ingestDate": {"type": "string", "format": "date-time"},
                "ingestType": {"type": "string", "enum": ["item"]},
                "isShownAt": {"type": "string", "format": "uri"},
                "object": {"type": "string", "format": "uri"},
                "originalRecord": {
                    "type": "object",
                    "additionalProperties": True
                },
                "provider": {
                    "type": "object",
                    "required": ["@id", "name"],
                    "properties":{
                        "@id": {"type": "string", "format": "uri"},
                        "name": {"type": "string"}
                    }
                },
                "sourceResource": {"$ref": "#/definitions/sourceResource"}
            }
        },
        "sourceResource": {
            "type": "object",
            "required": [
                "rights", # Many records are still missing rights
                "title"
            ],
            "additionalProperties": False,
            "properties": {
                "@id": {"type": "string", "format": "uri"},
                "collection": {
                    "oneOf": array_or_item({"$ref": "#/definitions/collection"})
                },
                "contributor": {"$ref": "#/definitions/arrayOrString"},
                "creator": {"$ref": "#/definitions/arrayOrString"},
                "date": {
                    "oneOf": array_or_item({"$ref": "#/definitions/date"})
                },
                "description": {"$ref": "#/definitions/arrayOrString"},
                "extent": {"$ref": "#/definitions/arrayOrString"},
                "format": {"$ref": "#/definitions/arrayOrString"},
                "identifier": {"$ref": "#/definitions/arrayOrString"},
                "language": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["name"],
                        "properties": {
                            "name": { "type": "string" },
                            "iso639_3": {
                                "type": "string",
                                "minLength": 3,
                                "maxLength": 3
                            }
                        }
                    }
                },
                "publisher": {"$ref": "#/definitions/arrayOrString"},
                "relation": {"$ref": "#/definitions/arrayOrString"},
                "rights": {"$ref": "#/definitions/arrayOrString"},
                "spatial": {
                    "oneOf": array_or_item({"$ref": "#/definitions/spatial"})
                },
                "specType": {"type": "string"},
                "stateLocatedIn": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"}
                        }
                    }
                },
                "subject": {
                    "$ref": "#/definitions/arrayMinOne",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"}
                        },
                    }
                },
                "temporal": {"$ref": "#/definitions/arrayOrString"},
                "title": {"$ref": "#/definitions/arrayOrString"},
                "type": {
                    "oneOf": array_or_item({"$ref": "#/definitions/type"})
                }
            }
        },
        "spatial": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "coordinates": {"type": "string"},
                "country": {"type": "string"},
                "county": {"type": "string"},
                "name": {"type": "string"},
                "region": {"type": "string"},
                "state": {"type": "string"}
            }
        },
        "type": {
            "type": "string",
            "enum": [
                "collection",
                "dataset",
                "image",
                "interactive resource",
                "moving image",
                "service",
                "sound",
                "text"
            ]
        }
    },
}