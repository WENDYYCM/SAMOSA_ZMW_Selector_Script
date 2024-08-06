import os
import sys
import subprocess
import pysam
from collections import Counter
from intervaltree import Interval, IntervalTree

def generate_index(bamfile):
    """Generate BAM index if it is older than the BAM file."""
    bam_index1 = bamfile.replace(".bam", ".bai")
    bam_index2 = bamfile + ".bai"
    bam_index = bam_index1 if os.path.exists(bam_index1) else bam_index2

    if os.path.exists(bamfile):
        bam_mtime = os.path.getmtime(bamfile)
        if os.path.exists(bam_index):
            index_mtime = os.path.getmtime(bam_index)
            if index_mtime < bam_mtime:
                subprocess.run(["samtools", "index", bamfile])
        else:
            subprocess.run(["samtools", "index", bamfile])

def readIterator(filename, chrom, start, end):
    generate_index(filename)

    bam_index1 = filename.replace(".bam", ".bai")
    bam_index2 = filename + ".bai"
    if os.path.exists(filename) and (os.path.exists(bam_index1) or os.path.exists(bam_index2)):
        input_file = pysam.AlignmentFile(filename, "rb")
        for read in input_file.fetch(chrom, start, end):
            yield read
        input_file.close()

def calculatePerBase(filename, tss, valid_chroms, window):
    zmws = []
    for line in tss:
        split = line.split()
        if len(split) > 3:
            label = split[3]
        chrom = split[0]
        if chrom not in valid_chroms:
            continue
        t_start, strand = int(split[1]), split[2]
        start = t_start - window
        if start <= 0:
            continue
        end = t_start + window
        for read in readIterator(filename, chrom, start, end):
            if read.is_reverse:
                rstrand = '-'
            else:
                rstrand = '+'
            rname = read.qname
            rstart = read.reference_start
            rend = read.reference_end
            zmw = rname.split('/')[1]
            if len(split) > 3:
                zmws.append(f"{zmw}\t{chrom}\t{rstart}\t{rend}\t{t_start}\t{label}\t{rstrand}\t{strand}")
            else:
                zmws.append(f"{zmw}\t{chrom}\t{rstart}\t{rend}\t{t_start}\t{rstrand}\t{strand}")
    return zmws

def main():
    if len(sys.argv) != 5:
        sys.exit(1)
    
    tfile_path = sys.argv[1]
    chromsizes_path = sys.argv[2]
    bam_file = sys.argv[3]
    window_size = int(sys.argv[4])
    
    if not os.path.exists(tfile_path):
        sys.exit(1)

    if not os.path.exists(bam_file):
        sys.exit(1)    

    if not os.path.exists(chromsizes_path):
        sys.exit(1)

    with open(tfile_path) as tfile, open(chromsizes_path) as valid_chroms_file:
        valid = {line.split()[0]: True for line in valid_chroms_file}
        tss = tfile.readlines()
    
    zmws = calculatePerBase(bam_file, tss, valid, window_size)
    
    for zmw in zmws:
        print(zmw)

if __name__ == "__main__":
    main()

