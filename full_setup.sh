pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'