## Async API based on aiohttp
***
API created for react social network: [Frontend of social network on react](https://github.com/Nikita-Goncharov/Social-network-React)

### Setup 
* Install requirements(create environment before):
```shell
pip install -r requirements.txt 
```
* Create .env next to the main.py and add content:
```dotenv
DBUSER=user
DBPASSWORD=password
DBHOST=host
DBNAME=databasename
```

* Start server:
```shell
python main.py
```

## API(REST) docs
***
#### Domain: *localhost:8080* 
* ### Users endpoint: */api/v0.1/users*


#### GET:
* Request
    * Query params: page=1(1, 2, 3,...), count=10(1, ...., 100)
    
* Response
```json
{
    "success": true,
    "message": "Users list",
    "users": [
        {"id": 1, "username": "Terry Lozano", "img": "https://api.dicebear.com/7.x/adventurer/svg?seed=Smokey", "status": "Discover yes administration little PM everybody people sport where bag moment name.", "followed": false, "country": "Tajikistan", "city": "Jameshaven"},
        ....
    ],
    "total_count": 40
}
```

#### POST:

* Request
    * Body(json):
```json
{
    "username": "", 
    "img": "", 
    "status": "", 
    "followed": "", 
    "country": "", 
    "city": ""
}
```
* Response
```json
{"success": true, "message": "User created"}
```

#### PUT:
* Request
    * Body(json):
```json
{
    "id": 23,
    "username": "", 
    "img": "", 
    "status": "", 
    "followed": "", 
    "country": "", 
    "city": ""
}
```
* Response
```json
{"success": true, "message": "User updated"}
```

#### DELETE:
* Request

  * Body(json):
```json
{
    "id": 23
}
```
* Response
```json
{"success": true, "message": "User deleted"}
```

***

TODO: add link to production server on pythonanywhere
