"""
Web API to recognize fish species in an image 
(based on fish in Norwegian waters)

Example how to run this file:

Notes:
    - We will use fastAPI to build a REST API for hvilkenfisk.no, see
        https://pypi.org/project/fastapi/
        https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
    - To try to run the API locally, go to "app/" and run in command prompt
         uvicorn main:app --debug
      where
        - 'main' refers to the file 'app/main.py' (i.e. this file),
        - 'app' is the object created inside 'app/main.py' 
          (when running 'app = FastAPI()')
        - '--debug' makes the server restart after code changes 
          (only do this for dev)
    - After running the above command, the app will be available through 
      local port 8000 (127.0.0.1:8000).
    - Go to http://127.0.0.1:8000/docs to get automatic interactive API 
      documentation (provided by Swagger UI)    

@author: David Volent Lindberg
"""
# Import standard modules
from fastapi import FastAPI, File, UploadFile
import tempfile
import os
import numpy as np
import cv2
import json
import time
from datetime import datetime

# Import custom modules
from model_utils import fish_model
from img_preprocess import preprocess_image

# Start FastAPI app
APP_INFO = {
    "Welcome": "This is the fish recognizer module of the 'hvilkenfisk' webpage",
    "Started at": datetime.now().strftime("%Y-%d-%m %H:%M:%S"),
}
STATS = list()
app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Welcome": "This is the web API for the Norwegian fish recognizer website, see hvilkenfisk.no"
    }


# @app.post("/uploadFile/")
def parse_image(file: UploadFile = File(...)):
    """
    Adapted from this source; https://github.com/tiangolo/fastapi/issues/426
    """
    extension = os.path.splitext(file.filename)[1]
    _, path = tempfile.mkstemp(prefix="parser_", suffix=extension)

    # Write to file in chunks for not to go OOM
    with open(path, "ab") as f:
        for chunk in iter(lambda: file.file.read(10000), b""):
            f.write(chunk)

    # extract content, which should be an image
    img = cv2.imread(path)

    # remove temp file
    os.close(_)
    os.remove(path)

    # Return image
    # return {"image": img}
    return img


@app.put("/run_model/{inputs}")
def run_model(
    water_type: str = "freshwater",
    approximate_length: float = 0,
    approximate_weight: float = 0,
    image: UploadFile = File(...),
):
    """
    Run fish recognizer model.

    To request files from client, see FastAPI docs here:
        - https://fastapi.tiangolo.com/tutorial/request-files/
    """
    # Import model according to water type
    tic_super = time.time()
    print("Loading model...")
    pred_model = fish_model()

    if water_type == "freshwater":
        pred_model.load_freshwater_model()
    elif water_type == "saltwater":
        pred_model.load_saltwater_model()
    toc_load_model = time.time()
    print("SUCCESS: Model loaded")

    # Take image as input by saving to temporary file which opencv will read from
    print("Loading image...")
    img = parse_image(image)

    original_image = {"filename": image.filename, "img_size": str(img.shape)}
    toc_load_image = time.time()
    print("SUCCESS: Image %s loaded" % image.filename)

    # Preprocess image
    image_preprocessed = preprocess_image("no_path", img=img)
    toc_preprocess = time.time()

    # Run model on image
    pred_model.predict_for_image(image_preprocessed)
    toc_predict = time.time()

    # Inputs
    inputs = {
        "water_type": water_type,
        "approximate_length": approximate_length,
        "approximate_weight": approximate_weight,
        "original_image": original_image,
    }

    # Time keeping
    time_keeping = {
        "date_initiated": str(datetime.now()),
        "time_load_model": "%.4f sec" % (toc_load_model - tic_super),
        "time_load_image": "%.4f sec" % (toc_load_image - toc_load_model),
        "time_preprocess_image": "%.4f sec" % (toc_preprocess - toc_load_image),
        "time_run_model": "%.4f sec" % (toc_predict - toc_preprocess),
        "TOTAL_TIME": "%.4f sec" % (toc_predict - tic_super),
    }

    # Define result
    result = {
        "inputs": inputs,
        "fish_predictions": pred_model.top_fish_predictions,
        "fish_prediction_probs": pred_model.top_fish_predictions_probs,
        "time_keeping": time_keeping,
    }

    return result


# if name == __main__:
#    FRESHWATER_MODEL =
#    SALTWATER_MODEL = 1
