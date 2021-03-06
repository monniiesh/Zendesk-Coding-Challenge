# Zendesk Ticket Viewer

## Zendesk Coding Challenge

Zendesk is a customer service tool that allows the creation and management of support tickets. Your company needs you to build a Ticket Viewer that will:<br />
● Connect to the Zendesk API<br />
● Request all the tickets for your account<br />
● Display them in a list<br />
● Display individual ticket details<br />
● Page through tickets when more than 25 are returned<br />

## Setup
### 1. Install all the necessary packages

run the following command in the location of the program files using terminal

> pip3 install -r requirements.txt

if the above command does not work, then pip3 install each of the required module in requirements.txt seperately

### 2. Setting up the API

open zendesk.py and ZendeskTester.py, and fill in the API, user and password information<br />
**Note** : the API should be of the format as shown below
> https://example.zendesk.com/api/v2/tickets.json?page[size]=25

### Usage

run the following command in the location of the program files using terminal

> python3 zendesk.py

1. Option (1) displays all the tickets in a table format recieved from the Zendesk API<br />
    select (1) to move to prev page and (2) to move to next page

2. Option (2) displays detailed information of a particular ticket based on the inputted ticket id

3. option (q) quits the program

### Running the Testers

run the following command in the location of the program files using terminal

> pytest ZendeskTester.py -vv
