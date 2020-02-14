#!/bin/bash

# Change this to install under a different name
name="alfonslistener"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Remove the old .service file
rm /etc/systemd/system/"$name".service

service=$(cat alfonslistener.service) 
cat >/etc/systemd/system/$name.service <<EOL
${service//"%path%"/$DIR}
EOL

chmod 644 /etc/systemd/system/"$name".service

systemctl daemon-reload
systemctl enable $name
systemctl start $name
