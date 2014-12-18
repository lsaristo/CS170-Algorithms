#!/usr/bin/python
"""
File:   main.py
Brief:  Implementation of greedy reconstruction of DNA subsequences. Part of 
        a homework project for CS170 at UC Berkeley.

Author: John Wilkey
"""
import os
import itertools
import re
import timeit
import time

INPUT_DATA = '../in-data'
OUTPUT_DATA = '../out-data'
VERIFY_DATA = '../ref-data'
f_regex = re.compile('\d+')

def enum_dir(dir):
    """ Get the list of reads per file as a dictionary """
    sequences = {}
    for path, dir, files in os.walk(dir):
        for file in files:
            if 'swp' in file: continue
            sequences[file] = []
            with open(path+'/'+file) as f:
                for i,line in enumerate(f.readlines()):
                    sequences[file].append(line.strip('\n'))
    return sequences

def get_reads():
    """Return samples from input directory"""
    return enum_dir(INPUT_DATA)

def reassemble(arr):
    """ Construct DNS sequence from arr of reads """
    temp_arr = []
    
    # Remove duplicate reads from the list. 
    for elem in arr:
        if not elem in temp_arr:
            temp_arr.append(elem)
    DEBUG = False

    if DEBUG: print("Starting with array " + temp_arr)
    str_so_far = max(temp_arr, key=len)
    temp_arr.remove(str_so_far);
    if DEBUG: print("Starting with string " + str_so_far)
    if DEBUG: print("After removing this string our array looks like this " \
        + str(temp_arr))

    while temp_arr:
        max_overlap = -1;
        current_winner = None
        elem_of_winner = None
        for elem in temp_arr:
            candidate = \
                max((merge_reads(str_so_far, elem),\
                merge_reads(elem, str_so_far)),\
                key = lambda x: x[1])
            if candidate[1] > max_overlap:
                max_overlap = candidate[1]
                current_winner = candidate[0]
                elem_of_winner = elem
        str_so_far = current_winner
        temp_arr.remove(elem_of_winner)
    return str_so_far

def merge_reads(read1, read2):
    """ Merge two reads together """
    
    if read1 in read2:
        return (read2, len(read1))
    if read2 in read1:
        return (read1, len(read2))
    
    max_string = 0;
    index = 0;
    last_found = 0;
    left = read1[len(read1)-1:]
    right = read2[:1]
    
    while left and right and index < min(len(read1), len(read2)):
        if left == right:
            last_found = index+1;
        index += 1
        left = read1[len(read1)-1-index:]
        right = read2[:index+1]
    return (read1 + read2[last_found:], last_found)

def verify(my):
    """Check result against known good solution"""

    print("Verifying\t" + str(my))
    fail = 0;
    ref_files = enum_dir(VERIFY_DATA)
    my_files = enum_dir(OUTPUT_DATA)
    test_file = 'answer' + re.findall(f_regex, my)[0] + '.txt'
    my_file = 'output' + re.findall(f_regex, my)[0] + '.txt'

    if not test_file in ref_files:
        print("No reference file for " + my + ". Skipping verification")
        return -1
    if not my_file:
        print("WARNING: No output file found for " + my);
        return -1

    if not ref_files[test_file] == my_files[my_file]:
        fail += 1
        print("Mismatch at file: " + my_file + " " \
        + str(len(my[my_file][0])) + " : " + ref_file \
        + " " + str(len(ref[ref_file][0])))
        print("Offending files: (only first 40 characters shown)")
        print(my_file + ": " + str(my[my_file][0][:41]))
        print(ref_file + ": " + str(ref[ref_file][0][:41]))
    return 0 if fail else 1

def _main():
    """ Run the algorithm and write to answer files """
    dict = get_reads();
    sorted = list(dict.keys())
    sorted.sort(reverse=True);
    for seq in sorted:
        print("Trying file\t" + str(seq))
        if not dict[seq]: continue
        dna = reassemble(dict[seq])
        dna = dna + '\x0a'
        out_file = 'output' + re.findall(f_regex, seq)[0] + '.txt'
        f = open(OUTPUT_DATA+'/'+out_file, 'w')
        f.write(dna)
        f.close()
        verif_res = verify(out_file);

        if verif_res == 1:
            print("Result:\t\tSUCCESS")
        elif verif_res == 0:
            print("Result:\t\t****FAILED")
        elif verif_res == -1:
            print("Verification aborted")

        print('--------------------------------------------------')

# Program entry point
_main()
