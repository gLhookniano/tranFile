#/usr/bin/env python
#coding: utf-8

import os
import re
#import subprocess

def update_file(old_file, new_file):
'''
update new_file base on old_file
'''
    add_count = 0
    sub_count = 0
    fp_o = open(old_file, 'r')
    fp_n = open(new_file, 'r')
    str_n = fp_n.read()
    fp_n.close()
    fp_n = open(new_file, 'w')
    try:
        for i in fp_o.readlines():
            if re.search(r'"(.*)"\t"(.*)"\t"(.*)"\n', i) == None:#search through the string
                continue
            sign = re.sub(r'"(.*)"\t"(.*)"\t"(.*)"\n', lambda _ :'"'+_.group(1)+'"\t"(.*)"\t"(.*)"\n', i)
            if re.search(sign, str_n) == None:
                str_n = i + str_n
                add_count = add_count + 1
                continue
            str_n = re.sub(sign, i, str_n)
            sub_count = sub_count + 1
        if add_count !=0 or sub_count !=0:
            print "add_count: {} sub_count: {} update file : {}\n".format(add_count,sub_count, new_file)
        fp_n.write(str_n)
        fp_o.close()
        fp_n.close()
    except Exception, e:
        print sign,'\t',e

def update_lf(list_file, old_path, new_path):
'''
update file form old_path to new_path which in list_file
'''
    if old_path[-1] != '\\':
        old_path = old_path + '\\'
    if new_path[-1] != '\\':
        new_path = new_path + '\\'
    
    for i in list_file:
        update_file(old_path+i, new_path+i)

def correct_file(file, correct_dict):
'''
correct file use correct_dict
'''
    fp_r = open(file, 'r')
    str_f = fp_r.read().strip()
    fp_w = open(file, 'w')

    for i in correct_dict.keys():
        str_f = re.sub(i, correct_dict[i], str_f)
    fp_w.write(str_f)
    
    fp_w.close()
    fp_r.close()

def correct_lf(list_file, path, correct_dict):
'''
correct file in list_file
'''
    if path[-1] != '\\':
        path = path + '\\'
    for i in list_file:
        correct_file(path+i, correct_dict)

def move_file(src_path, dst_path, list_file):
'''
copy file form src_path to dst_path which in list_file
'''
    if src_path[-1] != '\\':
        src_path = src_path + '\\'
    if dst_path[-1] != '\\':
        dst_path = dst_path + '\\'
    
    fp = open(list_file, 'r')
    for x in fp.readlines():
        fp_s = open(src_path+x[:-1], 'rb')
        fp_d = open(dst_path+x[:-1], 'wb')
        fp_d.write(fp_s.read())
        fp_s.close()
        fp_d.close()
    fp.close()


def filter(l1, l2, fp, check_path):
'''
filter two dir file, and write to fp; 
return 1:done, 0:no_done
'''
    if len(l1) == 0: return 1
    if len(l2) == 0: return 1
    for i in l1:
        for j in l2:
            if i==j:
                l1.remove(i)
                l2.remove(j)
                return 0
        l1.remove(i)
        if check_empty(i, check_path) == 1:
            return 0
        fp.write(i+'\n')
        return 0


def check_empty(file, check_path):
'''
check files in path whether empty
'''
    if check_path[-1] != '\\':
        check_path = check_path + '\\'
    fp = open(check_path + file, 'r')
    if fp.readline()=='':
        fp.close()
        return 1
    fp.close()
    return 0


if __name__ == "__main__":
    dir_refer = r"H:\WHM_en\text\db"
    dir_dst = r"H:\WHM_zh\text\db"
    dir_trans = r"H:\WHM_trans"
    file_difference = r"./test.txt"

    
    ldir1=os.listdir(dir_refer)
    ldir2=os.listdir(dir_trans)
    fp = open(file_difference, 'w')

    flag = 1
    while flag:
        flag = filter(ldir1, ldir2, fp, dir_refer)

    fp.close()
    move_file(dir_refer, dir_trans, file_difference)
