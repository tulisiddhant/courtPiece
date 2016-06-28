from django.shortcuts import render
from piece.models import * 
#from django.http import json.dumps
import random
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#import numpy as np
import json
# Create your views here.

MAX_MSG = 40
#CLUB = 1
#SPADE = 2
#DIAMOND = 3
#HEART = 4

def argmax(v1, v2, v3, v4):
	if v1 == max(v1, v2, v3, v4):
		return 0
	elif v2 == max(v1, v2, v3, v4):
		return 1
	elif v3 == max(v1, v2, v3, v4):
		return 2
	elif v4 == max(v1, v2, v3, v4):
		return 3

	
@csrf_exempt
def newRoom(request):
	context = RequestContext(request)
	roomObj = Room()
	
	#pl = Player()
	#pl.name = request.POST['player_name']
	#pl.save()
	
	roomObj.roomId = request.POST['roomId']
	roomObj.player1 = None
	roomObj.player2 = None
	roomObj.player3 = None
	roomObj.player4 = None
	roomObj.phase = 0
	#roomObj.team1score = 0
	#roomObj.team1score = 0
	#roomObj.status = 0 
	#roomObj.phase = 0
	roomObj.save()
	context['p1'] = ""
	context['p2'] = ""
	context['p3'] = ""
	context['p4'] = ""
	context['roomId'] = roomObj.roomId
	context['phase'] = roomObj.phase
	context['pId'] = -1	
		
	return render(request, 'piece/play_game.html', context)

@csrf_exempt	
def getRoomIds(request):
	objs = Room.objects.all()
	roomIds = []
	for x in objs:
		roomIds.append(x.roomId)
	
	return render(request, 'piece/chooseRoom.html', {'Room_ids':roomIds})
	

@csrf_exempt
def joinRoom(request):
	context = RequestContext(request)
	
	rId = request.POST['roomId']
	roomObj = Room.objects.get(roomId = rId)
		
	if roomObj.player1 != None and roomObj.player2 != None and roomObj.player3 != None and roomObj.player4 != None:
		return HttpResponse("Sorry. 4 players have already joined.")
		
	context['p1'] = ""
	context['p2'] = ""
	context['p3'] = ""
	context['p4'] = ""
	
	if roomObj.player1 != None:
		context['p1'] = roomObj.player1
	if roomObj.player2 != None:
		context['p2'] = roomObj.player1
	if roomObj.player3 != None:
		context['p3'] = roomObj.player1
	if roomObj.player4 != None:
		context['p4'] = roomObj.player1

	context['roomId'] = rId
	context['phase'] = roomObj.phase
	context['pId'] = -1
	
	return render(request, 'piece/play_game.html', context)


@csrf_exempt
def selectPosition(request):
	context = RequestContext(request)
	rId = request.POST['roomId']
	position = int(request.POST['position'])
	roomObj = Room.objects.get(roomId = rId)
	context['pId'] = position
	
	pl = Player()
	pl.name = request.POST['player_name']
	pl.save()
	
	if roomObj.player1 != None and roomObj.player2 != None and roomObj.player3 != None and roomObj.player4 != None:
		return HttpResponse("Sorry. 4 players have already joined.")
		
	if (position == 1 and roomObj.player1 == None):
		roomObj.player1 = pl	
	elif (position == 2 and roomObj.player2 == None):
		roomObj.player2 = pl
	elif (position == 3 and roomObj.player3 == None):
		roomObj.player3 = pl
	elif (position == 4 and roomObj.player4 == None):
		roomObj.player4 = pl
	else:
		return HttpResponse("Sorry.")
		
	roomObj.team1score = 0
	roomObj.team2score = 0
	roomObj.save()
	
	if (roomObj.player1 != None and roomObj.player2 != None and roomObj.player3 != None and roomObj.player4 != None):
		roomObj.phase = 1
		roomObj.save()
		roomObj = None
		initialiseGame(rId)
		#return redirect("/piece/initialise", context)
	#else:
	#return HttpResponse("Success")
	return HttpResponse(json.dumps({'pId':position}), content_type="application/json")
	#return render(request, 'piece/play_game.html', context)


def hasFaceCards(cards):
	face_cards = []
	
	for i in range(0,4):
		face_cards.append((i+1)*13-4)
		face_cards.append((i+1)*13-3)
		face_cards.append((i+1)*13-2)
		face_cards.append((i+1)*13-1)
	if (any(x in cards for x in face_cards)):
		return True
	else:
		return False
				
	
def initialiseGame(rId):
	roomObj = Room.objects.get(roomId = rId)
	trump = (roomObj.trump + 1) % 5
	if trump == 0:
		trump = 1
	roomObj.trump = trump
	
	flag = False
	p1cards = []
	p2cards = []
	p3cards = []
	p4cards = []
	while (flag == False):
		items = [i for i in range(0, 52)]
		random.shuffle(items)
		p1cards = items[0:13]
		p2cards = items[13:26]
		p3cards = items[26:39]
		p4cards = items[39:52]
		
		if (trump == 1):
			trumpCards = p1cards
		elif (trump == 2):
			trumpCards = p2cards
		elif (trump == 3):
			trumpCards = p3cards
		elif (trump == 4):
			trumpCards = p4cards
		
		if hasFaceCards(trumpCards[0:5]) == False:
			continue
		if hasFaceCards(p1cards) and hasFaceCards(p2cards) and hasFaceCards(p3cards) and hasFaceCards(p4cards):
			flag = True
		
	for i in p1cards:
		cr = Card()
		cr.value = i
		cr.owner = roomObj.player1
		cr.save()
		
	for i in p2cards:
		cr = Card()
		cr.value = i
		cr.owner = roomObj.player2
		cr.save()

	for i in p3cards:
		cr = Card()
		cr.value = i
		cr.owner = roomObj.player3
		cr.save()

	for i in p4cards:
		cr = Card()
		cr.value = i
		cr.owner = roomObj.player4
		cr.save()

	string = ""
	for i in sorted(p1cards):
		string += str(i) + ","	
	roomObj.p1cards = string
	
	string = ""
	for i in sorted(p2cards):
		string += str(i) + ","
	roomObj.p2cards = string

	string = ""
	for i in sorted(p3cards):
		string += str(i) + ","
	roomObj.p3cards = string
	
	string = ""
	for i in sorted(p4cards):
		string += str(i) + ","
	roomObj.p4cards = string		
	roomObj.team1score = 0
	roomObj.team2score = 0
	roomObj.phase = 1
	roomObj.save()
	
	print roomObj.p1cards
	print roomObj.p2cards
	print roomObj.p3cards
	print roomObj.p4cards

	
@csrf_exempt
def resetState(request):
	rId = request.POST['roomId']	
	roomObj = Room.objects.get(roomId = rId)	
	
	roomObj.card1 = -1
	roomObj.card2 = -1
	roomObj.card3 = -1
	roomObj.card4 = -1
	roomObj.status = 0
	roomObj.phase = roomObj.phase + 1
	roomObj.save()
	#roomObj = None
	if roomObj.phase == 15:
		initialiseGame(rId)
	
	return HttpResponse("New round")


@csrf_exempt
def setTrump(request):
	context = RequestContext(request)
	
	rId = request.POST['roomId']	
	roomObj = Room.objects.get(roomId = rId)

	trumpSuite = int(request.POST['trumpId'])-1
	roomObj.trumpSuite = trumpSuite
	roomObj.phase = 2
	roomObj.save()
	
	return HttpResponse("Success")
	#return render(request, 'piece/play_game.html', context)	
	
	
#def newSet(request):
	
	
@csrf_exempt	
def deleteRoom(request):
	rId = request.POST['roomId']	
	roomObj = Room.objects.get(roomId = rId)
	pl = roomObj.player1
	pl.delete()
	pl = roomObj.player2
	pl.delete()
	pl = roomObj.player3
	pl.delete()
	pl = roomObj.player4
	pl.delete()
	cards = Card.objects.filter(room=roomObj)
	for c in cards:
		c.delete()
	msgs = Message.objects.filter(room=roomObj)
	for m in msgs:
		m.delete()
	
	return redirect("/piece/selectRoom", context)


# input required: roomId, pId, message_start	
@csrf_exempt
def getGameStatus(request):
	context = {}
	
	#print request.POST
	rId = request.POST.get('roomId', '')
	#print "Room requested: " + rId	
	roomObj = Room.objects.get(roomId = rId)
	context['roomId'] = rId
	context['pId'] = int(request.POST['pId'])
	context['p1'] = roomObj.player1.name if roomObj.player1 != None else ""
	context['p2'] = roomObj.player2.name if roomObj.player2 != None else ""
	context['p3'] = roomObj.player3.name if roomObj.player3 != None else ""
	context['p4'] = roomObj.player4.name if roomObj.player4 != None else ""
	context['phase'] = roomObj.phase	
	if (roomObj.phase == 0):
		return HttpResponse(json.dumps(context), content_type="application/json")
		
	context['t1score'] = roomObj.team1score
	context['t2score'] = roomObj.team2score
	context['status'] = roomObj.status

	context['card1'] = roomObj.card1
	context['card2'] = roomObj.card2
	context['card3'] = roomObj.card3
	context['card4'] = roomObj.card4
	context['p1cards'] = roomObj.p1cards
	context['p2cards'] = roomObj.p2cards
	context['p3cards'] = roomObj.p3cards
	context['p4cards'] = roomObj.p4cards	
	context['trump'] = roomObj.trump
	context['trumpSuite'] = roomObj.trumpSuite
	startIndex = int(request.POST['message_start'])
	endIndex = roomObj.endIndex
	context['message_start'] = endIndex
	
	context['messages'] = []
	if endIndex != startIndex:
		messages = Message.objects.filter(room=roomObj).order_by('mid')

		print endIndex
		print startIndex
		if endIndex > startIndex:
			for i in range(startIndex-1, endIndex-1):
				context['messages'].append(messages[i].sender.name + ":" + messages[i].text)
		elif endIndex < startIndex:
			maxIndex = min(endIndex, MAX_MSG)
			for i in range(startIndex-1, maxIndex-1):
				context['messages'].append(messages[i].sender.name + ":" + messages[i].text)
			for i in range(0, endIndex-1):
				context['messages'].append(messages[i].sender.name + ":" + messages[i].text)
	return HttpResponse(json.dumps(context), content_type="application/json")
	
	
@csrf_exempt	
def throwCard(request):
	context = RequestContext(request)
	
	rId = request.POST['roomId']
	pId = int(request.POST['pId'])
	roomObj = Room.objects.get(roomId = rId)
	
	cardId = int(request.POST['cardId'])
	#cardObj = Card.objects.get(value=cardId)
	
	if pId == 1 and roomObj.card1 == -1:
		roomObj.card1 = cardId
		roomObj.status += 1
	elif pId == 2 and roomObj.card2 == -1:
		roomObj.card2 = cardId
		roomObj.status += 1
	elif pId == 3 and roomObj.card3 == -1:
		roomObj.card3 = cardId
		roomObj.status += 1
	elif pId == 4 and roomObj.card4 == -1:
		roomObj.card4 = cardId
		roomObj.status += 1
	else:
		return HttpResponse("Fail")	
	roomObj.save()
	#if cardObj != None:
		#cardObj.delete()
	
	if roomObj.status == 4:
		winner = checkWinner(roomObj.card1, roomObj.card2, roomObj.card3, roomObj.card4, roomObj.trumpSuite, roomObj.trump)
		print "winner is: ", winner
		if (winner == 1 or winner == 3):
			roomObj.team2score += 1
		else:
			roomObj.team1score += 1
	roomObj.save()
		
	return HttpResponse("Success")	
	

def checkWinner(c1, c2, c3, c4, tSuite, tPlayer):
	print "Trump is: ", tSuite
	suite1 = c1/13
	suite2 = c2/13
	suite3 = c3/13
	suite4 = c4/13
	print "Suites are: ", suite1, suite2, suite3, suite4
	tFlag = False
	
	if (suite1 == suite2 and suite1 == suite3 and suite1 == suite4):
		print "Same suite. Card values: ", c1, c2, c3, c4
		return argmax(c1, c2, c3, c4)
	
	if (suite1 == tSuite):
		c1 *= 100
		tFlag = True
	if (suite2 == tSuite):
		c2 *= 100
		tFlag = True
	if (suite3 == tSuite):
		c3 *= 100
		tFlag = True
	if (suite4 == tSuite):
		c4 *= 100
		tFlag = True	
			
	if tFlag == True:
		print "Trump present."
		print "Card values: ", c1, c2, c3, c4
		return argmax(c1, c2, c3, c4)
	
	maxSuite = 1
	if tPlayer == 1:
		maxSuite = suite1
	elif tPlayer == 2:
		maxSuite = suite2
	elif tPlayer == 3:
		maxSuite = suite3
	elif tPlayer == 4:
		maxSuite = suite4

	if suite2 == maxSuite:
		c1 *= 100
	if suite2 == maxSuite:
		c2 *= 100
	if suite3 == maxSuite:
		c3 *= 100
	if suite4 == maxSuite:
		c4 *= 100
	print "No trump"
	print "Card values: ", c1, c2, c3, c4
	return argmax(c1, c2, c3, c4)


@csrf_exempt	
def newMessage(request):
	context = RequestContext(request)
	
	rId = request.POST['roomId']
	pId = int(request.POST['pId'])
	roomObj = Room.objects.get(roomId = rId)
	endIndex = int(roomObj.endIndex)
	
	sender = None
	msg = Message()
	msg.mid = (endIndex+1) % MAX_MSG	
	if pId == 1:
		sender = roomObj.player1
	elif pId == 2:
		sender = roomObj.player2
	elif pId == 3:
		sender = roomObj.player3
	elif pId == 4:
		sender = roomObj.player4

	msg.sender = sender
	msg.room = roomObj
	msg.text = request.POST['msg_text']
	msg.save()
	roomObj.endIndex = roomObj.endIndex+1
	roomObj.save()
	
	return HttpResponse("Success in sending message.")
