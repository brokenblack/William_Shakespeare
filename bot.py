#!/usr/bin/python
# -*- coding:utf-8 -*-
 
import re
import json
import urllib.request
import random
from itertools import islice
import oauth2 as oauth
import sys

from plurk_oauth import PlurkAPI

 
plurk = PlurkAPI('APP_KEY', 'APP_SECRET')
plurk.authorize('ACCEESS_TOKEN', 'ACCESS_TOKEN_SECRET')
 
comet = plurk.callAPI('/APP/Realtime/getUserChannel')
comet_channel = comet.get('comet_server') + "&new_offset=%d"
jsonp_re = re.compile('CometChannel.scriptCallback\((.+)\);\s*');

keywords = [u'什麼', u'甚麼', u'what', u'?', u'？', u'沙小', u'啥']
others = dict({u'儚い': '* https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif ** https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif ** https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif * 儚い~ * https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif ** https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif ** https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif *',
		u'小薰': '......つ！！！！ (臉紅 https://emos.plurk.com/3110c3c233c48956057ec5c4628e3629_w39_h48.png',
		u'薰': '什麼事? 可愛的小貓咪?',
		u'喵': '喔呀，是位可愛的小貓咪呢',
		u'嗚欸': '啊，花音，你又迷路了嗎?',
		u'嗚誒': '啊，花音，你又迷路了嗎? 我們一起走吧',
		u'https://emos.plurk.com/a4ed9585c8b95b624483d95750b1bd0b_w48_h48.jpeg': '這不是千聖嗎，真是命運一般的邂逅啊',
		'': 'https://emos.plurk.com/af5e30f9838bee2712b3b82440b592e1_w48_h44.jpg'
		})
emojis = [u'https://emos.plurk.com/7e6738afd5272b8e86fca5f9ce76f6c0_w48_h48.gif',
		u'https://emos.plurk.com/99bec14fa184cc199bfd48a32e4254db_w48_h48.gif',
		u'https://emos.plurk.com/0e6035708fcb34472c66bc025dce3c10_w48_h48.gif',
		u'https://emos.plurk.com/dd230e309fa02ee98da5dad64b4ceeb6_w48_h48.png'
		]
emotion = 'https://emos.plurk.com/af5e30f9838bee2712b3b82440b592e1_w48_h44.jpg'

new_offset = -1
import time
while True:
	time.sleep(3)
	plurk.callAPI('/APP/Alerts/addAllAsFriends')
	req = urllib.request.urlopen(comet_channel % new_offset, timeout=80)
	rawdata = req.read().decode('utf-8')
	match = jsonp_re.match(rawdata)
	if match:
		rawdata = match.group(1)
	data = json.loads(rawdata)
	new_offset = data.get('new_offset', -1)
	msgs = data.get('data')
	if not msgs:
		continue
	for msg in msgs:
		if msg.get('type') == 'new_plurk': 
			pid = msg.get('plurk_id')
			content = msg.get('content_raw')
			if msg.get('replurkers') == []:
				with open('New Text Document.txt', 'r',encoding="utf-8") as f:
					e = f.read().splitlines()
					d = random.choice(e) 
					formatted_output = d.replace('\\n', '\n')
					plurk.callAPI('/APP/Responses/responseAdd',
									{'plurk_id': pid,
									'content': formatted_output,
									'qualifier': ':' })
			

		elif msg.get('type') == 'new_response':
			pid = msg.get('plurk_id')
			content = msg.get('response').get('content_raw')
			if content.find('@William_Shakespear') != -1:
				not_found = True
				for k in keywords:
					if content.find(k) != -1:
						uid = msg.get('user')
						uuu = [ uid[i]['nick_name'] for i in uid ][0]
						emoji = random.choice(emojis)
						plurk.callAPI('/APP/Responses/responseAdd',
										{'plurk_id': pid,
										'content': '@%s: 所以說，就是這麼一回事' %uuu + emoji,
										'qualifier': ':'})
						not_found = False
						break
				if not_found:
					for ha in others.keys():
						if content.find(ha) != -1:
							uid = msg.get('user')
							uuu = [ uid[i]['nick_name'] for i in uid ][0]
							plurk.callAPI('/APP/Responses/responseAdd',
											{'plurk_id': pid,
											'content': '@%s: {}'.format(others[ha])%uuu, 
											'qualifier': ':'})
							break

		'''	else:
				uid = msg.get('user')
				uuu = [ uid[i]['nick_name'] for i in uid ][0]
				plurk.callAPI('/APP/Responses/responseAdd',
									{'plurk_id': pid,
									'content': '@%s: '%uuu + emotion,
									'qualifier': ':'})  '''