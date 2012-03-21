from flask import make_response
from flask import render_template
import json
import util
import crud_helpers
from crud_helpers import HelperException

def create(request):
	success = True
	result = {}
	error = ''
	status_code = 200

	if request is None:
		success = False
		error = "Bad request.  Somehow the request wasn't found."
		status_code = 400

	# handle multi and inline parameters in request
	multi = util.str2bool(request.args.get('multi'))
	inline = util.str2bool(request.args.get('inline'))

	# handle multiple documents
	if multi is True:
		# TODO

		if type(request.json) is not list:
			# check to see if it is a single document (i.e., dict)
			#if multi is True:
			#	if len(request.json) > 1:
			#		for doc in request.json:
			#			print doc['title']
			pass

	if 'application/json' in request.headers['content-type']:
		# create the package object
		try:
			result['id'] = crud_helpers.create_package(request.json)
		except HelperException as e:
			success = False
			error = e.error
			status_code = e.status_code
	else:
		success = False
		error = "The content-type was not of the expected type.  The content-type found was " + request.headers["content-type"] + ", whereas the content-type expected was application/json."
		status_code = 400

	# handle inline parameter in request
	if inline is True:
		# parse out resource
		pass
		# TODO

	if success is True:
		response = createJsonResponse(result, status_code)
	else:
		result['error'] = error
		response = createJsonResponse(result, status_code)
	
	return response

def retrieve(request, id):
	# use HTTP status codes
	response = ''
	result = {}
	success = True
	error = ''
	status_code = 200

	if request is None:
		success = False
		error = "Bad request.  Somehow the request wasn't found."
		status_code = 400

	if id is None:
		success = False
		error = "Bad request.  No id was found."
		status_code = 400
	
	try:
		result = crud_helpers.retrieve_package(id)
	except HelperException as e:
		success = False
		error = e.error
		status_code = e.status_code

	if success is True:
		response = createJsonResponse(result, status_code)
	else:
		result['error'] = error
		response = createJsonResponse(result, status_code)

	return response

def update(request, id):
	response = ''
	result = {}
	success = True
	error = ''
	status_code = 200

	if request is None:
		success = False
		error = "Bad request.  Somehow the request wasn't found."
		status_code = 400

	if 'application/json' in request.headers['content-type']:
		# create the package object
		try:
			crud_helpers.update_package(id, request.json)
		except HelperException as e:
			success = False
			error = e.error
			status_code = e.status_code
	else:
		success = False
		error = "The content-type was not of the expected type.  The content-type found was " + request.headers["content-type"] + ", whereas the content-type expected was application/json."
		status_code = 400		

	if success is True:
		response = make_response(None, status_code)
	else:
		result['error'] = error
		response = createJsonResponse(result, status_code)

	return response

def delete(request, id):
	response = ''
	result = {}
	success = True
	error = ''
	status_code = 200

	if request is None:
		success = False
		error = "Bad request.  Somehow the request wasn't found."
		status_code = 400

	try:
		crud_helpers.delete_package(id)
	except HelperException as e:
		success = False
		error = e.error
		status_code = e.status_code

	if success is True:
		response = make_response(None, status_code)
	else:
		result['error'] = error
		response = createJsonResponse(result, status_code)

	return response

def createJsonResponse(doc, status_code):
	response = make_response(json.dumps(doc), status_code)
	response.headers['content-type'] = "application/json"
	return response