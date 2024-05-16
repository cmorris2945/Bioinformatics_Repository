#!/usr/bin/env python3




import pandas as pd
import argparse

def main(args):

    ## Load the AMR Finder report...
    amr_report = pd.read_csv(args.amr_report_path, sep='\t', header=0)

    ## Load the AMR Abundance file....
    amr_abundance = pd.merge(amr_report, amr_abundance, how='left', left_on='Accession of closest sequence', right_on='#Template')

    ## Merge the data baes on 'Accession of closest sequence' and '#Template' columnns...
    merged_data = pd.merge(amr_report, amr_abundance, how='left', left_on='Accession of closest sequence', right_on='#Template')

    ## Optionally drop the duplicate accession column from amr_abundance

    merged_data.drop(columns=['#Template'], inplace=True)

    ## Save the merged data back to a new file...

    merged_data.to_csv(args.output_path, sep='\t', index=False)

    print(f"Updated AMR Finder Report has been saved to {args.output_path}")


if _name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append AMR abundance data to AMR Finder Report based on accession numbers...")
    parser.add_argument("--amr_report_path", required=True, help="Path to the AMR finder report (TSC File) format")
    parser.add_argument("--amr_abundance_path", required=True, help="Path to the AMR abundance file (CSV) format")
    parser.add_argument("--output_path", required=True, help="Path for the output to save the updated AMR Finder report to (TSV file)")
    args = parser.parse_args()
    main(args)

