from stravalib.client import Client
from stravalib import unithelper

client = Client()

# The access token is the final result from OAuth
client.access_token = ''

athlete = client.get_athlete()
activities = client.get_activities()

activity_list = list(activities)

total_activities = len(activity_list)

print("Total activities retrieved: {total}".format(total=total_activities))

def createTimestamp(ts): # creating timestamp string from timestamp object
	return '{year}-{month}-{day} {hour}:{minute}:{second}'.format(year=ts.year, month=ts.month, day=ts.day, hour=ts.hour, minute=ts.minute, second=ts.second)

def xstr(s):
	if s is None:
		return ''
	else:
		return str(s)

print 'Opening file to write...'
outputfile = open('runLogsSorted.csv', 'a') # Append the entry for each run to this file

schema = '"ID","Name","Distance (mi)","Moving time (s)","Elapsed time (s)","Elevation gain (ft)","Avg speed (mph)","Max speed (mph)","Avg cadence","Avg temp (C)","Avg HR","Max HR","Calories","Shoes","Start timestamp (local)","Start Lat","Start Lng","End Lat","End Lng","City","State","Country","Achievements","Kudos","Workout type"\n'
print 'Writing schema...'
outputfile.write(schema)

runs = 0
print 'Writing activities...'
for x in range(total_activities-1,-1,-1):
	curr_activity = activity_list[x]
	if curr_activity.type == 'Run':
		print("Writing activity {i} (Run): {act_id}".format(i=x, act_id=curr_activity.id))
		curr_activity_full = client.get_activity(curr_activity.id)
		record = ''
		record = record + '"' + xstr(curr_activity_full.id) + '",'
		record = record + '"' + xstr(curr_activity_full.name) + '",'

		record = record + '"' + xstr(unithelper.miles(curr_activity_full.distance).num) + '",'
		record = record + '"' + xstr(curr_activity_full.moving_time.seconds) + '",'
		record = record + '"' + xstr(curr_activity_full.elapsed_time.seconds) + '",'
		record = record + '"' + xstr(unithelper.feet(curr_activity_full.total_elevation_gain).num) + '",'
		record = record + '"' + xstr(unithelper.miles_per_hour(curr_activity_full.average_speed).num) + '",'
		record = record + '"' + xstr(unithelper.miles_per_hour(curr_activity_full.max_speed).num) + '",'
		record = record + '"' + xstr(curr_activity_full.average_cadence) + '",'
		record = record + '"' + xstr(curr_activity_full.average_temp) + '",'
		record = record + '"' + xstr(curr_activity_full.average_heartrate) + '",'
		record = record + '"' + xstr(curr_activity_full.max_heartrate) + '",'
		record = record + '"' + xstr(curr_activity_full.calories) + '",'

		record = record + '"' + xstr(curr_activity_full.gear.name) + '",'
		record = record + '"' + xstr(createTimestamp(curr_activity_full.start_date_local)) + '",'

		start_lat = ''
		start_lng = ''
		end_lat = ''
		end_lng = ''
		if curr_activity_full.start_latlng is not None:
			start_lat = curr_activity_full.start_latlng.lat
			start_lng = curr_activity_full.start_latlng.lon
		if curr_activity_full.end_latlng is not None:
			end_lat = curr_activity_full.end_latlng.lat
			end_lng = curr_activity_full.end_latlng.lon
		record = record + '"' + xstr(start_lat) + '",'
		record = record + '"' + xstr(start_lng) + '",'
		record = record + '"' + xstr(end_lat) + '",'
		record = record + '"' + xstr(end_lng) + '",'

		record = record + '"' + xstr(curr_activity_full.location_city) + '",'
		record = record + '"' + xstr(curr_activity_full.location_state) + '",'
		record = record + '"' + xstr(curr_activity_full.location_country) + '",'
		record = record + '"' + xstr(curr_activity_full.achievement_count) + '",'
		record = record + '"' + xstr(curr_activity_full.kudos_count) + '",'
		record = record + '"' + xstr(curr_activity_full.workout_type) + '"\n'
		outputfile.write(record)
		runs+=1
	else:
		print("Skipping activity {i} ({type}): {act_id}".format(i=x, type=curr_activity.type, act_id=curr_activity.id))

print("Total runs recorded: {runs}".format(runs=runs))
outputfile.close()