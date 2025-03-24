import argparse
import ramanspy as rp

class BaselineASPLS:

    def preprocessFile(self):
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
        pipeline = rp.preprocessing.Pipeline([rp.preprocessing.baseline.ASPLS()])

        # Run the pipeline on the data
        data = pipeline.apply(raman_spectrum)

        # Make a popup happen that shows the original and the processed graphs
        # rp.plot is basically an image object so once you set things like spectra you'll get something out of show()
        rp.plot.spectra([raman_spectrum, data], label=["original","processed"], title='Useful Preprocessing Comparison', plot_type="stacked")
        rp.plot.show()

if __name__ == '__main__':
     processor = BaselineASPLS()
     processor.preprocessFile() 

