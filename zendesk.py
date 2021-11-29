"""
Author : Monniiesh Velmurugan
Project : Zendesk Ticket Viewer
"""

import json
import requests
from prettytable import PrettyTable

url_master = "Enter API Ex : https://example.zendesk.com/api/v2/tickets.json?page[size]=25"
user = "Enter User"
passwd = "Enter Passwd"

has_more = False
next_page = None
prev_page = None
url = None

class JsonDataNotFoundError(Exception):
	"""

	Custom class to throw error when the JSON file returned by request is empty

	"""
	def __init__(self, messsage = "The requested json file in empty"):
		self.messsage = messsage
		super().__init__(self.messsage)

def get_json(url, user, passwd):
	"""

	This function requests the tickets data in json format for teh given API, user & password.
	This function also throws ConnectionError if connection cannot be established for thr given 
	credentials and print & quit if its any error from the API.

	Parameters : 
		url (str) : the url of the API
		user (str) : the user id of the API
		passwd (str) : the password needed for the API

	Return : 
		data (list) : the json data requested from the given API 

	"""
	global has_more, next_page, prev_page
	try:
		r = requests.get(url, auth=(user, passwd), timeout = 5).json()
		data = r["tickets"]
		has_more = bool(r["meta"]["has_more"])
		next_page = r["links"]["next"]
		if next_page == 'None':
			next_page = None
		prev_page = r["links"]["prev"]
		if prev_page == 'None':
			prev_page = None

		if "error" in r.keys():
			print(data)
			quit()

		return data

	except requests.ConnectionError:		
		print("Request cannot be made to the given API")
		quit()

def get_tickets(data):
	"""

	This function exrtracts a list of tickets data from the given json file

	Parameters : 
		data (dict) : the json file whose data needs to be extracted
	
	Return : 

		tickets (list) : a list of lists containing datas of each tickets

	"""

	if data != None or len(data) != 0:
	    tickets = []

	    for k in data:

	        ticket_id = k["id"]
	        subject = k["subject"]
	        requester_id = k["requester_id"]
	        created_date = time_format(k["created_at"])
	        last_updated = time_format(k["updated_at"])
	        status = k["status"]
	        priority = k["priority"]
	        description = k["description"]
	        due_at = k["due_at"]

	        if k["email_cc_ids"] == []:
	            email_cc_ids = "None"
	        else:
	            email_cc_ids = k["email_cc_ids"]
	        if k["collaborator_ids"] == []:
	            collaborator_ids = "None"
	        else:
	            collaborator_ids = k["collaborator_ids"]

	        ticket = [ticket_id, subject, requester_id, created_date, last_updated, 
	                  status, priority, description, due_at, email_cc_ids, collaborator_ids]
	        
	        tickets.append(ticket)

	    return tickets
	
	else:
		raise JsonDataNotFoundError()


def display_tickets(tickets):
	"""

	This function returns a table representing the data of all the tickets

	Parameters : 
		tickets (list) : a list of lists containing datas of each ticket
	
	Return : 
		table (PrettyTable): a table containing data of all the tickets

	"""

	if tickets == []:
		return "\nNo Tickets Found"

	try:
	    table = PrettyTable(["Ticket ID", "Subject", "Requester ID", "Date Created", "Last Updated"])
	    
	    for k in tickets:
	        table.add_row(k[ : 5])
	    return table

	except ModuleNotFoundError:
		print("PrettyTable module not found")


def ticket_format(ticket):
	"""

	This function formats induvidual ticket's data into an easily readable format

	Parameters : 
		ticket (list): a list containing data of an particular ticket
	
	Return : 
		output : a formatted string with all the data

	"""

	output = (f"Ticket ID : {ticket[0]}\n"
            f"Status : {ticket[5]}\n"
            f"Priority : {ticket[6]}\n"
            f"Requester ID : {ticket[2]}\n"
            f"Subject : {ticket[1]}\n"
           )

	description = "\n"
	count = 0

	for k in ticket[7]:
		if count == 0:
			if k == " ":
				pass
			else:
				description += k
		else:
			description += k
		count += 1
		if count == 100:
			if description[-1] != "\n":
				description += "\n"
			count = 0
	if description[-1] != "\n":
		description += "\n"

	output += (f"Description : {description}\n"
            f"Email CC IDs : {ticket[9]}\n"
            f"Collaborators IDs : {ticket[10]}\n"
            f"Created At : {ticket[3]}\n"
            f"Updated At : {ticket[4]}\n"
            f"Due At : {ticket[8]}\n"
              )

	output = "\n" + "-" * 120 +  "\n" + output + "-" * 120 + "\n"
	return output


def ticket_details(ticket_id):
	"""

	This function returns a detailed data regarding a given ticket ID.
	It returns None if data for a given ticket ID does not exist

	Parameters : 
		ticket_id (int) : the ticket id of the ticket whose data is being searched for
	
	Return : 
		(str) ticket details if exist else return None

	"""

	global has_more, next_page
	json_data = get_json(url_master, user, passwd)
	while has_more == True:
		tickets = get_tickets(json_data)
		for k in tickets:
			if k[0] == ticket_id:
				return ticket_format(k)
		json_data = get_json(next_page, user, passwd)
	else:
		return None


def time_format(time):
	"""

	This function formats the date and time extracted from the json file to a easily
	readable format

	Parameters : 
		time : the string representing time from the json file

	Retrun : 
		(str) a string representing the date and time in an easily readable format

	"""
	temp = time.split("T")
	return "Date : " + temp[0] + " - Time : " + temp[1][ : -1]


def ui(url, user, passwd):
	"""

	This function runs the frontend of the program. It uses a Command line Iterface
	for the user to interact with the program

	Parameters : 
		url (str) : the url of the API
		user (str) : the user id of the API
		passwd (str) : the password needed for the API

	"""
	global url_master, has_more, next_page, prev_page
	while True:

		print(("*" * 50) + "Zendesk Ticket Viewer" + ("*" * 50))
		print("""
				Enter number to select the option:
				 * (1) View All Tickets
				 * (2) View Details of a Ticket
				 * (q) Quit
			  """)

		option = input("\t\t\t\tOption : ")

		if option == "1":

			while True:
				if url == None:
					json_data = get_json(url_master, user, passwd)
				else:
					json_data = get_json(url, user, passwd)

				if len(json_data) == 0:
					print("No Tickets Recieved")
					break
				else:
					tickets = get_tickets(json_data)

				print(display_tickets(tickets))
				prev_exist = False
				next_exist = False
				# if (has_more == True):
				if requests.get(prev_page, auth=(user, passwd), timeout = 5).json()["tickets"] != []:
					print(" * (1) Prev Page")
					prev_exist = True
				if requests.get(next_page, auth=(user, passwd), timeout = 5).json()["tickets"] != []:
					print(" * (2) Next Page")
					next_exist = True
				print(" * (q) Exit")
				opt = input("Enter Page [1 - 2] or (q) exit : ")
				print()

				if opt == "q":
					break
				elif opt.isalpha():
					print("Please Enter a Valid Page Number\n")
				elif int(opt) == 1:
					if prev_exist == False:
						print("There is no Previous Page\n")
					else:
						url = prev_page
				elif int(opt) == 2:
					if next_exist == False:
						print("There is no Next Page\n")
					else:
						url = next_page
				else:
					print("Please Enter a Valid Page Number\n")

		elif option == "2":

			ticket_id = input("Enter the Ticket ID No. : ")

			while ticket_id.isdigit() == False:
				print("\nInput a valid Ticket ID\n")
				ticket_id = input("Enter the Ticket ID No. : ")
			ticket = ticket_details(int(ticket_id))

			if (ticket == None):
				print("\nTicket with the given Ticket ID does not exist\n")
			else:
				print(ticket)

		elif option == "q":

			print("Thank you for using Zendesk Ticket Viewer")
			exit()

		else:

			print("\nChoose a Valid Option\n")

if __name__ == "__main__":

	ui(url, user, passwd)






