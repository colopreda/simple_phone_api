# -*- coding: utf-8 -*-
import unittest

from flask import json

from models import db
from models import Phone


class TestCase(unittest.TestCase):
    def setUp(self):
        from app import app
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        app.config["TESTING"] = True
        self.app = app.test_client()

        with app.app_context():
            db.init_app(app)
            db.drop_all()
            db.create_all()

            phone = Phone(11111111, "test")
            db.session.add(phone)
            db.session.commit()

    def tearDown(self):
        pass

    def test_create_phone_ok(self):
        payload = {"phone_number": 1123, "name": "test"}
        r = self.app.post('/lines/create', data=json.dumps(payload), content_type='application/json')
        r = json.loads(r.data)
        assert r['minutes'] == 0
        assert r['phone_number'] == 1123
        assert r['name'] == "test"

    def test_create_phone_duplicate(self):
        payload = {"phone_number": 1123, "name": "test"}
        r = self.app.post('/lines/create', data=json.dumps(payload), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 200
        assert s['minutes'] == 0
        assert s['phone_number'] == 1123
        assert s['name'] == "test"
        r = self.app.post('/lines/create', data=json.dumps(payload), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "Phone already exists. Check the number and try again"

    def test_create_phone_bad_body(self):
        payload = {"phone_nuber": 1123, "name": "test"}
        r = self.app.post('/lines/create', data=json.dumps(payload), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "The key/s you entered is/are invalid. Please check and try again"

    def test_create_phone_no_input_data(self):
        r = self.app.post('/lines/create', data=json.dumps({}), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "No input data provided"

    def test_create_phone_wrong_key_type(self):
        payload = {"phone_number": "123a5", "name": "test"}
        r = self.app.post('/lines/create', data=json.dumps(payload), content_type='application/json')
        assert r.status_code == 422

    def test_find_individual_phone(self):
        r = self.app.get('/lines/11111111')
        r = json.loads(r.data)
        assert r['minutes'] == 0
        assert r['phone_number'] == 11111111
        assert r['name'] == "test"

    def test_individual_phone_not_present(self):
        r = self.app.get('/lines/11111112')
        s = json.loads(r.data)
        assert r.status_code == 404
        assert s['message'] == "Phone 11111112 doesn't exist"

    def test_delete_individual_phone(self):
        r = self.app.delete('/lines/11111111')
        assert r.status_code == 204

    def test_individual_phone_not_found(self):
        r = self.app.delete('/lines/11111112')
        s = json.loads(r.data)
        assert r.status_code == 404
        assert s['message'] == "Phone 11111112 doesn't exist"

    def test_add_credit(self):
        payload = {"minutes": 5}
        self.app.put('lines/11111111/charge', data=json.dumps(payload), content_type='application/json')
        s = self.app.get('lines/11111111')
        s = json.loads(s.data)
        assert s['minutes'] == 5

    def test_add_credit_no_data(self):
        r = self.app.put('lines/11111111/charge', data=json.dumps({}), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "No input data provided"

    def test_add_credit_wrong_type_data(self):
        payload = {"minutes": "aaa"}
        r = self.app.put('lines/11111111/charge', data=json.dumps(payload), content_type='application/json')
        assert r.status_code == 422

    def test_add_credit_wrong_key_type(self):
        payload = {"minutos": 5}
        r = self.app.put('lines/11111111/charge', data=json.dumps(payload), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "The input data you entered is invalid. Please check it and try again"

    def test_add_credit_wrong_number(self):
        payload = {"minutes": 5}
        r = self.app.put('lines/12345/charge', data=json.dumps(payload), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 404
        assert s['message'] == "Phone 12345 doesn't exist"

    def test_add_credit_negative_number(self):
        payload = {"minutes": -1}
        r = self.app.put('lines/11111111/charge', data=json.dumps(payload), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "Your new account minutes must be positive"

    def test_recharge_invalid_number(self):
        payload_charge = {"minutes": 5}
        r = self.app.put('lines/1111111a/charge', data=json.dumps(payload_charge), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "You entered an invalid number. Please try again"

    def test_make_phonecall(self):
        payload_charge = {"minutes": 15}
        self.app.put('lines/11111111/charge', data=json.dumps(payload_charge), content_type='application/json')
        payload_phonecall = {"minutes": 8}
        r = self.app.put('lines/11111111/phonecall', data=json.dumps(payload_phonecall), content_type='application/json')
        assert r.status_code == 200

    def test_make_phonecall_no_data(self):
        payload_charge = {"minutes": 15}
        self.app.put('lines/11111111/charge', data=json.dumps(payload_charge), content_type='application/json')
        r = self.app.put('lines/11111111/phonecall', data=json.dumps({}), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "No input data provided"

    def test_make_phonecall_wrong_number(self):
        payload_charge = {"minutes": 15}
        self.app.put('lines/11111111/charge', data=json.dumps(payload_charge), content_type='application/json')
        payload_phonecall = {"minutes": 8}
        r = self.app.put('lines/12345/phonecall', data=json.dumps(payload_phonecall), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 404
        assert s['message'] == "Phone 12345 doesn't exist"

    def test_make_phonecall_wrong_key_type(self):
        payload_charge = {"minutes": 15}
        self.app.put('lines/11111111/charge', data=json.dumps(payload_charge), content_type='application/json')
        payload_phonecall = {"minutos": 8}
        r = self.app.put('lines/11111111/phonecall', data=json.dumps(payload_phonecall), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "The input data you entered is invalid. Please check it and try again"

    def test_make_phonecall_wrong_type_data(self):
        payload_charge = {"minutes": 15}
        self.app.put('lines/11111111/charge', data=json.dumps(payload_charge), content_type='application/json')
        payload_phonecall = {"minutes": "asdasd"}
        r = self.app.put('lines/12345/phonecall', data=json.dumps(payload_phonecall), content_type='application/json')
        assert r.status_code == 422

    def test_make_phonecall_no_credit(self):
        payload_charge = {"minutes": 5}
        self.app.put('lines/11111111/charge', data=json.dumps(payload_charge), content_type='application/json')
        payload_phonecall = {"minutes": 8}
        r = self.app.put('lines/11111111/phonecall', data=json.dumps(payload_phonecall), content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "You don't have enough minutes to make that phonecall"

    def test_make_phonecall_negative_minutes(self):
        payload_charge = {"minutes": 5}
        self.app.put('lines/11111111/charge', data=json.dumps(payload_charge), content_type='application/json')
        payload_phonecall = {"minutes": -1}
        r = self.app.put('lines/11111111/phonecall', data=json.dumps(payload_phonecall),
                         content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "The number of minutes of the call must be positive"

    def test_make_phonecall_invalid_number(self):
        payload_charge = {"minutes": 5}
        self.app.put('lines/11111111/charge', data=json.dumps(payload_charge), content_type='application/json')
        payload_phonecall = {"minutes": 8}
        r = self.app.put('lines/asdasd/phonecall', data=json.dumps(payload_phonecall),
                         content_type='application/json')
        s = json.loads(r.data)
        assert r.status_code == 400
        assert s['message'] == "You entered an invalid number. Please try again"
