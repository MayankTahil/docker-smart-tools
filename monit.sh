SWCH=true

## Logic to check if the connector is still running.
while [ "$SWCH" = "true" ]; do
	if ps aux | grep -q connector
	then 
	   sleep 5;
	else
	   exit 0;
	fi
done