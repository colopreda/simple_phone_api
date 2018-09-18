from flask import request
from flask_restful import Resource
from flask_restful import abort

from models import Phone, PhoneSchema
from models import db

phones_schema = PhoneSchema(many=True)
phone_schema = PhoneSchema()


class LineResourceCreation(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = phone_schema.load(json_data)
        if errors:
            return errors, 422
        # Check if the keys entered are the ones expected            
        try:
            phone = Phone(phone_number=data['phone_number'], name=data['name'])
        except KeyError:
            return {'message': "The key/s you entered is/are invalid. Please check and try again"}, 400
        repeated_phone = db.session.query(Phone).filter(Phone.phone_number == data['phone_number']).first()
        # Check if the phone is already on the database
        if repeated_phone:
            return {'message': 'Phone already exists. Check the number and try again'}, 400
        db.session.add(phone)
        db.session.commit()

        result = phone_schema.dump(phone).data

        return result, 200


class LineResourceSearch(Resource):
    def get(self, phone_number):
        phone = db.session.query(Phone).filter(Phone.phone_number == phone_number).first()
        # Check if the phone isn't present in the database
        if not phone:
            abort(404, message="Phone {} doesn't exist".format(phone_number))
        result = phone_schema.dump(phone).data
        return result

    def delete(self, phone_number):
        phone = db.session.query(Phone).filter(Phone.phone_number == phone_number).first()
        # Check if the phone isn't present in the database
        if not phone:
            abort(404, message="Phone {} doesn't exist".format(phone_number))
        db.session.delete(phone)
        db.session.commit()
        return {}, 204


class LineResourcePhonecall(Resource):
    def put(self, phone_number):
        json_data = request.get_json(force=True)
        # Check if the user sent an empty body
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = phone_schema.load(json_data)
        if errors:
            return errors, 422
        # Check if the input number is valid
        if not isvalidnumber(phone_number):
            abort(400, message="You entered an invalid number. Please try again")
        phone = db.session.query(Phone).filter(Phone.phone_number == phone_number).first()
        # Check if the phone isn't present in the database
        if not phone:
            abort(404, message="Phone {} doesn't exist".format(phone_number))
        try:
            minutes_to_discount = data['minutes']
        except KeyError:
            return {'message': "The input data you entered is invalid. Please check it and try again"}, 400
        # Check if the remaining minutes will allow the user make the phonecall
        if minutes_to_discount <= 0:
            abort(400, message="The number of minutes of the call must be positive")
        minutes_remaining = phone.minutes - minutes_to_discount
        if minutes_remaining < 0:
            abort(400, message="You don't have enough minutes to make that phonecall")
        phone.minutes -= data['minutes']
        db.session.add(phone)
        db.session.commit()
        result = phone_schema.dump(phone).data
        return result


class LineResourceRecharge(Resource):
    def put(self, phone_number):
        json_data = request.get_json(force=True)
        # Check if the user sent an empty body
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = phone_schema.load(json_data)
        if errors:
            return errors, 422
        # Check if the input number is valid
        if not isvalidnumber(phone_number):
            abort(400, message="You entered an invalid number. Please try again")
        phone = db.session.query(Phone).filter(Phone.phone_number == phone_number).first()
        # Check if the phone isn't present in the database
        if not phone:
            abort(404, message="Phone {} doesn't exist".format(phone_number))
        try:
            new_phone_minutes = data['minutes']
        except KeyError:
            return {'message': "The input data you entered is invalid. Please check it and try again"}, 400
        # Check if the number of minutes if positive
        if not new_phone_minutes > 0:
            abort(400, message="Your new account minutes must be positive")
        phone.minutes = new_phone_minutes
        db.session.add(phone)
        db.session.commit()
        result = phone_schema.dump(phone).data
        return result


def isvalidnumber(phone_number):
    return phone_number.isdigit()
