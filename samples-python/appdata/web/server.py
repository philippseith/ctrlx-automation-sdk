# MIT License
#
# Copyright (c) 2021-2022 Bosch Rexroth AG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from socketserver import UnixStreamServer
from urllib.parse import unquote
from json import loads

from  appdata.app_data_control import AppDataControl

import token



# Simple Webserver to get rest requests
class Server(BaseHTTPRequestHandler):

    rest_url_load = '/sdk-py-appdata/api/v1/load'
    rest_url_save = '/sdk-py-appdata/api/v1/save'

    app_data_control = AppDataControl()

    config_payload = {
        "configurationPath": "",
        "id": "",
        "phase": ""
        }

    def do_POST(self):
        # Check if url valid
        request_url = self.path
        print("INFO REST Command:", request_url)
        if request_url != Server.rest_url_load and request_url != Server.rest_url_save:
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        # Check if command valid
        if self.command != 'POST':
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)
            return
        # Check Request Token
        token_validation = webtoken.TokenValidation()
        result, token, token_decoded = token_validation.get_token(self.headers)
        if result is False or token_validation.is_authorized("rexroth-device.all.rwx") is False:
            self.send_error(HTTPStatus.UNAUTHORIZED)
            print("ERROR Not authorized (Bearer invalid)")
            return
        print("INFO Check scope passed")

        # Get payload from request
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        payload_string = unquote(self.rfile.read(content_length).decode("utf-8"))
        # parse = parse_qs(post_data)
        payload = dict(loads(payload_string))
        # Check if payload contains config payload
        if payload.keys() != Server.config_payload.keys():
            self.send_error(HTTPStatus.BAD_REQUEST)
            print("ERROR wrong request payload")
            return

        # Command evaluation
        # Load Command
        if request_url == Server.rest_url_load:
            # phases
            # phases we don't care about in this sample can be implemented on demand.
            # query: Check if loading is possible in the current system statecase "query" :
			# Hint: The phase 'query' is called 2 times: the first call asks for a setup mode change acknowledge and the second is called during normal load sequence
            if payload["phase"] == "query":
                print("INFO Phase: query")
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                return

            # prepare: Perform any required preparatory steps
            elif payload["phase"] == "prepare":
                print("INFO Phase: prepare")
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                return

            # validate: Perform post-processing steps, connect resources and resolve dependencies
            elif payload["phase"] == "validate":
                print("INFO Phase: validate")
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                return

            # activate (if phases 1-4 have been finished without problems): Establish desired run state of the device
            elif payload["phase"] == "activate":
                print("INFO Phase: activate")
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                return

            # abort (otherwise): Do NOT change run state of the device, clean up if required
            elif payload["phase"] == "abort":
                print("INFO Phase: abort")
                # We return 204 as an default to satisfy the workflow
                # response.WriteHeader(http.StatusNoContent)
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                return

            # load: Provide resources according to the data from the active configuration
            elif payload["phase"] == "load":
                print("INFO Phase: load")
                # This is were we can load our application data from current configuration
                if Server.app_data_control.load() is False:
                    self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)
                    return
                else:
                    self.send_response(HTTPStatus.ACCEPTED)
                    self.end_headers()
                    return
            else:
                # We return 204 here to add upwards-compatibility for new phases
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
                return
        # Save command
        if request_url == Server.rest_url_save:
            # phases
            # Save: Serialize current resources into active configuration
            if payload["phase"] == "save":
                print("INFO phase: save")
                # This is were we can save our application data into current configuration to be persistent
                # Set default data on save command every time because this sample has no additional application data
                Server.app_data_control.set_default()
                if Server.app_data_control.save() is False:
                    self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)
                    return
                else:
                    self.send_response(HTTPStatus.ACCEPTED)
                    self.end_headers()
                    return


# Because http.server lib is designed for tcp, we need to write our own class to use unix sockets
class UnixSocketHttpServer(UnixStreamServer):

    allow_reuse_address = True

    def get_request(self):
        # dummy client address to avoid errors
        request, client_address = super().get_request()
        return (request, ["local", 0])
