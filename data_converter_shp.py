import geopandas as gpd
import os
import pandas as pd
from dbfread import DBF
def shapefile_to_csv(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # List all shapefiles in the input folder
    shapefiles = [f for f in os.listdir(input_folder) if f.endswith('.shp')]
    
    # Convert each shapefile to CSV
    for shapefile in shapefiles:
        # Read shapefile
        gdf = gpd.read_file(os.path.join(input_folder, shapefile))
        
        # Define output CSV file path
        csv_file = os.path.join(output_folder, os.path.splitext(shapefile)[0] + '.csv')
        
        # Write to CSV
        gdf.to_csv(csv_file, index=False)

# Input folder containing shapefiles
input_folder = 'All_POIs'

# Output folder for CSV files
output_folder = 'data_folder'

# Convert shapefiles to CSV
# shapefile_to_csv(input_folder, output_folder)


def prj_files_to_csv(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # List all .prj files in the input folder
    prj_files = [f for f in os.listdir(input_folder) if f.endswith('.prj')]
    
    # Convert each .prj file to CSV
    for prj_file in prj_files:
        # Read the .prj file
        with open(os.path.join(input_folder, prj_file), 'r') as file:
            prj_data = file.read()
        
        # Define output CSV file path
        csv_file = os.path.join(output_folder, os.path.splitext(prj_file)[0] + '.csv')
        
        # Write the data to a CSV file
        with open(csv_file, 'w') as file:
            file.write("Coordinate Reference System\n")
            file.write(prj_data)
# Input folder containing shapefiles
input_folder = 'All_POIs'

# Output folder for CSV files
output_folder = 'data_folder_prj'

# prj_files_to_csv(input_folder, output_folder)

def dbf_to_csv(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # List all DBF files in the input folder
    dbf_files = [f for f in os.listdir(input_folder) if f.endswith('.dbf')]
    
    # Convert each DBF file to CSV
    for dbf_file in dbf_files:
        # Read the DBF file using dbfread
        dbf_data = DBF(os.path.join(input_folder, dbf_file))
        
        # Convert to DataFrame
        df = pd.DataFrame(iter(dbf_data))
        
        # Define output CSV file path
        csv_file = os.path.join(output_folder, os.path.splitext(dbf_file)[0] + '.csv')
        
        # Write the data to a CSV file
        df.to_csv(csv_file, index=False)
# Input folder containing DBF files
input_folder = 'All_POIs'

# Output folder for CSV files
output_folder = 'data_folder_dbf'

# Convert DBF files to CSV
dbf_to_csv(input_folder, output_folder)