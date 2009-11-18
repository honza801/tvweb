#!/bin/bash

PID="cherryd.pid"
LOG="0"
CONFIG="tutorial.conf"
IMPORT="tv_web"
export PYTHONPATH="/home/honza801/tvweb"

case "$1" in 
	-i) 
		IMPORT=$2
		shift 2
	;;
	-log)
		LOG="1"
		shift
	;;
	*)
		echo "unknown option"
	;;
esac

[ -f $PID ] && kill `cat $PID`
echo "cherrypy/cherryd --config=$CONFIG --import=$IMPORT --pidfile=$PID -f"
echo "Logging: $LOG"
if [ $LOG == "1" ]; then
	cherrypy/cherryd --config=$CONFIG --import=$IMPORT --pidfile=$PID -f >cherryd.log 2>&1 &
else
	cherrypy/cherryd --config=$CONFIG --import=$IMPORT --pidfile=$PID -f
fi

