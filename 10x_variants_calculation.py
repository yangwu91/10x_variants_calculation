#!/usr/bin/env python

import sys, re, os
from TransDigits import TransDigits as TD

def VariantStat(del_pattern, ins_pattern, HE_pattern, HO_pattern, type_info, heho_info, output_filename, window_point):
	#window_point=window_point/10000
	del_counts=len(re.findall(del_pattern, type_info))
	with open('%s_DelStat' % output_filename, 'a') as outputfile:
		outputfile.write('%s\t%s\n' % (window_point, del_counts))
	ins_counts=len(re.findall(ins_pattern, type_info))
	with open('%s_InsStat' % output_filename, 'a') as outputfile:
		outputfile.write('%s\t%s\n' % (window_point, ins_counts))
	he_counts=len(re.findall(HE_pattern, heho_info))
	ho_counts=len(re.findall(HO_pattern, heho_info))
	if he_counts<>0 or ho_counts<>0:
		heho_ratio=he_counts*100.0/(he_counts+ho_counts)
	else:
		heho_ratio='NA'
	with open('%s_HeHoRatio' % output_filename, 'a') as outputfile:
		outputfile.write('%s\t%s\n' % (window_point, heho_ratio))

if __name__ == '__main__':
	n=1
	try:
		vcf_file=sys.argv[1]
	except IndexError:
		print 'Please sepcify your input file!'
		quit()
	try:
		window=TD(sys.argv[2], 'number')
	except IndexError:
		window=1000000
	ins_pattern=re.compile(r';TYPE=ins;')
	del_pattern=re.compile(r';TYPE=del;')
	HE_pattern=re.compile(r'(1\|0)|(0\|1)')
	HO_pattern=re.compile(r'1\|1')
	with open(vcf_file, 'r') as inputfile:
		type_info=''
		heho_info=''
		os.system(r'rm -f %s_*' % sys.argv[1])
		outputfilename=r'%s_%s' % (sys.argv[1], TD(window, 'readable'))
		while True:
			line=inputfile.readline().strip()
			if len(line)==0:
				window_point=window*n - window/2
				VariantStat(del_pattern, ins_pattern, HE_pattern, HO_pattern, type_info, heho_info, outputfilename, window_point)
				break
			if line[0]<>'#':
				vcf_list=line.split('\t')
				if vcf_list[6]=='PASS' and float(vcf_list[5]) > 25:
					try:
						POS=int(vcf_list[1])
					except:
						continue
					if POS <= window*n:
						type_info+=('\t' + vcf_list[7])
						heho_info+=('\t' + vcf_list[9].split(':')[0])
					else:
						window_point=window*n - window/2
						VariantStat(del_pattern, ins_pattern, HE_pattern, HO_pattern, type_info, heho_info, outputfilename, window_point)
						type_info=vcf_list[7]
						heho_info=vcf_list[9].split(':')[0]
						n+=1
