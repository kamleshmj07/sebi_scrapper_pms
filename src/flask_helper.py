from flask import json, request, g, current_app
from flask.wrappers import Response
import time
import logging
from werkzeug.exceptions import HTTPException, InternalServerError
# from .authorize import authorize
import werkzeug

def fn_before_request():
    # setup timer
    g.req_time = time.time()

    # authenticate request
    # authorize(current_app.config["JWT_PUBLIC_KEY"])
    # authorize(current_app.config)
    
    # logging.warning("Before request")

def fn_after_request(response: Response):
    # TODO: Currently we are using flask-cors, but it can be removed and CORS policy should be set here.

    # logging.warning("After request")

    return response

def fn_teardown_request(err: None):
    # remove existing DB connection 
    current_app.db.remove()

    # see if anything else to be done by the app

    # log request with response or uncaught exception
    if err:
        logging.error(err)
    else:
        time_taken = time.time() - g.req_time
        logging.info(F"{request.endpoint}: {request.method} took {time_taken} seconds")

    # logging.warning("Teardown request")

def exception_jsonifier(err):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    # TODO: not the best version. looks like this will make code slow. optimize it.
    if isinstance(err, werkzeug.exceptions.HTTPException):
        response = err.get_response()
        response.data = json.dumps({
            "code": err.code,
            "name": err.name,
            "description": err.description,
        })
        response.content_type = "application/json"
        return response
    else:
        s = str(err)
        raise InternalServerError(description=s)

    # try:
    #     response = err.get_response()
    # except AttributeError as e:
    #     # any exception which is created by flask (or werkzeug) will have response. others will be logged here.
    #     s = str(err)
    #     raise InternalServerError(description=s)

    # # replace the body with JSON
    # response.data = json.dumps({
    #     "code": err.code,
    #     "name": err.name,
    #     "description": err.description,
    # })
    # response.content_type = "application/json"
    # return response
