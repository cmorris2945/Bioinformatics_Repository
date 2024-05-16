#!/usr/bin/env python3

import pandas as pd
import argparse

def extract_fragment_counts_and_total(file_path):
    """Extracts individual fragment counts from the .mapstat file and the total fragment count from metadata"""
    total_fragment_count = None
    individual_fragment_counts = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('## fragmentCount'):
                total_fragment_count = int(line.strip().split('\t')[1])
            elif not line.startswith('#') and line.strip():
                ##Extract individual fragment countrs from the data section...
                fields = line.strip().split('\t')
                if len(fields) > 2:    ## Ensure there is enough fields...
                    individual_fragment_counts.append(int(fields[2])) ## The third field is fragmentcount feature
    if total_fragment_count is None:
        raise ValueError("Total fragmentCount value not found in the metadata...")
    return individual_fragment_counts, total_fragment_count

def calculate_amr_abundance(n,N,l):
    """calculates AMR abundance based on the provided formula..."""
    return (n / (N * l)) * 1000000 * 1000

def merge_files(mapstat_file_path, res_file_path, output_file_path):
    """Merges .mapstat and .res files into a combined CSV file with individual and 
    total fragmentCounts and calculates AMR abundance"""
    individual_fragment_counts, total_fragment_count = extract_fragment_counts_and_total(mapstat_file_path)

    ## load the .res file....
    res_df = pd.read_csv(res_file_path, sep='\t', usecols=['#Template', 'Template_length'])

    if len(individual_fragment_counts) == len(res_df):
        res_df["FragmentCount"] = individual_fragment_counts  ## individual fragment count
        res_df["TotalFragmentCount"] = total_fragment_count  # total fragment count for all rows
        ##Calculate AMR abundance for each row...
        res_df['AMRabundance'] = res_df.apply(lambda row: calculate_amr_abundance(row['FragmentCount'],
    row['Template_length']), axis=1)
    else:
        raise ValueError("Mismatch in the number of rows between .mapstat /n"
                        " data and .res file entries")
    
    ## Save the combined DataFrame to a new CSV file....
    res_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge ,mapstat data and .res files with individual and total fragment counts and calculate \n"
        "AMR abundance")
    parser.add_argument("mapstat_file", help="The path to the .mapstat file")
    parser.add_argument("res_file", help="The path to the .res file")
    parser.add_argument("output_file", help= "The path where the output csv file will be saved")

    args = parser.parse_args()

    merge_files(args.mapstat_file, args.res_file, args.output_file)
    print(f"Combined data saved to {args.output_file}")



    











