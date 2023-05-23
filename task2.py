import pandas as pd
import numpy as np

try:
    # read the file using pd.read_csv() and skip lines that may cause parsing error
    file_path = './sample_files/Example.hs_intervals.txt'
    df = pd.read_csv(file_path, sep='\t', usecols = ['%gc','mean_coverage'], on_bad_lines= 'skip')
    
    # define the %gc bins
    bins = np.arange(0, 101, 10)

    # multiplies the %gc values by 100 to convert to percentages
    df['%gc'] = df['%gc'] * 100

    # group intervals into %gc bins and calculate the mean target coverage for each bin by adding a new column 'gc_bin' using pd.cut
    df['gc_bin'] = pd.cut(df['%gc'], bins)
    mean_coverage_by_bin = df.groupby('gc_bin')['mean_coverage'].mean()

    # Print the results
    for gc_bin, mean_coverage in mean_coverage_by_bin.items():
        print(f"GC% bin: {gc_bin}\tMean Target Coverage: {mean_coverage:.2f}")

except pd.errors.ParserError as e:
    print(f"Error {e} while reading the file. Please check the file.")

