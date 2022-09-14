import json
import werkzeug

from lib.imageModel import *
from lib.utils import *
from lib.readData import *
from lib.objectExtraction import *


def main(input_file: str, format_output: str):

    with open('params.json') as json_file:
        params = json.load(json_file)

    createDir('/tmp/test-api/tmp_output_files', True)
    createDir('/tmp/test-api/images/')

    if input_file.endswith(".jpg"):
        image = loadImage(input_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        tableConvertor(image, format_output,
                       input_file.replace(".jpg", ""), True)
        return

    model = loadPredictor(params)
    read_input(input_file)
    images = [loadImage(f'/tmp/test-api/images/{image}')
              for image in sorted(os.listdir('/tmp/test-api/images'))]

    for i, image in enumerate(images):
        boxes = predictImage(model, image)
        tables = boxes[(boxes.pred_classes == 3) & (
            boxes.scores > 0.7)].pred_boxes  # 3 is table class
        figures = boxes[(boxes.pred_classes == 4) & (
            boxes.scores > 0.7)].pred_boxes  # 4 is figure class
        extractResults(tables, format_output, figures, image, i)
    compressOutput()
    cleanDirectories()
