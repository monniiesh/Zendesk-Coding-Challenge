# PyTest testing framework

"""
Author : Monniiesh Velmurugan
Project : Zendesk Ticket Viewer
"""

from zendesk import *
import pytest
import requests

url= "Enter API Ex : https://example.zendesk.com/api/v2/tickets.json?page[size]=25"
user = "Enter User"
passwd = "Enter Passwd"

def test_get_json():
	"""
	
	unit test for zendesk.get_json() function

	"""
	global url, user, passwd

	data = get_json(url, user, passwd)

	assert data != []

def test_get_json_error_handling():
	"""
	
	unit test for error handling of zendesk.get_json() function

	"""
	url = "https://zccmonniieshelp.zendesk.com/api/v2/tickets.json?page[size]=25"
	user = "monniiesh22@gmail.com"
	passwd = "mondar22"	

	try:
		data = get_json(url, user, passwd)
		assert False
	except Exception:
		assert True

def test_get_tickets():
	"""
	
	unit test for zendesk.get_tickets) function

	"""
	global url, user, passwd
	tickets = get_tickets(requests.get(url, auth=(user, passwd), timeout = 5).json()["tickets"])

	assert 1267063452030 in tickets[0]
	assert "laboris sint Lorem ex Lorem" in tickets[20]
	assert "Date : 2021-11-19 - Time : 22:46:22" in tickets[10]

def test_display_tickets():
	"""
	
	unit test for zendesk.display_tickets() function

	"""
	global url, user, passwd
	tickets = get_tickets(requests.get(url, auth=(user, passwd), timeout = 5).json()["tickets"])

	pretty_table_obj = display_tickets(tickets)

	assert str(type(pretty_table_obj)) == "<class 'prettytable.prettytable.PrettyTable'>"

def test_ticket_details_and_ticket_format():
	"""
	
	unit test for zendesk.test_ticket_details_and_ticket_format() function

	"""
	global url, user, passwd
	tickets = get_tickets(requests.get(url, auth=(user, passwd), timeout = 5).json()["tickets"])

	for k in ["Ticket ID", "Status", "Priority", "Requester ID", "Subject", "Description", "Email CC IDs", "Collaborators IDs", "Created At", "Updated At", "Due At"]:
		assert k in ticket_format(tickets[0])

def test_timer_format():
	"""
	
	unit test for zendesk.time_format() function

	"""
	expected_output = "Date : 2021-11-19 - Time : 21:52:34"

	assert time_format("2021-11-19T21:52:34Z") == expected_output