import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

from .img_utils import reshape_img_to_square

def plot_random_images(image_list):
    """
    Resize and plot images
    """
    fig, ax = plt.subplots(4, 4, figsize=(20, 20))
    for i in range(4): 
        for j in range(4):
            img_tit = image_list[random.randint(0,len(image_list))]
            temp_img = cv2.imread(img_tit, cv2.IMREAD_UNCHANGED)
            temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)    
            temp_img = reshape_img_to_square(temp_img, plot_compressed=False)
            ax[i][j].imshow(temp_img)
            ax[i][j].set_title(img_tit.split('/')[-1], fontsize=16)
        
    plt.tight_layout()
    plt.show()


def plot_random_images_hdf5(images_hdf5, labels_hdf5):
    """
    Plot random images from hdf5 file
    """    
    #temp_x = np.array(images_hdf5["train_set"][:]) # your train set features
    #temp_y = np.array(images_hdf5["train_labels"][:]) # your train set targets

    fig, ax = plt.subplots(4, 4, figsize=(20, 20))
    for i in range(4): 
        for j in range(4):
            img_num = random.randint(0, labels_hdf5.shape[0])            
            ax[i][j].imshow(images_hdf5[img_num, :,:,:])
            ax[i][j].set_title(labels_hdf5[img_num].astype(str)[0], fontsize=16)
        
    plt.tight_layout()
    plt.show()

    #del temp_x, temp_y