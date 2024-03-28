#!/bin/bash
echo " ------- upgrading server ------- "
sudo apt-get update --yes --quiet
sudo apt-get upgrade --yes --quiet

echo " ------- installing packages ------- "
sudo apt-get --yes --quiet install build-essential git python3.8 python3.8-dev python3.8-venv sqlite3 supervisor

echo " ------- making directory ------- "
mkdir /opt/finalyca
mkdir /opt/finalyca/log

echo " ------- cloning repository ------- "
pushd  /opt/finalyca
git clone https://deploy:oJfHVyFPT_Ea3xgX32Zp@gitlab.com/f2504/sebi_scrapper.git
popd
