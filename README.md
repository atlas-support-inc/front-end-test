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

To view all the APIs, go to http://localhost:8000/docs#/

## Infra

### Users:
Here is how the user model looks like

```
class User(BaseModel):
    id: Optional[int]
    username: str
    password: str
```

Here are the different APIs related to users:
- http://localhost:8000/auth/create_users a POST call to this API will seed the users
- http://localhost:8000/auth/login a post call which logs the user in and will set the session cookie for other APIs
- http://localhost:8000/auth/me a get call to get logged in user
- http://localhost:8000/auth/users a get call to return all other user

### Chat:
Here is how the chat model looks like

```
class Chat(BaseModel):
    id: Optional[int]
    from_user_id: Optional[int]
    to_user_id: int
    message: str
```

- http://localhost:8000/chat/list a get call to get list of all chat for this user
- http://localhost:8000/chat/create a get call to create new chat for this user


### Websocket connection
You can connect to websocket using following endpoint: 
http://localhost:8000/ws/{user_id}

Server will send following two information on this websocket
- list of all connected users (updated list whenever there is a change)
- a message when current user has received has a new message

