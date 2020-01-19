from keras.models import model_from_json
import numpy as np
import pandas as pd

from fish_utils import fish_to_num_mapping

class fish_model:

    def __init__(self, select_top=5):
        self.model = None
        self.species = []
        self.predictions = pd.DataFrame()
        self.prediction_probs  = []  
        self.fish_map = fish_to_num_mapping()     
        self.top_predictions = [] 
        self.select_top = select_top
        self.top_fish_predictions = []
        self.top_fish_predictions_probs = []


    def load_keras_model(self, filename):
        """
        Loads keras model from .json and weights from .hf files

        See also https://machinelearningmastery.com/save-load-keras-deep-learning-models/

        Arguments:
            filename -- string
                Name (and dir) of file to save model to

        Returns:
            model -- fitted keras model object
        """
        # load json and create model        
        json_file = open(filename + ".json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)

        # load weights into new model
        model.load_weights(filename + ".h5")
        #logging.info("Loaded model '%s.json + .h5' from disk" % filename)

        return model


    def load_freshwater_model(self, filepath='model_files/Freshwater_model'):
        """
        Load freshwater model.

        Freshwater species up to element 43 in fish_map
        """
        self.model = self.load_keras_model(filepath)
        self.species = [x for x in self.fish_map.keys()][:43]

        return self.model


    def load_saltwater_model(self, filepath='model_files/Saltwater_model'):
        """
        Load saltwater model
        """
        self.model = self.load_keras_model(filepath)
        self.species = [x for x in self.fish_map.keys()][43:]

        return self.model


    def assure_prob_list(self):
        """
        Ensure prediction probabilities sum to one
        """
        if len(self.prediction_probs) == 0:
            return

        if sum(self.prediction_probs) != 1:
            self.prediction_probs = self.prediction_probs / (sum(self.prediction_probs))

    
    def find_top_predictions(self):
        """
        Find top 'select' predictions 
        """
        if self.predictions.shape[0] == 0:
            return

        temp_df = self.predictions.sort_values(by=['probs'], ascending=False)

        self.top_fish_predictions = temp_df.iloc[:self.select_top,:]['species'].tolist()
        self.top_fish_predictions_probs = temp_df.iloc[:self.select_top,:]['probs'].tolist()


    def predict_for_image(self, img):
        """
        Run prediction model for one image
        """
        if len(img.shape) < 4:
            img = np.asarray(img).reshape((1, img.shape[0], img.shape[1], img.shape[2]))

        # Make prediction
        self.prediction_probs = self.model.predict(img)[0]
        self.assure_prob_list()

        # Combine predicted probabilities and species list to dictionary
        #self.predictions = dict(zip(self.species, self.prediction_probs.tolist()))
        self.predictions = pd.DataFrame({'species': self.species, 
                                         'probs': self.prediction_probs.tolist()})
        
        self.find_top_predictions()



        