import csv
import sys
from collections import defaultdict

'''
    Function for extracting the data from the file coordinates_to_annotate.txt
    and putting the data in a dictionary for better performance
    with Chromosomea as the keys and an array of the corresponding coordintates as the values
    e.g. {'chr12': ['20704380', '20704379', '20704371',...]}
'''
def parseChromosome(filename):
    dict = defaultdict(list)
    with open(filename, 'r') as f:
        file = csv.reader(f, delimiter='\t')
        for row in file:
            chromo = row[0]
            coordinate = row[1]
            if coordinate not in dict[chromo]:
                dict[chromo].append(coordinate)
    # print(dict)
    return dict

'''
    Function for extracting the coordinate intervals (coordinate_start, coordinate_end) and gene names
    corresponding to the input chromosome from the file hg19_annotations.gtf
    and putting the data in a dictionary for better performance
    with (coordinate_start, coordinate_end) as the keys and an array of the corresponding coordintates as the values
    e.g. {(129001538, 129082406): 'PVT1'}
'''

def parseGTF(filename, chromo):
    dict = defaultdict(str)
    with open(filename, 'r') as f:
        file = csv.reader(f, delimiter='\t')
        for row in file:
            if row[0] == chromo:
                attributes = row[8].strip().split(';')
                gene_name = None
                for attribute in attributes:
                    if attribute.strip().startswith('gene_name'):
                        gene_name = attribute.split('"')[1].strip()
                if gene_name:
                    coordinate_start = int(row[3])
                    coordinate_end = int(row[4])
                    dict[(coordinate_start, coordinate_end)] = gene_name
    # print(dict)
    return dict

def main(chromo):
    filename_chromo = "./sample_files/annotate/coordinates_to_annotate.txt"
    filename_gtf = "./sample_files/gtf/hg19_annotations.gtf"

    #create the choromosome dict using parseChromosome
    chromosome_dict = parseChromosome(filename_chromo)

    # output = []

    # create gtf dict for the chromosome using chromosome_dict
    gtf_dict = parseGTF(filename_gtf, chromo)

    # look up and get the coordinates for the input chromosome from the chromosome_dict dictionary
    coordinates = chromosome_dict[chromo]
    
    # create the output file
    result = open('output.txt', 'w')
    # iterate over the coordinates and find the gene name that input position overlaps
    # and output to a file output.txt
    for position in coordinates:
        gene_name = ''
        for (start, end), name in gtf_dict.items():
            if start <= int(position) <= end:
                gene_name = name
        if gene_name:
            data = f" {chromo} {position}\t{gene_name}" + '\n'
            result.write(data)
            # output.append(f"Chromosome {chromo} Position {position}: Gene Name {gene_name}")
    result.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        chromo = sys.argv[1]
        main(chromo)
    elif len(sys.argv) > 2:
        print('Too many arguments')
    elif len(sys.argv) == 1:
        print('Please parse a chromosome as an argument')
    








    