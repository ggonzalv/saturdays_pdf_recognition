FROM python:3.9 as builder
WORKDIR /code
COPY requirements.txt requirements.txt
COPY requirements_api.txt requirements_api.txt
COPY src/lib/ src/lib/
COPY src/predictor/ src/predictor/
RUN pip install -r requirements.txt #!COMMIT
RUN python -m pip install 'git+https://github.com/facebookresearch/detectron2.git' #!COMMIT
# RUN pip uninstall markupsafe #!COMMIT
RUN pip install -r requirements_api.txt #!COMMIT
RUN sed -i 's/from collections import OrderedDict, MutableMapping/from collections import OrderedDict/g' /usr/local/lib/python3.*/site-packages/flask_restplus/model.py #!COMMIT
RUN sed -i '/from collections import OrderedDict/a from collections.abc import MutableMapping' /usr/local/lib/python3.*/site-packages/flask_restplus/model.py #!COMMIT
RUN apt-get update && apt-get install wget build-essential cmake libfreetype6-dev pkg-config libfontconfig-dev libjpeg-dev libopenjp2-7-dev -y #!COMMIT
# Poppler instalation
RUN wget https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz \
    && tar -xf poppler-data-0.4.9.tar.gz \
    && cd poppler-data-0.4.9 \
    && make install \
    && cd .. \
    && wget https://poppler.freedesktop.org/poppler-20.08.0.tar.xz \
    && tar -xf poppler-20.08.0.tar.xz \
    && cd poppler-20.08.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && ldconfig #!COMMIT
CMD tail -f /dev/null
RUN apt-get update #!COMMIT
# Tesseract installation
RUN apt-get -y install tesseract-ocr #!COMMIT
RUN apt-get install tesseract-ocr-ben #!COMMIT
RUN wget https://github.com/tesseract-ocr/tessdata/raw/main/spa.traineddata -O /usr/share/tesseract-ocr/4.00/tessdata/spa.traineddata 2> /dev/null #!COMMIT
# CV2 dependencies NER V2
RUN apt-get update  #!COMMIT
RUN apt-get install ffmpeg libsm6 libxext6  -y #!COMMIT

FROM builder
WORKDIR /code
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5020
ENV FLASK_ENV=development
EXPOSE 5020
COPY . .
CMD ["python3","-m","flask", "run", "--host=0.0.0.0", "--port=5020"]
