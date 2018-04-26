
from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout


# importing the requests library
import requests
import googlemaps

city=""
checkin=""
checkouts=""
interest=""
duration=0

budget=-1
time=-1



# api-endpoint
#URL = "https://api.sandbox.amadeus.com/v1.2/flights/extensive-search"
def call_hotel():
	global city,checkin,checkout,interest,duration
	URL = "https://api.sandbox.amadeus.com/v1.2/hotels/search-circle"
	 
	# location given here
	apikey="XTWA1DICDxHhoa8ZDuZWeLLfAnPbm2HB" 
	#date=
	#origin=
	#duration=
	# defining a params dict for the parameters to be sent to the API
	#PARAMS = {'apikey':apikey,'origin':'DEL','destination':'JAI','departure_date':'2018-06-16','duration':3}
	PARAMS = {'apikey':apikey,'latitude':26.9124,'longitude':75.7873,'radius':42,'check_in':checkin,'check_out':checkout}
	  

	# sending get request and saving the response as response object
	r = requests.get(url = URL, params = PARAMS)
	 
	# extracting data in json format
	data = r.json()

	#print(data)
	hotels=[]
	for i in range(2):
		print(data['results'][i]['property_name'])
		hotels.append(data['results'][i]['property_name'])
	return hotels

def getloc():

	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	#print(lat,lon)
	return lat,lon
def getplacefromid(id_list):
	gmaps = googlemaps.Client(key='AIzaSyBXu-MjQ_fWNYpwL_UJdPIbc0EtYp2t6sQ')
	nearby_place=[]
	for id in id_list:
		place_id = id
		# Geocoding an address
		geocode_result = gmaps.reverse_geocode(place_id)


		#print (geocode_result)
		#r=json.dumps(geocode_result,indent=4)
		#print(r)

		p=geocode_result[0]['address_components'][1]['long_name']
		nearby_place.append(p)
	return nearby_place

def getid(radius,lat,lon,place):
	url="https://maps.googleapis.com/maps/api/place/radarsearch/json"
	loc=str(lat)+","+str(lon)
	params = {
	'location': loc,
	'radius': 5000,
	'type': place,
	'key':'AIzaSyAEipbDYwLFjS54ddnMJW13mMYj0J3ySGI'

	}
	r = requests.get(url = url, params = params)

	data=r.json()
	#print(data)
	print(data)
	id_list=[]
	for i in range(5):
		id_list.append(data['results'][i]['place_id'])
	return id_list




app = Flask(__name__)



@app.route('/webhook', methods=['POST'])
def webhook():
	global city,checkin,checkout,time,budget,duration,interest
	

	req = request.get_json(silent=True, force=True)


	if(req.get("result").get("action")=="ask_time"):

		param=req.get("result").get("parameters")
		#print(param['unit-currency']['amount'])
		budget=param['unit-currency']['amount']
		res = {"speech":"Please Enter estimated duration of your trip!!!",
		"displayText":"Please Enter estimated duration of your trip!!!",
		"source":"ask_time"}
		res = json.dumps(res, indent=4)
		# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r


	elif(req.get("result").get("action")=="input.welcome"):
		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": "Welcome to Course Selector!!!!Here are the courses we provide!!",
											"displayText":"Welcome to Course Selector!!!!Here are the courses we provide!!"
											},
											{
											"type": 0,
											"speech": "1.Machine Learning",
											"displayText":"1.Machine Learning"
								
											},
											{
											"type":0,
											"speech":"2.Cyber Security",
											"displayText":"2.Cyber Security"
											},
											{
											"type":0,
											"speech":"3.BioInformatics"
											
											},
											{
											"type":0,
											"speech":"4.Cryptography"
										
											},
											{
											"type":0,
											"speech":"5.Data Structures & Algorithms"
										
											},
											{
											"type":0,
											"speech":"Get more information about any course."
										
											}
											],
											"source": "Default Welcome Intent"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

	elif(req.get("result").get("action")=="reach"):
		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": "Which Mode of Transport would you prefer?",
											
											},
											{
											"type": 0,
											"speech": "1.ROAD",
											
								
											},
											{
											"type":0,
											"speech":"2.RAIL",
											
											},
											{
											"type":0,
											"speech":"3.AIR",
											
											}
								
											],
											"source": "reach"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r


	#Course ke baare mein info
	elif(req.get("result").get("action")=="askcourse"):
		param=req.get("result").get("parameters")
		method=param["course"]

		desc={'Machine Learning':'ML',
			'Cryptography':'CR',
			'Bioinformatics':'BI',
			'Data Structures & Algorithms':'DSA',
			'Cyber Security':'CS'}
		link={'Machine Learning':'ML',
			'Cryptography':'CR',
			'Bioinformatics':'BI',
			'Data Structures & Algorithms':'DSA',
			'Cyber Security':'CS'}
				

		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": desc[method],
											
											},
											{
											"type": 0,
											"speech": link[method],
											
											},
											{
											"type": 0,
											"speech":"Please also enter the following details as these will help us make better course suggestions for you!!",
											
											},
											{
											"type": 0,
											"speech":"Could you Tell us about your interests!",
											
											},
											
											],
											"source": "askcourse"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

	#askinterest
	elif(req.get("result").get("action")=="askinterest"):
		param=req.get("result").get("parameters")
		interest=param["interest"]

		
				

		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": "Thanks! Also can you also tell us your preferred course duration!",
											
											}
											
											],
											"source": "askinterest"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

	#askduration
	elif(req.get("result").get("action")=="askduration"):
		param=req.get("result").get("parameters")
		duration=param['duration']['amount']

		
				

		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": "Thanks for Providing the info!! You have entered "+interest+"as your area of interest and you want a course for an estimated duration of "+str(duration) + " months" ,
											
											},
											{
											"type": 0,
											"speech": "Now you can surf the site so that our automated computer vision model can correctly identify which courses you like! And based on your area of interest and duration required we would suggest you the most appropriate courses." ,
											
											}
											
											],
											"source": "askduration"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r




	elif(req.get("result").get("action")=="reachinfo"):
		param=req.get("result").get("parameters")
		method=param["toreach"]
		dict={'air':'Rajasthan is a tourist hub and therefore well-connected by air. ',
			'rail':'Rail is one of the best ways to travel to Rajasthan from anywhere within India as it is both, comfortable and economical.',
			'road':'Rajasthan has 20 national highways passing through the state, spanning a distance of about 6373 kms.'}
		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": dict[method],
											
											}
											
											],
											"source": "reachinfo"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r


	elif(req.get("result").get("action")=="helpdesk"):
		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": "Contact Info",
											
											}
											
											],
											"source": "helpdesk"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r


	elif(req.get("result").get("action")=="plantrip"):
		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": "Planning Trip!!!PLease Kindly enter your Budget!",
											
											}
											
											],
											"source": "plantrip"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r


	elif(req.get("result").get("action")=="nearby"):

		param=req.get("result").get("parameters")
		place=param["places"]
		lat,lon=getloc()
		id_list=getid(500,lat,lon,place)
		print(id_list)
		name_list=getplacefromid(id_list)
		print(name_list)
		if len(name_list)==0:
			name_list.append("No "+place+" found!")


		res = {"speech": "",
											"messages": [
											{
											"type": 0,
											"speech": "Sure showing them right away!!!!",
											
											},
											{
											"type":0,
											"speech":name_list[0]
											},
											{
											"type":0,
											"speech":name_list[1]
											},
											{
											"type":0,
											"speech":name_list[2]
											},
											{
											"type":0,
											"speech":name_list[3]
											},
											{
											"type":0,
											"speech":name_list[4]
											}
											
											],
											"source": "nearby"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r


		
	elif(req.get("result").get("action")=="thank"):
		param=req.get("result").get("parameters")
		#print(param['duration']['amount'])
		time=param['duration']['amount']
		res = {
		"speech":"Thanks for providing the information.",
		"displayText":"Thanks for providing the information.",
		"source":"thank_user"
		}
		res = json.dumps(res, indent=4)
		# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

	elif(req.get("result").get("action")=="getplace"):
		param=req.get("result").get("parameters")
		city=param['place']
		res = {
		"speech":"Please Enter a tentative checkin date!!!",
	"displayText":"Please Enter a tentative checkin date!!!",
	"source":"entercheckin"
		}
		res = json.dumps(res, indent=4)
		# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

	elif(req.get("result").get("action")=="getcheckin"):
		param=req.get("result").get("parameters")
		checkin=param['date']
		d=checkin.split('-')
		day=d[0]
		month=d[1]
		year=d[2]
		checkin=day+"-"+month+"-"+year
		res = {
		"speech":"Please Enter a tentative checkout date!!!",
	"displayText":"Please Enter a tentative checkout date!!!",
	"source":"entercheckout"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

	elif(req.get("result").get("action")=="getcheckout"):
		param=req.get("result").get("parameters")
		checkout=param['date']
		d=checkout.split('-')
		day=d[0]
		month=d[1]
		year=d[2]
		checkout=day+"-"+month+"-"+year
		hotels=call_hotel()
		
		res={
		"speech":hotels[0]+","+hotels[1],
	"displayText":hotels[0]+","+hotels[1],
	"source":"final_output_hotel"
		}
		res = json.dumps(res, indent=4)
		# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r



	elif(req.get("result").get("action")=="getstart"):
		param=req.get("result").get("parameters")
		city=param['place']
		res = {
		"speech":"Please enter your preferred destination!!!!!",
	"displayText":"Please enter your preferred destination!!!!!",
	"source":"askend"
		}
		res = json.dumps(res, indent=4)
		# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r
	elif(req.get("result").get("action")=="getend"):
		param=req.get("result").get("parameters")
		city=param['place']
		res = {
		"speech":"Please enter Start Date!!!!!",
	"displayText":"Please enter Start Date!!!!!",
	"source":"askstartdate"
		}
		res = json.dumps(res, indent=4)
		# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

	elif(req.get("result").get("action")=="getstartdate"):
		param=req.get("result").get("parameters")
		city=param['date']
		res = {
		"speech":"Please enter End Date!!!!!",
	"displayText":"Please enter End Date!!!!!",
	"source":"askenddate"
		}
		res = json.dumps(res, indent=4)
	# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r

	elif(req.get("result").get("action")=="getenddate"):
		param=req.get("result").get("parameters")
		city=param['date']
		res = {
		"speech":"Here is your train!!!!!",
	"displayText":"Here is your train!!!!!",
	"source":"output_train"
		}
		res = json.dumps(res, indent=4)
		# print(res)
		r = make_response(res)
		r.headers['Content-Type'] = 'application/json'
		return r
			

		
		


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
