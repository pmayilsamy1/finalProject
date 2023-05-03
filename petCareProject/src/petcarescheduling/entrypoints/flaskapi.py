from flask import Flask, jsonify, request
from petcarescheduling import bootstrap, views
from petcarescheduling.domain import commands
from petcarescheduling.services.handlers import InvalidService

app = Flask(__name__)
bus = bootstrap.bootstrap()


@app.route("/add_service", methods=["POST"])
def add_service():

    data = request.get_json()
    print(data)
    #service_id = data["service_id"]
    service_name = data["service_name"]
    price = data["price"]
    pet_species = data["pet_species"]
    qty = data["qty"]
    print(service_name,price,pet_species)
    
    cmd = commands.CreateService(
        service_name=service_name, price=price, pet_species=pet_species, qty=qty
    )
    bus.handle(cmd)
    return "OK", 201

@app.route("/allocate_service", methods=["POST"])
def allocate_service():
    try:
        cmd = commands.AllocateService(
            request.json["customer_id"], request.json["service_name"], request.json["pet_species"]
        )
        bus.handle(cmd)
    except InvalidService as e:
        return {"message": str(e)}, 400

    return "OK", 202

@app.route("/allocations/<customer_id>", methods=["GET"])
def allocations_view_endpoint(customer_id):
    print(customer_id)
    result = views.allocations(int(customer_id), bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

