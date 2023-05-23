from Bio import SeqIO

def frequentSeqs(file):
    fasta_sequences = SeqIO.parse(open(file),'fasta')
    dict = {}
    # use dictionary to count the frenquency of each sequence in the fasta file
    for fasta in fasta_sequences:
        seq = str(fasta.seq)
        if seq in dict:
            dict[seq] += 1
        else:
            dict[seq] = 1
    
    # sort the items in the dictionary and convert to an array based on the frequency
    sorted_list = sorted(dict.items(), key = lambda x: x[1], reverse = True)
    
    # get the 10 most frequent sequences along with their frenquency
    result = sorted_list[0:10]

    return result

if __name__ == "__main__":
    file = "./sample_files/fasta/sample.fasta"
    print(frequentSeqs(file))



       


