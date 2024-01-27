#!/bin/bash

TARGET_USER="user"
START_TIME=9
END_TIME=16

while true; do
CURRENT_HOUR=$(TZ="Europe/Vilnius" date "+%H")

if ((CURRENT_HOUR >= START_TIME)) && ((CURRENT_HOUR < END_TIME)); then
PIDS=$(ps -u $TARGET_USER -o pid=,cmd=)

if [ -n "$PIDS" ]; then
	echo "Terminating processes for user $TARGET_USER..."
	while read -r PID CMD; do
		echo "Killing process $PID (Command: $CMD)..."
		kill -9 "$PID"
	done <<< "$PIDS"
	else
		echo "No processes found for user $TARGET_USER."
	fi
	else
		echo "Not within the specified time range. Sleeping..."
fi

sleep 10
done

