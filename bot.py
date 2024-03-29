#!/usr/bin/python
# -*- coding:utf-8 -*-
 
import re
import json
import urllib.request
import random
from itertools import islice
#import oauth2 as oauth
import sys

from plurk_oauth import PlurkAPI

 
plurk = PlurkAPI('APP_KEY', 'APP_SECRET')
plurk.authorize('ACCEESS_TOKEN', 'ACCESS_TOKEN_SECRET')
 
comet = plurk.callAPI('/APP/Realtime/getUserChannel')
comet_channel = comet.get('comet_server') + "&new_offset=%d"
jsonp_re = re.compile('CometChannel.scriptCallback\((.+)\);\s*');

keywords = [u'什麼', u'甚麼', u'what', u'?', u'？', u'沙小', u'啥']
others = dict({u'儚い': '* https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif ** https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif ** https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif * 儚い~ * https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif ** https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif ** https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif *',
		u'小薰': '......つ！！！！ 小千...(臉紅 https://emos.plurk.com/3110c3c233c48956057ec5c4628e3629_w39_h48.png',
		u'kaoru': '什麼事? 可愛的小貓咪?',
		u'喵': '\nhttps://emos.plurk.com/2855722f8a0cac58d9503de3999e3a16_w46_h48.jpeg 喔呀，可愛的小貓咪有什麼事呢? 這麼大的雨，待在這裡可是會感冒的喔?\nhttps://emos.plurk.com/cbf27bddd90675c4baf25fc7ce9c9ee9_w48_h47.jpeg ．．．薰，你在做什麼?\nhttps://emos.plurk.com/c998f6c405b82415369ee41a5cecb8bb_w48_h48.gif 呦，千聖，我打算給迷失的小貓咪找個家哦\nhttps://emos.plurk.com/2c98e01f6ab8b6483815c43b263e76fc_w47_h48.jpeg ．．．傘給我\nhttps://emos.plurk.com/8737ccc164cff4da40a56e1048e6d55e_w44_h48.jpeg ?\nhttps://emos.plurk.com/fff851e041880f422788fbc81f1ee159_w45_h48.jpeg 把傘給我幫你拿，這樣你也比較輕鬆吧?',
		u'貓咪': '\n哎呀 看來又有一隻小貓咪因為我的美麗 被奪去了心神\n啊~ 太美也是一種罪惡啊',
	        u'嗚欸': '啊，花音，你又迷路了嗎?',
		u'嗚誒': '啊，花音，你又迷路了嗎? 我們一起走吧',
		u'莎莎': '我的名字不叫莎莎喔，小貓咪',
	        u'千聖': '千聖是我的幼馴染呢，你也喜歡她嗎? 我也是呢 (自豪+儚い閃光',
		u'機車': '小貓咪心情不好嗎?真是儚い啊',
		u'去死': '怎麼了小貓咪? 今天很暴躁呢',
		u'瑪芬': '瑪芬最U秀了，爁藍和77也是，當然還有清風和玉鴞',
	        u'muffin': '現在可不是瑪芬時間喔',
		u'愛愛': 'https://emos.plurk.com/3110c3c233c48956057ec5c4628e3629_w39_h48.png ......つ！！！！ 小千...你在說什麼？(臉紅',
		u'煩': '唉呀，那有什麼是我能為小貓咪做的呢?',
		u'遲到': '\nhttps://emos.plurk.com/0e6035708fcb34472c66bc025dce3c10_w48_h48.gif 「我達達的馬蹄是美麗的錯誤」儚い~\n呦，花音你也要遲到了嗎？我也是哦\n__ __ __ __ __ __\nhttps://emos.plurk.com/8324a0426a714ffd48b4cba274994ab4_w48_h48.png 嗚誒誒',
		u'Leo': '啊，Leo好久不見了，你還是一樣儚い',
		u'謝': '滿足小喵咪是王子的責任呢，儚い',
		u'笑': '呀，心你的笑容還是一如改往的儚い呢',
		u'樹': '\nhttps://emos.plurk.com/c998f6c405b82415369ee41a5cecb8bb_w48_h48.gif 誒，行道樹演起來真不容易．．．\nhttps://emos.plurk.com/8d84d891658b99b6aa60e0bfd7b96811_w48_h48.png 薰前輩又在那做什麼啊．．．',
		u'leo': '\nhttps://emos.plurk.com/c998f6c405b82415369ee41a5cecb8bb_w48_h48.gif 你這樣扯著我，我可是很困擾的，小貓咪\nhttps://emos.plurk.com/7fda7cf2081d578fa8f7e7616468cac4_w48_h48.jpeg Leo是隻狗喔，薰',
		'': '': ('https://emos.plurk.com/af5e30f9838bee2712b3b82440b592e1_w48_h44.jpg',
			 'https://emos.plurk.com/a4ed9585c8b95b624483d95750b1bd0b_w48_h48.jpeg 薰她現在不在喔',
			 'https://emos.plurk.com/7e6738afd5272b8e86fca5f9ce76f6c0_w48_h48.gif',
			 'https://emos.plurk.com/03860276d09cb8c3af57f4e1f67d7a10_w48_h48.gif',
			 'https://emos.plurk.com/eb84f444b7b5ab6b4f933cb3c4e4114e_w48_h48.png',
			 'https://emos.plurk.com/a5dd8755156189f69ffc99066371ec32_w48_h48.gif (盜號')
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
			time.sleep(3)

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
						time.sleep(3)
						break
				if not_found:
					for ha in others.keys():
						if content.find(ha) != -1:
							uid = msg.get('user')
							uuu = [ uid[i]['nick_name'] for i in uid ][0]
							plurk.callAPI('/APP/Responses/responseAdd',
											{'plurk_id': pid,
											'content': '@{}: {}'.format(uuu, others[ha] if type(others[ha]) == str else random.choice(others[ha])) ,
											'qualifier': ':'})
							time.sleep(3)
							break

		'''	else:
				uid = msg.get('user')
				uuu = [ uid[i]['nick_name'] for i in uid ][0]
				plurk.callAPI('/APP/Responses/responseAdd',
									{'plurk_id': pid,
									'content': '@%s: '%uuu + emotion,
									'qualifier': ':'})  '''
