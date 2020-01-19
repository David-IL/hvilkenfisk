# hvilkenfisk (what fish)
![](https://i.imgur.com/EfSGk8c.jpg)

This is a repo for the hobby project *hvilkenfisk*,
a web page where you can upload a picture of a fish caught in Norwegian waters
and it will suggest what fish you have caught. 
In addition to the image the user can select in what kind of water the fish has been caught in
(saltwater or freshwater), and approximate length and weight.
The algorithm attempting to identify the fish species based on these inputs 
is a deep learning models, where we have performed transfer learning on 
a selected set of models based on the dataset established.

The site can be found at [hvilkenfisk.no](hvilkenfisk.no) and is in Norwegian only.


## Data
100 images have been manually selected per fish for a selected set of Norwegian fish species:
- **Freshwater:** 27 species (out of about 41 possible species)
- **Saltwater:** 36 species (out of about 150 possible species)
The sources from which these data have been taken from are mostly Google, but also a
private group on Facebook *Norske artsfiskere*. 
Note that this training data will therefor not be made available for public use.

As the intended use of [hvilkenfisk](hvilkenfisk.no) is for a fisherman/-woman who has caught
a strange looking fish, the data collection procedure has focused on images that could have been 
taken in such a setting. Hence as few aquarium / natural habitat images as possible.


## Modelling
Per now (19.01.2020) no model is linked to the [hvilkenfisk](hvilkenfisk.no) homepage, but
initial experiments have been conducted - see e.g. notebooks in the folder `notebooks/`. 
The model type for the page falls under the category *image classification* or *object recognition*, 
i.e. *which fish is in the image?* (as opposed to *object detection - where in the image is the object/fish?*).
