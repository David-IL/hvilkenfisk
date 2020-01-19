from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd



def plot_keras_history(history, plotsize=8):
    """
    Plot loss function over epochs (and accuracy if present).

    Arguments:
        history -- keras History.history object
        plotsize -- scalar integer, default 8
            Size of plot

    Returns:

    """
    n_metrics = len(history.history.keys())
    fig, axes = plt.subplots(n_metrics, 1, figsize=(15, plotsize*n_metrics))
    ind = 0

    # Plot training & validation accuracy values
    if 'acc' in history.history.keys():
        ax = axes[ind]
        ax.plot(history.history['acc'], linewidth=3)
        if 'val_acc' in history.history.keys():
            ax.plot(history.history['val_acc'])
        ax.set_ylim([-0.01,1.01])
        ax.set_title('Model accuracy', fontsize=20)
        ax.set_ylabel('Accuracy', fontsize=18)
        ax.set_xlabel('Epoch', fontsize=18)
        ax.legend(['Train', 'Test'], loc='upper left', fontsize=14)
        ind += 1

    # Plot training & validation loss values
    if n_metrics > 1:
        ax = axes[ind]
    else:
        ax = axes
    ax.plot(history.history['loss'], linewidth=3)
    if 'val_loss' in history.history.keys():
        ax.plot(history.history['val_loss'])
    ax.set_ylim([0,max(history.history['loss'])*1.05])
    ax.set_title('Model loss', fontsize=20)
    ax.set_ylabel('Loss', fontsize=18)
    ax.set_xlabel('Epoch', fontsize=18)
    ax.legend(['Train', 'Test'], loc='upper left', fontsize=14)

    plt.tight_layout()
    plt.show()


def revert_onehot_encode(Y_mat):
    if len(Y_mat.shape) == 1:
        return Y_mat
    if Y_mat.shape[1] <= 1:
        return Y_mat

    n = Y_mat.shape[0]
    y_arr = np.zeros(n)
    for i in range(n):
        y_arr[i] = np.argmax(Y_mat[i,:])
    return y_arr.astype(int)



def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    y_true = revert_onehot_encode(y_true)
    y_pred = revert_onehot_encode(y_pred)

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    #print(cm)

    fig, ax = plt.subplots(figsize=(20,20))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    #ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    #fig.tight_layout()    
    plt.draw()
    return ax