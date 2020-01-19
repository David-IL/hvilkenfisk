# Import keras modules
import keras
import keras.backend as K
K.set_image_data_format('channels_last')
from keras.layers import Dense, GlobalAveragePooling2D, Activation
from keras.applications import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam


def mobilnet_fish_recognition_model(input_shape=None, plot_to_file=False, n_fish=17):
    """
    Implementation of the initial keras model.
    
    NOTE: Discarding the last layer in the original Mobilenet model (setting include_top=False)
    disregards the 6 layers (with one fully connected 1024 -> 1000 nodes layer)
        global_average_pooling2d_4 ( (None, 1024)              0         
        reshape_1 (Reshape)          (None, 1, 1, 1024)        0         
        dropout (Dropout)            (None, 1, 1, 1024)        0         
        conv_preds (Conv2D)          (None, 1, 1, 1000)        1025000   
        act_softmax (Activation)     (None, 1, 1, 1000)        0         
        reshape_2 (Reshape)          (None, 1000)              0         
    
    Arguments:
        input_shape -- shape of the images of the dataset

    Returns:
        model -- a Model() instance in Keras
    """  
    ### Import the mobilenet model and discard the last 1000 neuron layer (1000 classes) ###
    base_model = MobileNet(weights='imagenet', include_top=False, input_shape=input_shape) 
    X = base_model.output
    
    # 
    X = GlobalAveragePooling2D()(X)
    #X = Dense(1024, activation='relu')(X) #we add dense layers so that the model can learn more complex functions and classify for better results.
    #X = Dense(1024, activation='relu')(X) #dense layer 2
    #X = Dense(512, activation='relu')(X) #dense layer 3
    #preds = Dense(2, activation='softmax')(X) #final layer with softmax activation
    
    ### Dense fully connected layer 2 - final layer ###
    X = Dense(n_fish, name='fc_final')(X)
    
    ### Prediction layer - here a binary classification prediction ###
    preds = Activation(activation='sigmoid', name='prediction')(X)

    model = Model(inputs=base_model.input, outputs=preds)    
    
    # Plot model if specified
    if plot_to_file is True:
        plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)    
        
    # Will use pre-trained weights on all convolutional layers (up to layer 87) - only train fully connected ones
    for layer in model.layers[:87]:
        layer.trainable = False
    for layer in model.layers[87:]:
        layer.trainable = True
    
    return model