# Reporter app

This application is for sending daily email on the same time.

## Deployment

Clone code:

```
git clone https://github.com/crocodilered/reporter.git
cd reporter
```

Copy .env.example to .env and edit .env for desired settings:

```
cp .env.example .env
nano .env
```

Run docker containers:

```
sudo docker compose up -d --build
```

## To do

* Randomize sending time.
* Take report file from volume (to do not rebuild containers when new report 
  files arrived).