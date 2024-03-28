#!/bin/bash
echo " ------- setting up venv ------- "
pushd  /opt/finalyca/sebi_scrapper
python3 -m venv venv
source venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt
deactivate
popd

echo " ------- set up supervisor ------- "
pushd  /opt/finalyca/sebi_scrapper/scripts
cp sebi_scrapper.super.config /etc/supervisor/conf.d/sebi_scrapper.super.conf
supervisorctl reread
supervisorctl update
popd

echo " ------- set up cron ------- "
pushd  /opt/finalyca/sebi_scrapper/scripts
cp cron_sebi_scrapper /etc/cron.d/
popd

echo " ------- opening port ------- "
ufw allow 5000

echo " ------- check from local browser if you can get api heartbeat ------- "