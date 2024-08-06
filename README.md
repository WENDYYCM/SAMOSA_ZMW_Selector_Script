# SAMOSA_ZMW_Selector_Script
1) Enhanced zmw_selector.py: Refined the original script to improve efficiency and functionality. 
2) New run_zmw_selector.sh: Added a shell script for streamlined execution of the Python script, including environment setup and error detection.

# SAMOSA ZMW Selector

## Overview

This repository contains the refined `zmw_selector.py` script and the newly added `run_zmw_selector.sh` script for enhanced functionality and efficiency in extracting Pacific Bioscience's Zero-Mode Waveguides (ZMWs) near predicted transcription factor binding sites. The original script is credited to the [Ramani Lab's SAMOSA project](https://github.com/RamaniLab/SAMOSA).

## Features

### Enhancements in zmw_selector.py

- **Automatic BAM Indexing**: The script now checks for the existence of a BAM index file. If none exists or if the existing index is outdated, the script generates a new index file based on the BAM file's creation date.
- **Improved Error Handling**: Added comprehensive error handling to manage various edge cases and ensure robust script execution.
- **Refactored Code**: Simplified and cleaned the code for better readability and maintainability.

### New run_zmw_selector.sh Script

- **Environment Setup**: The shell script activates a Conda environment linked to a Jupyter kernel, ensuring all required packages are available.
- **Error Detection**: Implemented echo statements within the shell script to identify and report potential errors, aiding in quick troubleshooting.
- **Batch Processing**: Allows the user to pass a directory of BAM files, processing each file sequentially and outputting individual ZMW TSV files.

### Prerequisites for Shell Script Usage

- Conda installed and configured.
- Jupyter Notebook installed.
- Required Python packages listed in `zmw_selector_updated.py` import section (provided in the repository).



