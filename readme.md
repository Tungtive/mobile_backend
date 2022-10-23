

# AD-RedBack



## Install


Clone the repo to your project folder:
```bash
git clone --branch main [git@github.com:COMP90082-2022-SM2/AD-RedBack.git](mailto:git@github.com:COMP90082-2022-SM2/AD-RedBack.git) your-project-name
```

## Front-end

### Install dependencies:
```bash
cd your-project-name/src/AD-software
npm install
```

### Start the app in the dev environment:
```bash
npm start
```


### Packaging for Production:
```bash
npm run package
```
## Back-end

### Install docker compose
[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

### Install MongoDB Compass
https://www.mongodb.com/try/download/compass

### Install dependencies:
```bash
cd your-project-name/src/backend
pip install -r requirements.txt
```



### Running MongoDB in a Docker Container:
```bash
docker pull mongo
=docker compose up
```


### Set up connection in MongoDB Compass:
```bash
mongodb://root:root@localhost:27017/?authMechanism=DEFAULT
```



### Starting Development:
```bash
python api.py
```
