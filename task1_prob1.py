import os
from Bio import SeqIO

# Recursively find all files with the extension .fastq
def findAllFastqFiles(directory, extension):
    filenames = []
    for path, dirnames, files in os.walk(directory):
        for f in files:
            if f.endswith(extension):
                filename = os.path.join(path, f)
                filenames.append(filename)
    return filenames

#Iterate through the files and find the percent of sequences in the file that are 30 nucleotides long
def fastaSeq(filenames):
    res = []
    for filename in filenames:
        number_of_large_sequences = 0
        number_of_sequences = 0
        for sequence in SeqIO.parse(open(filename, "r"), "fastq"):
            number_of_sequences += 1
            if len(sequence.seq) > 30:
                number_of_large_sequences += 1
        percentage = number_of_large_sequences / number_of_sequences
        format_percentage = "Percentage: " + "{:.2%}".format(percentage)
        res.append((filename, format_percentage))
    return res

if __name__ == "__main__":
    directory = "./sample_files/fastq"
    extension = ".fastq"
    filenames = findAllFastqFiles(directory, extension)

    fastaSeq(filenames)
    print('All the fastq files:', filenames)

    print('File names and the percent of sequences in that file that are greater than 30 nucleotides long:', fastaSeq(filenames))




            
                



