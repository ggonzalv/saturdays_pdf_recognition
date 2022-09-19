import torch
import cv2

from lib.utils import bcolors

from detectron2.config import get_cfg
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.config import CfgNode as CN

from predictor.backbone import build_vit_fpn_backbone

# ---------------------------------------------------------------
# Load predictor model
# ---------------------------------------------------------------


def loadPredictor(params: dict, verbose: bool = False):
    '''
    Loads the predictor model.
    output:
        predictor: the predictor model
        verbose: additional prints for debugging (bool)
    '''

    if verbose:
        print(f"{bcolors.OKBLUE}Loading transformers model...{bcolors.ENDC}")

    # Step 1: instantiate config
    cfg = get_cfg()
    add_vit_config(cfg)
    cfg.merge_from_file(params['modelConfig'])

    # Step 2: add model weights URL to config
    cfg.merge_from_list(params['modelWeights'])

    # Step 3: set device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    cfg.MODEL.DEVICE = device

    # Step 4: define model
    predictor = DefaultPredictor(cfg)

    return predictor

# ---------------------------------------------------------------
# Predict image
# ---------------------------------------------------------------


def predictImage(predictor, img):
    '''
    Predict image.
    input:
        predictor: the predictor model (DefaultPredictor)
        imagePath: the image to predict 
    output:
        predictions: tagged boxes (dict)
    '''

    return predictor(img)["instances"]

# ---------------------------------------------------------------
# Load cv2 image
# ---------------------------------------------------------------


def loadImage(imagePath: str):
    """
    Load cv2 image.
    input:
        imagePath: the image to predict 
    output:
        image: the image to predict 
    """
    return cv2.imread(imagePath)

# ---------------------------------------------------------------
# Visualize predictions
# ---------------------------------------------------------------


def visualizePredictions(predictions: dict, img, outputPath: str, verbose: bool = False):
    '''
    Visualize predictions.
    input:
        predictions: tagged boxes (dict)
        img: input image 
        outputPath: path to save the image
        verbose: additional prints for debugging
    '''

    if verbose:
        print(
            f"{bcolors.OKBLUE}Now creating boxes for visualization...{bcolors.ENDC}")
    md = MetadataCatalog.get('publaynet_val')
    md.set(thing_classes=["text", "title", "list", "table", "figure"])
    # Step 6: visualize results
    v = Visualizer(img[:, :, ::-1],
                   md,
                   scale=1.0,
                   instance_mode=ColorMode.SEGMENTATION)
    result = v.draw_instance_predictions(predictions.to("cpu"))
    result_image = result.get_image()[:, :, ::-1]

    # step 6: save
    cv2.imwrite(outputPath, result_image)


# ---------------------------------------------------------------
# Add model configuration parameters to the configuration
# ---------------------------------------------------------------
def add_vit_config(cfg):
    '''
    Add config for VIT.
    '''
    _C = cfg

    _C.MODEL.VIT = CN()

    # CoaT model name.
    _C.MODEL.VIT.NAME = ""

    # Output features from CoaT backbone.
    _C.MODEL.VIT.OUT_FEATURES = ["layer3", "layer5", "layer7", "layer11"]

    _C.MODEL.VIT.IMG_SIZE = [224, 224]

    _C.MODEL.VIT.POS_TYPE = "shared_rel"

    _C.MODEL.VIT.DROP_PATH = 0.

    _C.MODEL.VIT.MODEL_KWARGS = "{}"

    _C.SOLVER.OPTIMIZER = "ADAMW"

    _C.SOLVER.BACKBONE_MULTIPLIER = 1.0

    _C.AUG = CN()

    _C.AUG.DETR = False
