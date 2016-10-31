#!/usr/bin/env python
# encoding: utf-8
import re
def TransDigits(num, *fmt):
	try:
		num=int(num)
	except ValueError:
		num=str(num)+'b'
		t=re.findall(r'([0-9]+)[tT]', num)
		g=re.findall(r'([0-9]+)[gG]', num)
		m=re.findall(r'([0-9]+)[mM]', num)
		k=re.findall(r'([0-9]+)[kK]', num)
		b=re.findall(r'([0-9]+)b', num)
		if t==[]:
			t=[0]
		if g==[]:
			g=[0]
		if m==[]:
			m=[0]
		if k==[]:
			k=[0]
		if b==[]:
			b=[0]
		#print b[0], k[0], m[0], g[0], t[0]
		number=int(b[0]) + 1000*int(k[0]) + 1000000*int(m[0]) + 1000000000*int(g[0]) + 1000000000000*int(t[0])
		if fmt==('readable',):
			return TransDigits(number)
		else:
			return number
	else:
		if fmt==('number',):
			return num
		else:
			num_list="{:,}".format(int(str(num))).split(',',4)
			num_list.reverse()
			n=0
			converted_num_list=[]
			for digit in num_list:
				if digit<>'000':
					if n==0:
						converted_num_list.append(str(int(digit)))
					elif n==1:
						converted_num_list.append(str(int(digit))+'K')
					elif n==2:
						converted_num_list.append(str(int(digit))+'M')
					elif n==3:
						converted_num_list.append(str(int(digit))+'G')
					elif n==4:
						converted_num_list.append(str(int(digit))+'T')				
				n+=1
			converted_num_list.reverse()
			return(''.join(converted_num_list))