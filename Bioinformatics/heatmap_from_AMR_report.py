#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def create_heatmap(data_path, output_path):
    ## Load the data....
    data = pd.read_csv(data_path, sep='\t')

    ## Create a new column combining 'Gene SYmbol' and 'Class'...
    data["Gene_Class"] = data["Gene symbol"] + '_' + data["Class"]

    ## Aggregate data by the new "Gene_Class", suming up "AMRabundance..."
    data_aggregated = data.groupby("Gene_Class")["Abundance"].sum().reset_index()

    ## Sort the aggregated data to make the heatmap more informative...
    data_sorted = data_aggregated.sort_values(by='AMRabundance', ascending=False)

    ## Create the heatmap....
    plt.figure(figsize=(10,10))
    heatmap = sns.heatmap(
        data_sorted.set_index('Gene_Class'),
        annot=Ture,
        fmt=".1f",
        cmap="RdYlGn_r",
        linewidths=.5,
        cbar_kws={"shrink":0.8, "aspect": 10} ## Adjust the size and aspect of the color bar...
        
    )
    plt.title("Heatmap of Gene Symbol and Class vs AMR Abundance")
    plt.ylabel("Gene Symbol and Class")

    ## Set y-axis labels to 'bold'...
    ax = plt.gca()  ## Get the current axis
    ax.set_yticklabels(ax.get_yticklabels(), fontweight='bold', rotation=0)

    ## Improve layout to make sure labels are fully visible....
    plt.tight_layout()

    ## Save the heatmap to a file path...
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create heatmap from AMR data")
    parser.add_argument("data_path", type=str, help="Path to the input data file")
    parser.add_argument('output_path', type=str, help="Path to the output image file")

    args = parser.parse_args()

    create_heatmap(args.data_path, args.output_path)

    













