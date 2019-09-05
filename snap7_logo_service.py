#!/usr/bin/env python

from flask import Flask
from flask import request
from flask_cors import CORS

import json
import time
import sys
import string
import ctypes

import logo_io_node

import snap7

########################################################
# client      = [snap7.logo.Logo(), snap7.logo.Logo()] #
# client_ip   = ["10.0.0.2",        "10.0.0.3"]        #
# local_tsap  = [0x4200,            0x4200]            #
# remote_tsap = [0x5200,            0x5200]            #
########################################################
import private_config
client      = private_config.client
client_ip   = private_config.client_ip
local_tsap  = private_config.local_tsap
remote_tsap = private_config.remote_tsap

nodes_and_pages_array = logo_io_node.IO_Array()

app = Flask(__name__)
cors = CORS(app, resources={r"/logo/api/*": {"origins": "*"}})


def setupApp():
    for x in range(len(client)):
        target = client[x]
        target.connect(client_ip[x], local_tsap[x], remote_tsap[x])


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1", "on")


def read(logo, address, bit, lenght, invert):
    print "GET - Logo:" + str(logo) + " Addr:" + str(address) + " Bit:" + str(bit) + " Lenght:" + str(lenght) + " Invert:" + str(invert)
    target = client[logo]
    if lenght == 1:
        addr = "V" + str(address) + "." + str(bit)
        try:
            rBit = target.read(addr)
        except:
            target.disconnect()
            target.connect(client_ip[logo], local_tsap[logo], remote_tsap[logo])
            rBit = read(logo, address, bit, lenght, invert)
        if invert == 1:
            if rBit == 1:
                rBit = 0
            else:
                rBit = 1
        return rBit
    if lenght == 8:
        addr = "V" + str(address)
        byte = 0
        try:
            byte = target.read(addr)
        except:
            target.disconnect()
            target.connect(client_ip[logo], local_tsap[logo], remote_tsap[logo])
            byte = read(logo, address, bit, lenght, invert)
        return byte
    if lenght == 16:
        addr = "VW" + str(address)
        word = 0
        try:
            word = target.read(addr)
        except:
            target.disconnect()
            target.connect(client_ip[logo], local_tsap[logo], remote_tsap[logo])
            word = read(logo, address, bit, lenght, invert)
        return word
    if lenght == 32:
        addr = "VD" + str(address)
        dword = 0
        try:
            dword = target.read(addr)
        except:
            target.disconnect()
            target.connect(client_ip[logo], local_tsap[logo], remote_tsap[logo])
            dword = read(logo, address, bit, lenght, invert)
        return dword


def write(logo, address, bit, lenght, value):
    print "SET - Logo:" + str(logo) + " Addr:" + str(address) + " Bit:" + str(bit) + " Lenght:" + str(lenght) + " Value:" + str(value)
    target = client[logo]
    if lenght == 1:
        addr = "V" + str(address) + "." + str(bit)
        try:
            target.write(addr, int(value))
        except:
            target.disconnect()
            target.connect(client_ip[logo], local_tsap[logo], remote_tsap[logo])
            write(logo, address, bit, lenght, value)
    if lenght == 8:
        addr = "V" + str(address)
        try:
            target.write(addr, int(value))
        except:
            target.disconnect()
            target.connect(client_ip[logo], local_tsap[logo], remote_tsap[logo])
            write(logo, address, bit, lenght, value)
    if lenght == 16:
        addr = "VW" + str(address)
        try:
            target.write(addr, int(value))
        except:
            target.disconnect()
            target.connect(client_ip[logo], local_tsap[logo], remote_tsap[logo])
            write(logo, address, bit, lenght, value)
    if lenght == 32:
        addr = "VD" + str(address)
        try:
            target.write(addr, int(value))
        except:
            target.disconnect()
            target.connect(client_ip[logo], local_tsap[logo], remote_tsap[logo])
            write(logo, address, bit, lenght, value)
    return 1


def getNode(node):
    reply = read(node.n_logo, node.n_readAddress, node.n_readBit, node.n_rwLenght, node.n_invertResult)
    return reply


def setNode(node, pushButton, set, value):
    wAddr = node.n_writeAddress
    wBit  = node.n_writeBit
    if set == "on":
        wAddr = node.n_writeOnAddress
        wBit  = node.n_writeOnBit
    if set == "off":
        wAddr = node.n_writeOffAddress
        wBit  = node.n_writeOffBit
    if node.n_logo != 255:
        write(node.n_logo, wAddr, wBit, node.n_rwLenght, value)
        if pushButton == 1 and node.n_rwLenght == 1:
            time.sleep(.200)
            write(node.n_logo, wAddr, wBit, node.n_rwLenght, int(not value))
    else:
        num = 0
        for x_logo in client:
            write(num, wAddr, wBit, node.n_rwLenght, value)
            if pushButton == 1 and node.n_rwLenght == 1:
                time.sleep(.200)
                write(num, wAddr, wBit, node.n_rwLenght, int(not value))
            time.sleep(.200)
            num = num + 1
    return 1


def getPage(page):
    reply = ""
    for node_id in page.p_nodeArray:
        node = nodes_and_pages_array.returnNodeWitheID(node_id)
        reply = reply + str(read(node.n_logo, node.n_readAddress, node.n_readBit, node.n_rwLenght, node.n_invertResult)) + "|"
        time.sleep(.200)
    return reply


@app.errorhandler(400)
def bat_request(error):
    return json.dumps({'error': 'Bad Request'}), 400, {'ContentType':'application/json'}


@app.errorhandler(404)
def not_found(error):
    return json.dumps({'error': 'Not Found'}), 404, {'ContentType':'application/json'}


@app.route("/")
def root():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


# http://10.0.0.4:5000/logo/api/v1.0/help
@app.route("/logo/api/v1.0/help", methods=['GET'])
def apiCall_v1_0_help():
    jsonHelp = json.loads('''{"requests":{"node":{"post_url":"http://0.0.0.0:5000/logo/api/v1.0/node?json=<json_request>","examples":[{"command":"SET","id":1,"pushbutton":0,"write":"on","value":1,"return":"GET"},{"command":"SET","id":2,"value":30},{"command":"GET","id":3}]},"page":{"post_url":"http://0.0.0.0:5000/logo/api/v1.0/page?json=<json_request>","example":{"command":"GET","id":201}}},"response":{"node":{"value": 1,"success":true},"page":{"value": "0|0|0|0|0|0|0|1|0|","success":true},"error_1":{"error":"Bad Request"},"error_2":{"error":"Not Found"}}}''')
    return jsonHelp, 200, {'ContentType':'application/json'}


# http://10.0.0.4:5000/logo/api/v1.0/node?json={"command":"SET","id":40,"pushbutton":1,"write":"default","value":0,"return":"GET"}
@app.route("/logo/api/v1.0/node", methods=['POST'])
def apiCall_v1_0_node():
    try:
        node_command        = ""
        node_id             = 0
        node_pushButton     = 1
        node_write          = "default"
        node_value          = 1
        node_return_command = ""
        node_return_value   = 0
        if not request.args.get("json"):
            return json.dumps({'error': 'Bad Request'}), 400, {'ContentType':'application/json'}
        data = request.args.get('json')
        data_decoded = json.loads(data)
        if 'command' in data_decoded:
            node_command = str(data_decoded['command']).upper()
        else:
            return json.dumps({'error': 'Bad Request'}), 400, {'ContentType':'application/json'}
        if 'id' in data_decoded:
            node_id = int(data_decoded['id'])
        else:
            return json.dumps({'error': 'Bad Request'}), 400, {'ContentType':'application/json'}
        if 'pushbutton' in data_decoded:
            node_pushButton = int(data_decoded['pushbutton'])
        if 'write' in data_decoded:
            node_set = data_decoded['write']
        if 'value' in data_decoded:
            node_value = int(data_decoded['value'])
        if 'return' in data_decoded:
            node_return_command = str(data_decoded['return']).upper()
        node = nodes_and_pages_array.returnNodeWitheID(node_id)
        if node_command == "GET":
            node_return_value = getNode(node)
        if node_command == "SET":
            node_return_value = setNode(node, node_pushButton, node_set, node_value)
            if node_return_command == "GET":
                time.sleep(.200)
                node_return_value = getNode(node)
            if node_return_command == "VALUE":
                node_return_value = node_value
        return json.dumps({'success':True,'value':node_return_value}), 200, {'ContentType':'application/json'}
    except:
        return json.dumps({'success':False}), 200, {'ContentType':'application/json'}

# http://10.0.0.4:5000/logo/api/v1.0/page?json={"command":"GET","id":201}
@app.route("/logo/api/v1.0/page", methods=['POST'])
def apiCall_v1_0_page():
    try:
        page_command      = ""
        page_id           = 0
        page_return_value = ""
        if not request.args.get("json"):
            return json.dumps({'error': 'Bad Request'}), 400, {'ContentType':'application/json'}
        data = request.args.get('json')
        data_decoded        = json.loads(data)
        if 'command' in data_decoded:
            page_command = str(data_decoded['command'])
        else:
            return json.dumps({'error': 'Bad Request'}), 400, {'ContentType':'application/json'}
        if 'id' in data_decoded:
            page_id = int(data_decoded['id'])
        else:
            return json.dumps({'error': 'Bad Request'}), 400, {'ContentType':'application/json'}
        page = nodes_and_pages_array.returnPageWitheID(page_id)
        if page_command == "GET":
            page_return_value = getPage(page)
        if page_command == "SET":
            return json.dumps({'error': 'Not Implemented'}), 501, {'ContentType':'application/json'}
        return json.dumps({'success':True,'value':page_return_value}), 200, {'ContentType':'application/json'}
    except:
        return json.dumps({'success':False}), 200, {'ContentType':'application/json'}


setupApp()


if __name__ == "__main__":
    print "main"
