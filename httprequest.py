# python 3
import urllib.request
# python 2.7
#import urllib2
import json
import time
import datetime

starttime = datetime.datetime.now()

apikey = open('key.dat', 'r').read()

stopseqnum = 1704492188 # stop at this index


def accessMatchHistory(lastseqnum):
	succeed = False
	while not succeed:
		try:
			matchHist = json.loads(urllib.request.urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/V001/?key=" + apikey + "&start_at_match_seq_num=" + str(lastseqnum)).read().decode("utf-8"))
			succeed = True
		except urllib.error.HTTPError:
			print("WOAH")
			time.sleep(30)
		except:
			print("Some other error has occured")
			time.sleep(30)
	return matchHist

def fetch():
	recordfile = open('record.dat', 'r')
	lastseqnum = recordfile.read()
	recordfile.close()
	matches = open('./testing/data.csv', 'a')
	data = accessMatchHistory(lastseqnum)
	for i in range(100):
		curmatch = data['result']['matches'][i]
		match_id = curmatch['match_id']
		lastseqnum = curmatch['match_seq_num']
		print(str(i + 1) + "/100 " + str(match_id))
		if 'picks_bans' in curmatch:
			print(str(match_id) + " captain's mode")
			matches.write(str(match_id) + ",")
			matches.write(str(curmatch['radiant_win']) + ",")
			matches.write(str(curmatch['duration']))
			picklist = curmatch['picks_bans']
			for i in range(len(picklist)):
				matches.write("," + str(picklist[i]['is_pick']) + "," + str(picklist[i]['team']) + "," + str(picklist[i]['hero_id']))
			matches.write("\n")
	matches.close()
	# if any error occured before this point it must have occured at "lastseqnum"

	recordfile = open('record.dat', 'w')
	# thus we can safely start at the next one up...
	recordfile.write(str(lastseqnum + 1))
	recordfile.close()
	print("CYCLE FINISHED: " + str(stopseqnum - lastseqnum))
	if lastseqnum >= stopseqnum:
		return False
	else:
		return True

processFlag = True
while processFlag:
	processFlag = fetch()
	time.sleep(1)

endtime = datetime.datetime.now()

print("Started at " + starttime.isoformat() + "\nEnded at: " + endtime.isoformat())
