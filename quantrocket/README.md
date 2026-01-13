https://www.quantrocket.com
https://www.quantrocket.com/docs
https://github.com/quantrocket-llc

# installation
curl 'https://www.quantrocket.com/composefiles/latest/local/docker-compose.yml' -o docker-compose.yml
cd ~/quantrocket
docker compose -p quantrocket up -d

# quick start
- go to https://quantrocket.auth0.com/ login and go to https://www.quantrocket.com/account/ to copy license key
- open http://localhost:1969/ on browser
- go to quickstart tab
- complete step2 on quickstart
- go to terminal tab [quantrocket ibg credentials 'ibg1' --username 'xxx' --paper] to connect to ibkr