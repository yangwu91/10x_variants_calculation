#!/usr/bin/env python

import sys, re, os
from TransDigits import TransDigits as TD
from ggplot import *
from pandas import DataFrame

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
	return [window_point, heho_ratio, del_counts, ins_counts]

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
		type_info, heho_info='', ''
		pos_list, heho_list, del_list, ins_list=[], [], [], []
		os.system(r'rm -f %s_*' % sys.argv[1])
		outputfilename=r'%s_%s' % (sys.argv[1], TD(window, 'readable'))
		while True:
			line=inputfile.readline().strip()
			if len(line)==0:
				window_point=window*n - window/2
				row=VariantStat(del_pattern, ins_pattern, HE_pattern, HO_pattern, type_info, heho_info, outputfilename, window_point)
				pos_list.append(row[0]), heho_list.append(row[1]), del_list.append(row[2]), ins_list.append(row[3])
				break
			if line[0]<>'#':
				vcf_list=line.split('\t')
				qual=vcf_list[5]
				if qual=='.':
					qual=25
				else:
					try:
						qual=float(qual)
					except:
						continue
					else:
						if vcf_list[6]=='PASS' and  qual>= 25:
							try:
								POS=int(vcf_list[1])
							except:
								continue
							if POS <= window*n:
								type_info+=('\t' + vcf_list[7])
								heho_info+=('\t' + vcf_list[9].split(':')[0])
							else:
								window_point=window*n - window/2
								row=VariantStat(del_pattern, ins_pattern, HE_pattern, HO_pattern, type_info, heho_info, outputfilename, window_point)
								pos_list.append(row[0]), heho_list.append(row[1]), del_list.append(row[2]), ins_list.append(row[3])
								type_info=vcf_list[7]
								heho_info=vcf_list[9].split(':')[0]
								n+=1
						
	# Plotting using ggplot for Python
	plotting_data=DataFrame({'pos':pos_list, 'heho':heho_list, 'del':del_list, 'ins':ins_list})
	heho_p=ggplot(aes(x = 'pos', y = 'heho'), data= plotting_data) + geom_point() + ggtitle('heterozygous / (heterozygous + homozygous)') + scale_x_continuous('Position', breaks = [0, 1e+08, 2e+08, 3e+08], labels = ['0', '100Mb', '200Mb', '300Mb']) + xlim(low=0, high=3.7e8) + scale_y_continuous('Percent (%)', breaks = [25, 50, 75, 100]) + ylim(low=0, high=100)# + theme(axis.title.x = element_text())
	heho_p.save('heho_ratio_%s.png' % TD(window, 'readable'), dpi = 300)#, width = 8.43, height = 5.28, dpi = 300)#, limitsize = TRUE)
	del_p=ggplot(aes(x = 'pos', y = 'del'), data= plotting_data) + geom_point() + ggtitle('Deletion') + ylab('Count') + scale_x_continuous('Position', breaks = [0, 1e+08, 2e+08, 3e+08], labels = ['0', '100Mb', '200Mb', '300Mb']) + xlim(low=0, high=3.7e8) + scale_y_continuous('Count') + ylim(low = 0)
	del_p.save('del_stat_%s.png' % TD(window, 'readable'), dpi = 300)#, width = 8.43, height = 5.28, dpi = 300)#, limitsize = TRUE)
	ins_p=ggplot(aes(x = 'pos', y = 'ins'), data= plotting_data) + geom_point() + ggtitle('Insertion') + ylab('Count') + scale_x_continuous('Position', breaks = [0, 1e+08, 2e+08, 3e+08], labels = ['0', '100Mb', '200Mb', '300Mb']) + xlim(low=0, high=3.7e8) + scale_y_continuous('Count') + ylim(low = 0)
	ins_p.save('ins_stat_%s.png' % TD(window, 'readable'), dpi = 300)#, width = 8.43, height = 5.28, dpi = 300)#, limitsize = TRUE)

