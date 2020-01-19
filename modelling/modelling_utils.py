from keras.models import model_from_json
import logging


def save_keras_model(model, filename):
    """
    Saves keras model to .json and weights to .hf files

    See also https://machinelearningmastery.com/save-load-keras-deep-learning-models/

    Arguments:
        model -- fitted keras model object
        filename -- string
            Name (and dir) of file to save model to

    Returns:

    """
    # serialize model to JSON
    model_json = model.to_json()
    with open(filename + ".json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    model.save_weights(filename + ".h5")
    logging.info("Saved model '%s.json + .h5' to disk" % filename)


def load_keras_model(filename):
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
    logging.info("Loaded model '%s.json + .h5' from disk" % filename)

    return model
