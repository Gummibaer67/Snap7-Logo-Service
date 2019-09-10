Snap7 Logo Service
==================

Is a tool to communicate with multiple Logo's via REST API.

And a backend for:
  - [Homebridge-Logo-REST](https://github.com/Sinclair81/Homebridge-Logo-REST)
  - [Homebridge-Logo-Blind-REST](https://github.com/Sinclair81/Homebridge-Logo-Blind-REST)

## Installation
- Install dependencies:
  - Python PIP using: `sudo apt-get install python-pip` or for Python3 using: `sudo apt-get install python3-pip`
  - Flask using: `sudo pip install flask`
  - Flask-CORS using: `sudo pip install -U flask-cors`
  - Waitress using: `sudo pip install waitress`
  - Install Snap7:
    - with this guide: [Raspberry Pi getting data from a S7-1200 PLC](http://simplyautomationized.blogspot.de/2014/12/raspberry-pi-getting-data-from-s7-1200.html)
    - [Snap7](http://snap7.sourceforge.net)
    - [Python-Snap7](https://github.com/gijzelaerr/python-snap7)
- Copy all files to: `/home/pi/python/snap7_logo_service`
- Go to snap7_logo_service: `cd /home/pi/python/snap7_logo_service`
- Change the settings for your logo's in:
  - in snap7_logo_service.py: Snap7 client, IP address, local TASP and remote TASP.
  - in logo_io_node.py: enter a few variable memory values.
- Test Snap7 Logo Service with: `python waitress_server.py`
- Copy snap7_logo_service.service to /etc/systemd/system: `sudo cp snap7_logo_service.service /etc/systemd/system/snap7_logo_service.service`
- Test snap7_logo_service.service:
  - start: `sudo systemctl start snap7_logo_service.service`
  - stop: `sudo systemctl stop snap7_logo_service.service`
- If everything is ok, start the service with the system start: `sudo systemctl enable snap7_logo_service.service`

- Optionally, a Chrome extension for [REST API Testing](https://chrome.google.com/webstore/detail/restlet-client-rest-api-t/aejoelaoggembcahagimdiliamlcdmfm)

## Snap7 Logo Service singel Node json request
*`[POST]`* `http://0.0.0.0:5000/logo/api/v1.0/node?json=<json_request>`

Name             | Values                   | Required | Notes
---------------- | ------------------------ | -------- | -------------------------------------
`command`        | "GET" or "SET"           | yes      | "GET" - reads the values from the logo, "SET" - write the values in the logo.
`id`             | (custom)                 | yes      | a number for a IO_Node
`pushbutton`[^1] | 1 or 0                   | no       | Must be set to `0` if your Network-Input act as a switch, default is: `1`, if `rwLenght` (from IO_Node) > `1`: `pushbutton` is ignort
`write`          | "on", "off" or "default" | no       | Must be set to "on" or "off", default is: "default" ;-)
`value`          | (custom)                 | no       | a number, default is: `1`
`return`         | "GET" or "value"         | no       | "GET" - reads the values from the logo, "value" - return `value`, default return value for "SET" is: `1`

[^1]: `pushbutton` means: 1. send `value` to "SET";  2. wait 0.2 sec;  3. send *not* `value` to "SET";

## Snap7 Logo Service Page json request
*`[POST]`* `http://10.0.0.4:5000/logo/api/v1.0/page?json=<json_request>`

Name             | Values   | Required | Notes
---------------- | -------- | -------- | -------------------------------------
`command`        | "GET"    | yes      | "GET" - reads the values from the logo
`id`             | (custom) | yes      | a number for a IO_Page

## For example request and response json objects:
*`[GET]`* `http://10.0.0.4:5000/logo/api/v1.0/help`

## Logo IO_Node configuration parameters

### Example IO_Node:

`IO_Node(1, 1, 1064, 0, 1, 0, 0, 0, 0, 0, 1, 0, "Q1 - V1.0 - Logo 8FS4 Test")`

### IO_Node parameters:

`IO_Node(id, logo, readAddress, readBit, writeAddress, writeBit, rwLenght, invertResult, text)`

Name              | Type   | Description
----------------- | ------ | -------------------------------------
`id`              | int    | ID
`logo`            | int    | Logo number (depend on how much Logos in snap7_logo_service.py) 1..244 / 255 for broadcast to all Logo's
`readAddress`     | int    | Read Address - VM[variable memory], VB- VW- or VD-Address
`readBit`         | int    | Read Bit (ignored at 8, 16 or 32 bits length)
`writeOnAddress`  | int    | Write On Address - VM[variable memory], VB- VW- or VD-Address
`writeOnBit`      | int    | Write On Bit (ignort at 8, 16 or 32 bits length)
`writeOffAddress` | int    | Write Off Address - VM[variable memory], VB- VW- or VD-Address
`writeOffBit`     | int    | Write Off Bit (ignort at 8, 16 or 32 bits length)
`writeAddress`    | int    | Write Default Address - VM[variable memory], VB- VW- or VD-Address
`writeBit`        | int    | Write Default Bit (ignort at 8, 16 or 32 bits length)
`rwLenght`        | int    | Read/Write Length (1, 8, 16 or 32) [1 -> 1 Bit, 8 -> VB-Address, 16 -> VW-Address, 32 -> VD-Address]
`invertResult`    | int    | Invert Read Result (ignort at 8, 16 or 32 bits length)
`text`            | string | Description Text

## Logo IO_Page configuration parameters

### Example IO_Page:

`IO_Page(1, [1, 4, 3, 2, 22, 56, 11], "Page 1")`

### IO_Page parameters:

`IO_Page(id, nodeArray, text)`

Name        | Type   | Description
----------- | ------ | -------------------------------------
`id`        | int    | ID
`nodeArray` | [int]  | ID's of several IO_Node's
`text`      | string | Description Text

## Logo VM-Addresses

### Logo 0BA7:
Type | Count | Start Address | Length
---- | ----- | ------------- | ------
Input | 24 | 923 | Bit
Analog Input | 8 | 926 | Word
Output | 16 | 942 | Bit
Analog Output | 2 | 944 | Word
Merker | 27 | 948 | Bit
Analog Merker | 16 | 952 | Word

### Logo 0BA8 / 8.SF4:
Type | Count | Start Address | Length
---- | ----- | ------------- | ------
Input | 24 | 1024 | Bit
Analog Input | 8 | 1032 | Word
Output | 20 | 1064 | Bit
Analog Output | 8 | 1072 | Word
Merker | 64 | 1104 | Bit
Analog Merker | 64 | 1118 | Word
