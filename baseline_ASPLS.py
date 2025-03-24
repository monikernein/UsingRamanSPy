import argparse
import ramanspy as rp

class BaselineASPLS:
    
    def __init__(self, mode = 'normal', test_param = None):
        # Validate and process arguments
        self.parse_args(mode, test_param)
        self.file_name = self.get_file_name() 

    def parse_args(self, mode, test_param):
        if mode == 'unittest':
            if test_param is None:
                print("missing test param")
                exit()
            # Pull file name from unit test
            self.name = test_param['file_name']
        else:
            parser = argparse.ArgumentParser()
            # Adding file path argument
            parser.add_argument("-f", "--File", help = "File to parse")

            # Read arguments from command line
            args =  parser.parse_args()

            if args.File:
                print("File loaded is: %s " % args.File)
                self.name = args.File
            else:
                # Send an error
                print ("File argument not specified with -f \"/path/to/file.mat\"")
                exit()

    def get_file_name(self):
        file_name = self.name
        return file_name

    def preprocessFile(self):
        # Load file
        raman_spectrum = rp.load.witec(self.file_name)         

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

