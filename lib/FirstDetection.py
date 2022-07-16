from imageai.Detection import ObjectDetection
import os

'''
# ---------------------------------------------------------------
# Detect objects in image
# ---------------------------------------------------------------
def detect_objects(image, model_path, model_name, threshold=0.5, verbose=False):
    
    Detect objects in image
    input:
        image: image to detect objects (numpy array)
        model_path: path to model (str)
        model_name: name of model (str)
        threshold: threshold for detection (float)
        verbose: additional prints for debugging (bool)
    output:
        objects: list of detected objects (list)
    
    # create detector
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel(verbose=verbose)
    # detect objects
    objects = detector.detectObjectsFromImage(input_image=image,
                                              output_image_path=f"images/{model_name}_detected.png",
                                              minimum_percentage_probability=threshold)
    return objects

'''
# ---------------------------------------------------------------
# Detect objects in image
# ---------------------------------------------------------------
def first_detection_image(): 
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "models/resnet50_coco_best_v2.1.0.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(f'{execution_path}/images/CERN-THESIS-2022-048/' , "CERN-THESIS-2022-048_0001-064.png"), output_image_path=os.path.join(execution_path , "imagenew.jpg"))

    for eachObject in detections:
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )