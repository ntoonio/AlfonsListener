name="alfonslistener"

rm /etc/systemd/system/"$name".service
cp "$name".service /etc/systemd/system/"$name".service
chmod 644 /etc/systemd/system/"$name".service

systemctl daemon-reload
systemctl enable $name
systemctl start $name
