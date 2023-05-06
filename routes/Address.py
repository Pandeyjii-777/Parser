from flask import Blueprint, render_template, abort, request
from service.AddressService import *
from service.AddressParse import *


class Address:
    address_app = Blueprint('address_app', __name__, template_folder='templates')
    def __init__(self):
        pass

    @address_app.route('/address', methods=['GET'])
    def AddressByCompanyIdAndHubId():
        company_id = request.args.get('company_id')
        hub_id = request.args.get('hub_id')
        user_id = request.args.get('user_id')
        return getAddressByCompanyIdAndHubId(company_id, hub_id, user_id)
        
    @address_app.route('/saveAddress', methods=['POST'])
    def saveAddress():
        company_id = request.args.get('company_id')
        user_id = request.args.get('user_id')
        data = request.json
        return updateAndSave(data["addresses"], company_id, user_id)

    @address_app.route('/parse', methods=['POST'])
    def parseAddressNormal():
        data = request.json
        return normalParse(data)

    @address_app.route('/geocode', methods=['POST'])
    def allLatAndLng():
        data = request.json
        return getLatAndLng(data)

