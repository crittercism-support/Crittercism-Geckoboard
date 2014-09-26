#! /usr/bin/python

import unirest, json, time, urllib2
from datetime import datetime
from urllib2 import urlopen
from timeit import Timer

#####################################
geckoboard_key = 'EDIT ME!' #geckoboard api key, find from geckoboard portal
appId = 'EDIT ME!' #appid of crittercism registered app
access_token = 'EDIT ME!' #request access_token by using the provided client id
#####################################

#get and push api status
url = 'https://developers.crittercism.com:443/v1.0/base'
request_api = urllib2.Request(url)
response_api = json.load(urllib2.urlopen(request_api))
#get response time
def fetch():
	response_page = urlopen(url)
timer = Timer(fetch)
response_time = timer.timeit(1)
#get api status
status = response_api['status']
if status == 'active':
	status = "Up"
else:
	status = "Down"
#push api status
"""create monitoring widget"""
response = unirest.post(
	"https://push.geckoboard.com/v1/send/106305-129ea4fa-9a17-4f61-801b-a377c60e9b67",
	headers={"Accept": "application/json", "Content-Type": "application/json"},
	params=json.dumps({
	  "api_key": geckoboard_key,
	  "data": {
  "status": status,
  "downTime": "",
  "responseTime": "%.3f" % response_time
}}))

#fetch daily app loads
def fetch_daily_appLoads(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		headers={
			"Content-Type": "application/json",
			"Authorization" : "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
			"graph": "appLoads",
			"duration": 1440,
			"appId": appId,
			}})
		)
	try:
		return response.body['data']['series'][0]['points'][0]
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_app_loads')
		return  None

#push daily app loads
"""create number widget"""
def push_daily_appLoads(appLoads):
	response = unirest.post(
		"https://push.geckoboard.com/v1/send/106305-3ace4a63-945e-423f-88c3-c7c9c6325374",
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
		  "api_key": geckoboard_key,
		  "data": {
	  "item": [
	    {
	      "value": appLoads,
	      "text": "Daily App Loads"
	    }
	  ]
	}}))

#fetch daily app crashes
def fetch_daily_app_crashes(access_token,appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		headers={
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
			"graph": "crashes",
			"duration": 1440,
			"appId": appId
			}})
		)
	try:
		return response.body['data']['series'][0]['points'][0]
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_app_crashes')
		return None

#push daily app crashes
"""create number widget"""
def push_daily_app_crashes(crashes):
	response = unirest.post(
	        "https://push.geckoboard.com/v1/send/106305-dc7d33b9-4023-4c1f-acc7-9559cd804671",
	        headers={"Accept": "application/json", "Content-Type": "application/json"},
	        params=json.dumps({
	          "api_key": geckoboard_key,
	          "data": {
	  "item": [
	    {
	      "value": crashes,
	      "text": "Daily App Crashes"
	    }
	  ]
	}}))

#fetch daily active users
def fetch_daily_active_users(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		headers={
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
			"graph": "dau",
			"duration": 1440,
			"appId": appId
			}})
		)
	try:
		return response.body['data']['series'][0]['points'][0]
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_app_loads')
		return None

#push daily active users
"""create number widget"""
def push_daily_active_users(dau):
	response = unirest.post(
	        "https://push.geckoboard.com/v1/send/106305-64e65b64-30f5-46f0-9edb-43b25d5f6c10",
	        headers={"Accept": "application/json", "Content-Type": "application/json"},
	        params=json.dumps({
	          "api_key": geckoboard_key,
	          "data": {
	  "item": [
	    {
	      "value": dau,
	      "text": "Daily Active Users"
	    }
	  ]
	}}))

#fetch daily crash percent
def fetch_daily_crash_percent(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/graph",
		headers={
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
			"value_type": "percent",
			"graph": "crashPercent",
			"duration": 1440,
			"appId": appId
			}})
		)
	try:
		crash_rate = float(response.body['data']['series'][0]['points'][0])
		return crash_rate / 100
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_crash_percent')
		return None

#push daily crash percent
"""create number widget"""
def push_daily_crash_percent(crash_rate):
	response = unirest.post(
	        "https://push.geckoboard.com/v1/send/106305-05aaac70-bb20-4533-a129-03a6fe9fabb5",
	        headers={"Accept": "application/json", "Content-Type": "application/json"},
	        params=json.dumps({
	          "api_key": geckoboard_key,
	          "data": {
	  "item": [
	    {
	      "value": crash_rate,
	      "text": "Daily Crash Rate"
	    }
	  ]
	}}))

#fetch daily crashes by os
def fetch_daily_crashes_os(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/pie",
		headers={
			"Content-Type": "application/json", 
			"Authorization" : "Bearer %s" % access_token
			},
		params=json.dumps({"params":{
				"graph": "crashes",
				"duration": 1440, 
				"groupBy": "os",
				"appId": appId
			}})
		)

	os_list = []
	try:
		for series in response.body['data']['slices']:	
			os_list.append((series['label'], series['value']))
		os_list = sorted(os_list, key=lambda x: x[1], reverse=True)[0:4]
		return map(list, zip(*os_list))
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_crashes_os')
		return [None, None]

#push daily crashes by os
"""create pie chart"""
def push_daily_crashes_os(os_list):
	response = unirest.post(
		"https://push.geckoboard.com/v1/send/106305-941b1040-d241-4106-a78e-6603c2a29a53",
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
		  "api_key": geckoboard_key,
		  "data": {
  	"item": [
 	   {
 	     "value": os_list[1][0], #os one value
 	     "label": os_list[0][0], #os name
 	   },
 	   {
 	     "value": os_list[1][1], #os two value
 	     "label": os_list[0][1], #os name
 	   },
 	   {                                                                                                                                              
 	     "value": os_list[1][2], #os three value                                                                                                                       
 	     "label": os_list[0][2], #os name                                                                                                                            
 	   },  
 	   {                                                                                                                                              
    	  "value": os_list[1][3], #os three value                                                        
    	  "label": os_list[0][3], #os name                                                                                                                           
    	}  
  	]
	}}))

#fetch daily app loads by device
def fetch_daily_app_loads_device(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/errorMonitoring/pie",
		headers={
			"Content-Type": "application/json",
			"Authorization" : "Bearer %s" % access_token,
			},
		params=json.dumps({"params":{
			"graph": "appLoads",
			"duration": 1440,
			"appId": appId,
			"groupBy": "device"
		}})
		)
	device_list = []
	try:
		for device in response.body['data']['slices']:
			device_list.append((device['label'], device['value']))
		device_list = sorted(device_list, key=lambda x: x[1], reverse=True)[0:5]
		return map(list, zip(*device_list))
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_app_loads_device')
		return [None, None]

#push daily app loads by device
"""create funnel chart since Geckoboard API has no bar chart"""
def push_daily_app_loads_device(device_list):
	response = unirest.post(
	#	"https://push.geckoboard.com/v1/send/106305-6557c1f1-9c30-4701-8940-971fc1b7eb3c",
		"https://push.geckoboard.com/v1/send/106305-58cd87cd-15ac-409a-a379-f7097abc1e9d",
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
		  "api_key": geckoboard_key,
		  "data": {
	#"type": "reverse",
	"percentage": "hide",
	"item": [
	{
	"value": device_list[1][0], #apploads device one 
	"label": device_list[0][0] #device one name
	},
	{
	"value": device_list[1][1], #apploads device two
	"label": device_list[0][1] #device two name
	},
	{
	"value": device_list[1][2], #apploads device three
	"label": device_list[0][2] #device three name
	},
	{
	"value": device_list[1][3], #apploads device four
	"label": device_list[0][3] #device four name
	},
	{
	"value": device_list[1][4], #apploads device five
	"label": device_list[0][4] #device five name
	}                                                      
	]
	}}))
	 
#fetch service monitoring error rate (top three offenders)
def fetch_daily_service_monitoring_rate(access_token, appId):
	response = unirest.post(
		"https://developers.crittercism.com:443/v1.0/performanceManagement/pie",
		headers={
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" % access_token,
			},
		params=json.dumps({"params":{
			"groupBy": "service",
			"graph": "errors",
			"duration": 60,
			"appId": appId
			}})
		)
	service_list = []
	try:
		for service in response.body['data']['slices']:
			service_list.append((service['label'], service['value']))
		service_list = sorted(service_list, key=lambda x: x[1], reverse=True)[0:4]
		return map(list, zip(*service_list))
	except KeyError as e:
		print 'ERROR: Could not access %s in %s.' % (str(e), 'fetch_daily_service_monitoring_rate')
		return [None, None]

#push service monitoring error rate (top three offenders)
"""create funnel chart since Geckoboard API has no bar chart"""
def push_daily_service_monitoring_rate(service_list):
	response = unirest.post(
		"https://push.geckoboard.com/v1/send/106305-e02412d0-eef7-47a6-82f8-39b8e8d5efc6",
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		params=json.dumps({
		  "api_key": geckoboard_key,
		  "data": {
	"type": "reverse",
	"percentage": "hide",
	"item": [
	{
	"value": "%.2f" % service_list[1][0], #seconds 
	"label": service_list[0][0] #name of request
	},
	{
	"value": "%.2f" % service_list[1][1], #seconds
	"label": service_list[0][1] #name of request
	},
	{
	"value": "%.2f" % service_list[1][2], #seconds
	"label": service_list[0][2] #name of request
	}                                                            
	]
	}}))

def main():
#updates daily app loads
	appLoads = fetch_daily_appLoads(access_token, appId)
	if appLoads is not None:
		push_daily_appLoads(appLoads)
	time.sleep(1)

#updates daily app crashes
	crashes = fetch_daily_app_crashes(access_token, appId)
	if crashes is not None:
		push_daily_app_crashes(crashes)
	time.sleep(1)

#updates daily active users
	dau = fetch_daily_active_users(access_token, appId)
	if dau is not None:
		push_daily_active_users(dau)
	time.sleep(1)

#updates daily crash percent
	crash_rate = fetch_daily_crash_percent(access_token, appId)
	if crash_rate is not None:
		push_daily_crash_percent(crash_rate)
	time.sleep(1)

#updates daily crashes by os
	os_list = fetch_daily_crashes_os(access_token, appId)
	if os_list is not None:
		push_daily_crashes_os(os_list)
	time.sleep(1)

#updates daily app loads by device
	device_list = fetch_daily_app_loads_device(access_token, appId)
	if device_list is not None:
		push_daily_app_loads_device(device_list)
	time.sleep(1)

#updates daily service monitoring rate (error rate)
	service_list = fetch_daily_service_monitoring_rate(access_token, appId)
	if service_list is not None:
		push_daily_service_monitoring_rate(service_list)
	time.sleep(1)
		



if __name__=='__main__':
	main()

