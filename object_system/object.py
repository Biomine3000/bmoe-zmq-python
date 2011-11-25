#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import hashlib
import json
import unittest

OBJECT_SYSTEM_NS_UUID = uuid.UUID('6b004e0a-f846-409e-9c3e-c770194b2446')
NULL = '\0'

def get_uuid(string):
    return uuid.uuid5(OBJECT_SYSTEM_NS_UUID, string)

class EmptyMessageError(Exception):
    pass

class JSONParsingError(Exception):
    pass

class MissingMimeTypeError(Exception):
    pass

class MissingMimeTypeError(Exception):
    pass

# http://en.wikipedia.org/wiki/Internet_media_type
# http://en.wikipedia.org/wiki/MIME
class InvalidMimeTypeError(Exception):
    pass


class BusinessObject(object):
    def __init__(self, bytes):
        if len(bytes) == 0:
            raise EmptyMessageError("Parsed message was empty: %s" % repr(bytes))

        parts = bytes.split(NULL)
        header = parts[0]

        if len(parts) > 1:
            self.payload = NULL.join(parts[1:])
        else:
            self.payload = None

        try:
            self.metadata = json.loads(header)
        except ValueError, ve:
            if str(ve) == 'No JSON object could be decoded':
                raise JSONParsingError(str(ve))
            else:
                raise ve

        if not self.metadata.has_key('mimetype'):
            raise MissingMimeTypeError("Missing mimetype from metadata (keys: %s)" %
                                       ', '.join([repr(k) for k in self.metadata.keys()]))

        if len(self.metadata['mimetype'].split('/')) != 2:
            raise InvalidMimeTypeError("Invalid mime type: %s" % self.metadata['mimetype'])

        self.metadata['id'] = str(get_uuid(bytes))

    def bytes(self):
        if self.payload:
            return json.dumps(self.metadata) + NULL + self.payload
        else:
            return json.dumps(self.metadata) + NULL

class PlaintextObject(BusinessObject):
    def __init__(self, text):
        self.metadata = {}
        self.metadata['mimetype'] = 'text/plain'
        self.payload = text


class TestBusinessObjectInit(unittest.TestCase):
    # self.assertEqual(, )
    # self.assertTrue()
    # self.assertRaises(Exception, function, params)

    def test_valid_message(self):
        msg = json.dumps({'mimetype': 'text/plain'}) + NULL + 'hello'
        bo = BusinessObject(msg)

        self.assertEquals(bo.metadata['mimetype'], 'text/plain')
        self.assertEquals(bo.payload, 'hello')

    def test_invalid_message(self):
        msg = ''
        self.assertRaises(EmptyMessageError, BusinessObject, msg)

    def test_invalid_json(self):
        msg = 'aoeu' + NULL
        self.assertRaises(JSONParsingError, BusinessObject, msg)

    def test_missing_mimetype(self):
        msg = json.dumps({}) + NULL + 'hello'
        self.assertRaises(MissingMimeTypeError, BusinessObject, msg)

    def test_missing_mimetype(self):
        msg = json.dumps({'mimetype': 'text'}) + NULL + 'hello'
        self.assertRaises(InvalidMimeTypeError, BusinessObject, msg)


if __name__ == '__main__':
    unittest.main()
