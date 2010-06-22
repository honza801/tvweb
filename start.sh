#!/bin/bash

PID="cherryd.pid"
LOG="0"
CONFIG="etc/cherryd-tvweb.conf"
IMPORT="tv_web"
export PYTHONPATH=`pwd`

function printhelp {
	cat << EOF
Usage: `basename $0` [-i|-log|--help]
  -i    import some other module
  -log  log into cherryd.log and put itself to background
  --help this help screen
EOF
}

case "$1" in 
	-i) 
		IMPORT=$2
		shift 2
	;;
	-log)
		LOG="1"
		shift
	;;
	--help)
		printhelp
		exit 1
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

