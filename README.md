<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

# Git Buddies REST
REST-API for official Git Buddies
# ⚙️ Prerequisites

- You need to have python installed. You can install it from microsoft store or follow this [guide](https://www.geeksforgeeks.org/how-to-install-python-on-windows/).

# Setting up a Virtual Enviroment

It’s a common practice to have your Python apps and their instances running in virtual environments. Virtual environments allow different package sets and configurations to run simultaneously, and avoid conflicts due to incompatible package versions. 

Create a Virtual Enviroment in python by executing following command.
```bash
$ python3 -m venv env
```
activate the virtual environment.
```bash
# On Unix or MacOS (bash shell): 
/path/to/venv/bin/activate

# On Unix or MacOS (csh shell):
/path/to/venv/bin/activate.csh

# On Unix or MacOS (fish shell):
/path/to/venv/bin/activate.fish

# On Windows (command prompt):
\path\to\venv\Scripts\activate.bat

# On Windows (PowerShell):
\path\to\venv\Scripts\Activate.ps1
```

# Installation:
now install all the dependencies.
```bash
 $ pip install -r requirements.txt
```

# Working:
Thats it! You are ready to go. </br>
run the Project by executing this.
```bash
$ uvicorn <filename without extension>:app --reload
```

Project will be available on
``http://127.0.0.1:8000``

for accessing Swagger UI
``http://127.0.0.1:8000/docs``

# API Reference


### TOKEN ENDPOINT

| Endpoint | Request | Parameter | Type     | Description                       |

| :-------- | :-------- | :------- | :-------------------------------- |
| `/token/`     | `POST`     |   `username,password,scope`  | `string` | **REQUIRED**  |


### USER ENDPOINT

| Endpoint | Request | Parameter | Type     | Description                       |

| :-------- | :-------- | :------- | :-------------------------------- |
| `/user/me`     | `GET`     |  -     | - | -  |
| `/user/add`     | `POST`     |  -     | - | -  |
| `/user/delete`     | `DELETE`     |  -   | -| -  |
| `/user/update`     | `PUT`     | -     | - | -  |
| `/user/all`     | `GET`     | -    | - | -  |

### REPOSITORY ENDPOINT

| Endpoint | Request | Parameter | Type     | Description                       |
| :-------- | :-------- | :------- | :-------------------------------- |

| `/boosted/repos`     | `GET`     |-     | - | -  |
| `/boosted/repos`     | `POST`     |-     | - | -  |
| `/boosted/repos/{id}`     | `PUT`     | `id`   | `string` | **REQUIRED**  |
| `/boosted/repos/{id}`     | `DELETE`     | `id`   | `string` | **REQUIRED**  |



# Feedback
If you have any feedback, please reach out to me at  `rimmelasghar4@gmail.com` 


[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

```
print('Code by Rimmel with ❤')
```

