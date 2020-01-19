import cv2
import numpy as np


def preprocess_image(filepath, img=None, size=224):
    """
    Take an image, preprocess and return it as numpy array data.

    Pre-processing steps;
        - Ensure correct color order (BGR2RGB)
        - Reshape image to (sizexsize). If original image 
          is not square, we mirror it when padding (cv2.BORDER_REFLECT)
        - Reshape image tensor from (size, size, 3) to (1, size, size, 3)
          (which is they format the model needs)
    """
    if img is None:
      img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
    print(img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    img = reshape_img_to_square(img, size=size)
    img = np.asarray(img).reshape((1, size, size, 3))

    return img


def reshape_img_to_square(img, size=224):
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
        
    return new_img

