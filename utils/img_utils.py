import cv2
import imutils
import os, sys
import h5py
import matplotlib.pyplot as plt
import numpy as np
from string import digits

def reshape_img_to_square(img, size=224, plot_compressed=True):
    """
    Reshape image to square (size x size) shape (default 224x224).

    OpenCV has different types of way to fill, we use cv2.BORDER_REFLECT.
    
    Note that default size for mobilenet and mobilenet2 model is 224x224,
    
    References:
    - https://keras.io/applications/#mobilenet
    - https://stackoverflow.com/questions/43391205/add-padding-to-images-to-get-them-into-the-same-shape
    """
    old_size = img.shape[:2] # old_size is in (height, width) format

    ratio = float(size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format

    img = cv2.resize(img, (new_size[1], new_size[0]))

    delta_w = size - new_size[1]
    delta_h = size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    # Some cv2 reshape options; [cv2.BORDER_REFLECT, cv2.BORDER_WRAP, cv2.BORDER_CONSTANT]
    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_REFLECT)

    if plot_compressed:
        plt.imshow(new_img)
        
    return new_img

    

def reshape_img_deprecated(img, size=(224,224), plot_compressed=True):
    """
    Reshape image to square shape (default 224x224).

    OpenCV has different types of way to fill, we use cv2.BORDER_REFLECT.
    
    Note that default size for mobilenet and mobilenet2 model is 224x224,
    see https://keras.io/applications/#mobilenet
    """
    s = size[0]
    
    #Creating a dark square with NUMPY  
    f = np.zeros((size[0], size[1], 3), np.uint8)

    #Getting the bigger side of the image
    if img.shape[0] > img.shape[1]:
        new_width = (s * img.shape[1]) // img.shape[0]
        img = cv2.resize(img, (new_width, s))
    else:
        new_height = (s * img.shape[0]) // img.shape[1]
        img = cv2.resize(img, (s, new_height))

    #Getting the centering position
    ax, ay = (s - img.shape[1]) // 2, (s - img.shape[0]) // 2

    #Pasting the 'image' in a centering position
    f[ay:img.shape[0]+ay, ax:ax+img.shape[1]] = img
    
    if plot_compressed:
        plt.imshow(f)
        
    return f


def list_images(img_folder="Fiskebilder/Ferskvann/"):
    """
    List images in given directory
    """
    fishes = os.listdir(img_folder)
    images = []
    for fish in fishes:
        temp_imgs = os.listdir(img_folder + fish + '/')
        temp_imgs = [img_folder + fish + '/' + s for s in temp_imgs]
        images.append(temp_imgs)

    images = [item for sublist in images for item in sublist]
    
    return images    


def _add_noise_to_image(img, std=20):
    """
    Add Gaussian noise to an image
    """
    img_noisy = img.copy()
    cv2.randn(img_noisy, (0,0,0), (std, std, std)) 
    noisy_img = img_noisy + img
    
    return noisy_img


def augment_image_data(img, plot_augmentations=True):  
    """
    Augment an image by flipping it, rotating it and adding noise.

    Default setting is to generate 11 augmentations per image.
    """  
    rows, cols, ch = img.shape
    img_augmentations = np.ndarray((rows, cols, ch, 12)).astype(int)
    img_augmentations[:,:,:,0] = img
    ind = 1

    # Flipping
    flips = [0, 1, -1]
    for flip in flips:
        img_augmentations[:,:,:,ind] = cv2.flip(img, flip)
        ind += 1    
    
    # Rotation
    rotations = [45, 90, 270, 315]
    for rot in rotations:
        img_augmentations[:,:,:,ind] = imutils.rotate(img, rot, scale=1.5)        
        ind += 1    
    
    # Adding noise    
    stds = [10, 20, 30, 40]    
    img_inds_noise = [0, 1, 5, 6]
    for i, std in enumerate(stds):
        img_to_noise = img_augmentations[:,:,:,img_inds_noise[i]]
        img_augmentations[:,:,:,ind] = _add_noise_to_image(img_to_noise, std)  
        ind += 1
    
    # Plot augmentations
    if plot_augmentations:
        fig, ax = plt.subplots(3, 4, figsize=(20, 15))
        ind = 0
        for i in range(3): 
            for j in range(4):                    
                ax[i][j].imshow(img_augmentations[:,:,:,ind].astype(np.uint8))
                ind += 1

        plt.tight_layout()
        plt.show()

    return img_augmentations


def combine_data_to_hdf5(filename="fish_training.hdf5", 
                        img_folder="Fiskebilder/Ferskvann/",
                        size=224, augment_data=True, 
                        verbose=True):
    """
    Combine fish images from image files (.jpg and .png) and their species title
    in a hdf5 file format.
    """
    images = list_images(img_folder)
    if augment_data:
        n_augments = 11
    else:
        n_augments = 0
    n_data = len(images) * (1 + n_augments)

    # Create a hdf5 file; open a hdf5 file and create arrays for feature set (images), label set and metadata    
    hdf5_path = "data/" + filename
    if os.path.isfile(hdf5_path):
        raise ValueError('A file already exists in "../../data/" with the specified name "%s"'%filename)
    if filename[-5:] != '.hdf5':
        raise ValueError('The filename should end with ".hdf5", argument given: "%s"'%filename)
            
    dt_meta = h5py.special_dtype(vlen=bytes)  # For ASCII strings, see http://docs.h5py.org/en/latest/strings.html
    train_shape = (n_data, size, size, 3)

    hdf5_file = h5py.File(hdf5_path, mode='w')
    hdf5_file.create_dataset("train_set", train_shape, np.uint8)
    hdf5_file.create_dataset("train_labels", (n_data, 1), dtype=dt_meta)
    hdf5_file.create_dataset("train_metadata", (n_data, 1), dtype=dt_meta)

    # Insert into hdf5 object
    ind = 0
    for img_path in images:
        im = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) 
        im = reshape_img_to_square(im, size=224, plot_compressed=False)
        im_target = _fish_name_from_path(img_path)
        
        if augment_data:
            img_augs = augment_image_data(im, plot_augmentations=False)
            for i in range(12):
                hdf5_file["train_set"][ind, ...] = img_augs[:,:,:,i]
                hdf5_file["train_labels"][ind] = [im_target] 
                ind += 1
        else:
            hdf5_file["train_set"][ind, ...] = im
            hdf5_file["train_labels"][ind] = [im_target] 
            ind += 1   
        if (ind / 500) == 0:
            print("Done converting and adding %i images, at species %s" % (ind, im_target))
    hdf5_file.close()


def _fish_name_from_path(string):
    s = string.split('/')[-1].split('.')[0]
    remove_digits = str.maketrans('', '', digits)
    
    return s.translate(remove_digits)