import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import argparse


### this is a function to reverse compliment a DNA/RNA sequence if needed....

def reverse_compliment(seq):
    return str(Seq(seq).reverse_compliment())

def main(args):
    ### Load the table data made here. Assume that it is in a tab-separated format....
    df = pd.read_csv(args.table_path, sep='\t')

    ## Load the contig fastA file here....
    contigs = SeqIO.to_dict(SeqIO.parse(args.contigs_path, "fasta"))

    ## Process each riw and extract sequences....

    extracted_sequences = []
    for index,row in df.iterrows():
        contig_id = row['Contig id']
        start = row['Start']
        stop = row['Stop']
        strand = row['Strand']
        accession = row['Accession of closest sequence']
        if contig_id in contigs:
            sequence = contigs[contig_id].seq[start:stop]
            if strand == '-':
                sequence = reverse_compliment(sequence)

            ## Create a new SeqRecord here...
            new_record = SeqRecord(
                Seq(sequence),
                id=accession,
                description=""
            )
            extracted_sequences.append(new_record)

    ## Write the extracted sequences to a new FASTA file....
    SeqIO.write(extracted_sequencesm args.output_path, "fasta")

    print(f"Extracted sequences have been saved to {args.output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extra specific sequences from a FASTA file based on a TSV file.")
    parser.add_argument("--table_path", required=True, help="Path to the tab-separated values (TSV) table file.")
    parser.add_argument("--contigs_path", required=True, help="Path to the contig FASTA FIle")
    parser.add_argument("--output_path", required=True, help="Path to output extracted sequences in FASTA foramt")
    args=parser.parse_args()
    main(args)


    


