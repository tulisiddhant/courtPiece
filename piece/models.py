from __future__ import unicode_literals
from django.db import models


class Player(models.Model):
	name = models.CharField(max_length=100,null=True,blank=True) 
	def __unicode__(self):
		return str(self.name)
		
		
class Room(models.Model):
	roomId = models.CharField(max_length=100, null=True, blank=True)
	player1 = models.ForeignKey(Player, null=True, blank=True, related_name='first_pos')
	player2 = models.ForeignKey(Player, null=True, blank=True, related_name='second_pos')
	player3 = models.ForeignKey(Player, null=True, blank=True, related_name='third_pos')
	player4 = models.ForeignKey(Player, null=True, blank=True, related_name='fourth_pos')
	card1 = models.IntegerField(default=-1, null=True)
	card2 = models.IntegerField(default=-1, null=True)
	card3 = models.IntegerField(default=-1, null=True)
	card4 = models.IntegerField(default=-1, null=True)
	p1cards = models.CharField(max_length=150, null=True, blank=True)
	p2cards = models.CharField(max_length=150, null=True, blank=True)
	p3cards = models.CharField(max_length=150, null=True, blank=True)
	p4cards = models.CharField(max_length=150, null=True, blank=True)
	team1score = models.IntegerField(null=True, default=0)
	team2score = models.IntegerField(null=True, default=0)
	endIndex = models.IntegerField(null=True, default=1) 
	status = models.IntegerField(null=True, default=0) 
	phase = models.IntegerField(null=True, default=0)
	trump = models.IntegerField(null=True, default=0)
	trumpSuite = models.IntegerField(null=True, default=1)
	def __unicode__(self):
		return str(self.roomId)		


class Card(models.Model):
	owner = models.ForeignKey(Player, null=True, blank=True)
	value = models.IntegerField(null=True, default=1)
	def __unicode__(self):
		return str(self.value)

class Message(models.Model):
	mid = models.IntegerField(default=0, null=True, blank=True)
	text = models.CharField(max_length=200, null=True, blank=True)
	sender = models.ForeignKey(Player, null=True,blank=True)
	room = models.ForeignKey(Room, null=True, blank=True)
	def __unicode__(self):
		return str(self.mid)	
