import argparse
import ramanspy as rp

#TODO help message
# Initialize parser
parser = argparse.ArgumentParser()

# Adding file path argument
parser.add_argument("-f", "--File", help = "File to parse")

# Read arguments from command line
args =  parser.parse_args()

if args.File:
    print("File loaded is: %s " % args.File)
    raman_spectrum =  rp.load.witec(args.File)
else:
    # Send an error
    print ("File argument not specified with -f \"/path/to/file.mat\"")
    exit()

# Create baseline preprocessing pipeline, there are others that can be used
# pipeline = rp.preprocessing.Pipeline([rp.preprocessing.baseline.ASPLS()])
# Example with baseline, spike removal, denoising, cropping 
pipeline = rp.preprocessing.Pipeline([
    rp.preprocessing.baseline.ASPLS(),
    rp.preprocessing.despike.WhitakerHayes(),
    rp.preprocessing.denoise.Gaussian(),
    rp.preprocessing.misc.Cropper(region=(None, 2000))
])

# Analsysis methods to sort out
# rp.analysis.unmix, rp.analysis.cluster, rp.analysis.decompose

# Run the pipeline on the data
data = pipeline.apply(raman_spectrum)

# Make a popup happen that shows the original and the processed graphs
# rp.plot is basically an image object so once you set things like spectra you'll get something out of show()
rp.plot.spectra([raman_spectrum, data], label=["original","processed"], title='Useful Preprocessing Comparison', plot_type="stacked")
rp.plot.show()

# Analysis methods to sort out
unmix = rp.analysis.unmix.VCA(n_endmembers=4, abundance_method="ucls")

projections, components = unmix.apply(data)
rp.plot.spectra(components, data.spectral_axis, plot_type="single stacked", title='Unmix')
rp.plot.show()

# TODO clustering not working yet
# cluster = rp.analysis.cluster.KMeans(n_clusters=1)
# clusters =  cluster.apply(data)

# rp.plot.spectra(clusters, data.spectral_axis, plot_type="single stacked", title='Cluster')
# rp.plot.show()

# TODO decompose not working yet, I think because it needs maps
# decomp =  rp.analysis.decompose.ICA(n_components=4)
# p, c = decomp.apply(data)

# rp.plot.spectra(c, data.spectral_axis, plot_type="single stacked", title='Decompose')
# rp.plot.show()

