
# grain-trade-environment-China

This repository contains code used for data processing, statistical analysis, and figure generation for the manuscript:

“Climate change and interprovincial trade move grain production and environmental burdens northward in China”

## Repository structure
- `scripts/`: main scripts for figure generation and analysis
- `data_processed/`: processed data used in the main analyses, where permitted
- `docs/`: additional notes describing variables and workflow

## Data
The raw data used in this study were obtained from public sources described in the manuscript and Supplementary Information. Raw source data are therefore not fully redistributed here unless permitted. Processed data necessary to reproduce the main results are provided where permitted and where possible.

## Code use
The scripts are organized according to the main workflow, including data cleaning, model analysis, and figure production. The `scripts/` folder currently contains the main scripts used to generate Figures 2–5 in the manuscript.

## Usage notes
Some scripts currently contain local absolute paths (for example, `E:\...`) for input and output files. These paths reflect the original local working environment and should be modified by users before running the scripts on another computer.

Users may need to update:
- input data paths
- shapefile paths
- output directories

Please adjust these paths according to your local file structure before execution.

## Requirements
The code was developed using Python. Required packages may include:
- `pandas`
- `numpy`
- `matplotlib`
- `geopandas`
- `scipy`

Some scripts may also require additional local data files before execution.

## Contact
For questions regarding the code and materials, please contact the corresponding author.
