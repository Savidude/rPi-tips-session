
echo "----------------------------------------------------------------"
echo "|		      Silent Doorbell				                      "
echo "|	              ----------------				                  "
echo "|           ....initializing setup script	              "
echo "----------------------------------------------------------------"

currentDir=$PWD
destination=<DESTINATION_FOR_dash-arpsniffer.py>
#destination="/usr/local/bin/doorbell"

#If the directory at the provided destination is not there, create a directory
if [ ! -d "$destination" ]
then
    mkdir $destination
fi

echo moving dash-arpsniffer.py to destination
sudo cp $currentDir/dash-arpsniffer.py $destination
echo changing permissions for dash-arpsniffer.py
sudo chmod 755 $destination/dash-arpsniffer.py
echo Removing DashSniffer service
sudo update-rc.d -f dashsniffer.sh remove
echo moving DashSniffer to init.d
sudo cp $currentDir/dashsniffer.sh /etc/init.d
echo changing permissions of DashSniffer service
sudo chmod 755 /etc/init.d/dashsniffer.sh
echo symlinking dashsniffer.sh as a service
sudo update-rc.d dashsniffer.sh defaults
echo starting DashSniffer service
sudo service dashsniffer.sh start
echo setup completed successfully