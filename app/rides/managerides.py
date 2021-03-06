from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from app.model.user import User, generate_token, decode_token
import re
import json
from app.user.authentication import my_users_list
from app.model.addride_model import AddRide


rides_list = []


class GetRides(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('details', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('token', location='headers')

        args = parser.parse_args()
        # check the token value if its available
        if not args['token']:
            return make_response(jsonify({"message":
                                          "Token is missing"}),
                                 401)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message":
                                          decoded["message"]}),
                                 401)

        for user in my_users_list:
            if user['id'] == decoded['id']:
                offer_name = args['name']
                offer_details = args['details']
                price = args['price']
                global id
                if not rides_list:
                    id = len(rides_list)+1
                else:
                    id = id+1
                new_request = AddRide(id, offer_name, offer_details, price)
                for ridereq in rides_list:
                    if on == ridereq['name']:
                        return make_response(jsonify({"message":
                                                      'This ride offer  already exists.'}),
                                             400)

                ridereq = json.loads(new_request.json())
                rides_list.append(ridereq)

                return make_response(jsonify({
                    'message': 'Ride offer created successfully.',
                    'status': 'success'},
                ), 201)

        return make_response(jsonify({"message":
                                      "Please first create an account."}),
                             401)

    def get(self):
        """
        Returns all ride offers  made for authenticated drivers and passengers
        token is required to get them.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()
        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}),
                                 401)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}),
                                 401)

        my_rides = []
        for ride in rides_list:
            rides_data = {
                "id": ride["id"],
                "name": ride["name"],
                "details": ride['details'],
                "price": ride['price']
            }
            my_rides.append(rides_data)
        if my_rides:
            return make_response(jsonify({"ride_offers": my_rides,
                                          "status": "success"}),
                                 200)
        else:
            return make_response(jsonify({"message": "No ride offers found."}),
                                 404)

        return make_response(jsonify({"message": "Please first create an account."}),
                             404)


class GetSingleRide(Resource):
    def get(self, ride_id):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')
        args = parser.parse_args()

        if not args['token']:
            return make_response(jsonify({"message": "Token is missing"}),
                                 401)
        decoded = decode_token(args['token'])
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}),
                                 401)
        for ride in rides_list:
            if int(ride['id']) == int(ride_id):

                rides_data = {
                    "id": ride["id"],
                    "name": ride["name"],
                    "details": ride['details'],
                    "price": ride['price']
                }

                return make_response(jsonify({"ride_offer": rides_data,
                                              "status": "success"}),
                                     200)
        return make_response(jsonify({"message":
                                      "sorry please , ride offer not found"}),
                             404)
