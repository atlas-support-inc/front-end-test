## To install this backend
```
git clone git@github.com:atlas-support-inc/front-end-test.git
cd front-end-test
brew update
brew install python@3
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r webapp/requirements.txt
```

## To start the server
```
cd webapp
uvicorn main:app --reload
```

