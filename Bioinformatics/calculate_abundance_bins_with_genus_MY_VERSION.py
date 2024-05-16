#! /usr/bin/env python3

import pandas as pd
import sys 
from openpyxl.styles import Alignment, Font

def extract_genus_species(taxonomic_string):
    parts = taxonomic_string.split(';')
    genus = None
    for part in parts:
        if part.startswith('g__'):
