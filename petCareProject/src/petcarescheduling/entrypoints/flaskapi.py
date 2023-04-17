from flask import Flask, jsonify, request
from petcarescheduling import bootstrap
from petcarescheduling.domain import commands

app = Flask(__name__)
bus = bootstrap.bootstrap()


@app.route("/add_service", methods=["POST"])
def add_service():

    data = request.get_json()
    print(data)
    service_id = data["service_id"]
    service_name = data["service_name"]
    price = data["price"]
    pet_species = data["pet_species"]
    print(service_name,price,pet_species)
    
    cmd = commands.CreateService(
        service_id=service_id,service_name=service_name, price=price, pet_species=pet_species
    )
    bus.handle(cmd)
    return "OK", 201
