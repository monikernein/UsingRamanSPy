# Load ramanspy
import ramanspy as rp
import os  # Import os for handling file names
import matplotlib.pyplot as plt
import pandas as pd  # Import Pandas for CSV export
import numpy as np

import glob


# Load data
folder_path = r"C:\Users\Taladriz\OneDrive - Université de Fribourg\SERS TAG PROJECT\Liquid Data\AuStars\Raman\100 nm PS_0.1mMStars_2NAT_785nm\Dataset_11_Liquid_MHAuStars9_mPEG3_2NAT1_0p1mM_PS100nm_NIR785_GlasSlide\Python"
file_paths = glob.glob(f"{folder_path}/*.mat")
data_list = [rp.load.witec(file) for file in file_paths]

# Function to load and process spectra
def process_spectra(file_paths):
    processed_spectra = []
    file_names = []  # Ensure file_names is initialized

    # Define the cropping region (e.g., from wavenumber 800 to 1800)
    crop_region = (800, 1800)

    # Creating the pipeline with multiple processing steps (cropping)
    pipeline = rp.preprocessing.Pipeline([rp.preprocessing.misc.Cropper(region=crop_region), rp.preprocessing.baseline.ASPLS()])

    for file_path in file_paths:
        # Extract file name without extension for labeling
        file_name = os.path.basename(file_path).replace(".mat", "")
        file_names.append(file_name)

        # Load spectrum
        spectrum = rp.load.witec(file_path)

        # Apply the preprocessing pipeline
        corrected_spectrum = pipeline.apply(spectrum)

        # Store the processed spectrum
        processed_spectra.append((spectrum, corrected_spectrum))

    return processed_spectra, file_names  # Ensure correct indentation

# Process all spectra
corrected_spectra, file_names = process_spectra(file_paths)

# Extract only the corrected spectra for plotting
corrected_spectra = [corr for _, corr in corrected_spectra]

# Generate labels using file names
labels = [f"{name}_processed" for name in file_names]

# Plot stacked processed spectra with proper labels
ax = rp.plot.spectra(corrected_spectra, 
                      label=labels,
                      title="Baseline and Cropping Processing",
                      plot_type="single stacked")

# Display plot
rp.plot.show()

def save_spectra_to_csv(spectra, file_names, output_dir):
    """
    Save processed spectra to CSV files.

    Parameters:
    - spectra: List of processed Spectrum objects.
    - file_names: List of original file names corresponding to each spectrum.
    - output_dir: Directory where CSV files will be saved.
    """
    for spectrum, name in zip(spectra, file_names):
        # Create a DataFrame from the spectrum data
        df = pd.DataFrame({
            'Wavenumber': spectrum.spectral_axis,
            'Intensity': spectrum.spectral_data
        })
        # Define the output file path
        output_file = os.path.join(output_dir, f"{name}_processed.csv")
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")

# Define the directory where you want to save the CSV files
output_directory = r"C:\Users\Taladriz\Desktop\Data"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Save the processed spectra to CSV
save_spectra_to_csv(corrected_spectra, file_names, output_directory)

# Function to extract maximum intensities in two wavenumber ranges
def extract_max_intensities_in_ranges(spectra, file_names, range1, range2, output_file):
    """
    Extracts maximum intensity values within two specified wavenumber ranges 
    from multiple spectra and exports to CSV.

    Parameters:
    - spectra: List of processed Spectrum objects.
    - file_names: List of original file names corresponding to each spectrum.
    - range1: Tuple specifying the first wavenumber range (min, max).
    - range2: Tuple specifying the second wavenumber range (min, max).
    - output_file: Path to the output CSV file.
    """
    intensity_data = []

    for spectrum, name in zip(spectra, file_names):
        # Extract wavenumbers and intensities
        wavenumbers = spectrum.spectral_axis
        intensities = spectrum.spectral_data

        # Function to get max intensity in a given range
        def get_max_in_range(wavenumbers, intensities, wavenumber_range):
            indices = np.where((wavenumbers >= wavenumber_range[0]) & (wavenumbers <= wavenumber_range[1]))[0]
            if len(indices) == 0:
                return None, None  # No data in the range
            max_idx = np.argmax(intensities[indices])
            return wavenumbers[indices][max_idx], intensities[indices][max_idx]

        # Get max intensity for both ranges
        max_wavenumber1, max_intensity1 = get_max_in_range(wavenumbers, intensities, range1)
        max_wavenumber2, max_intensity2 = get_max_in_range(wavenumbers, intensities, range2)

        # Store results
        intensity_data.append({
            "File Name": name,
            f"Max Wavenumber {range1}": max_wavenumber1,
            f"Max Intensity {range1}": max_intensity1,
            f"Max Wavenumber {range2}": max_wavenumber2,
            f"Max Intensity {range2}": max_intensity2
        })

    # Convert to DataFrame
    df = pd.DataFrame(intensity_data)
    
    # Display preview
    print("\nExtracted Maximum Intensities:")
    print(df.head())

    # Export to CSV
    df.to_csv(output_file, index=False)
    print(f"Results exported to {output_file}")

# Define two wavenumber ranges of interest
wavenumber_range1 = (1000, 1100)  # Example range 1
wavenumber_range2 = (1300, 1400)  # Example range 2

# Define the output CSV file path
output_file = r"C:\Users\Taladriz\Desktop\Data\max_intensity_two_ranges.csv"

# Extract and export max intensities for both ranges
extract_max_intensities_in_ranges(corrected_spectra, file_names, wavenumber_range1, wavenumber_range2, output_file)