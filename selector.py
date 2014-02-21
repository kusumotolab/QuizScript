#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
import random


class Selector:
	def __init__(self):
		self.prob = -1
		self.money_list = []	

	def __total_money(self, prob):
		mod = (prob % 100) + 1
		return (mod * setting.RATE)

	def __new_prob_num(self):
		return random.randint(1, setting.MAX_PROBLEM_NUM)

	def __rate_list(self):
		half = setting.MEMBER / 2
		rl = [ 2.0**x for x in range(0,half) ]
		p_sum = sum(rl)
		rl = map( (lambda x: x / p_sum), rl)
		
		pos_list = rl[::-1]
		neg_list = map( (lambda x: x * -1), rl )
		if(setting.MEMBER%2 == 1):
			pos_list.append(0)

		return pos_list + neg_list

	def shuffle(self):
		self.prob = self.__new_prob_num()
		self.money_list = map( (lambda x: x * self.__total_money(self.prob)), self.__rate_list() )
		self.money_list = map( (lambda x: int(x)), self.money_list )