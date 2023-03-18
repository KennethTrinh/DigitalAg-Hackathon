import csv
import pandas as pd
import numpy as np 
from regression import microbiome_impact

# Define the CSV file path, header row index and header name
header_row_index = 4
csv_file_path = "methane_diff.csv"
means_header = "Mean relative abundance (%)"
stds_header = "STD"

df = pd.read_csv('methane_diff.csv', skiprows=4)
mean_values =  df.iloc[:, 5].to_numpy().astype(float)
std_values = df.iloc[:,6].to_numpy().astype(float)



# Define the means and standard deviations
means_a = np.array(mean_values[:4])
means_b = np.array(mean_values[4:])
stds_a = np.array(std_values[:4])
stds_b = np.array(std_values[4:])

def gen_data(category_means, category_stds):
  # Define the number of features
  n_features = len(category_means)

  data_points = np.zeros(n_features)
  
  while True:
    data = np.random.normal(category_means, category_stds)
    if all(data >= 0) and abs(sum(data) - 100) <= 1:
        break
  # Adjust the data points so they sum up to 100
  data = data / sum(data) * 100
  data = [round(d, 2) for d in data]

  return data
          

with open("output.csv", "w", newline="") as csv_file:
  for x in range(200):
    a = gen_data(means_a, stds_a)
    b = gen_data(means_b, stds_b)
    total_methane = 400 + microbiome_impact(a, b)
    row = a + b + [total_methane]
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(row)
  
