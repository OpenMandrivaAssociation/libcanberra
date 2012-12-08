
# (cg) Set the driver properly based on the current sound profile
CONFIG="/etc/sound/profiles/current/canberra.conf"
if [ -r $CONFIG ]; then
  . $CONFIG
fi

if [ -n "$CANBERRA_DRIVER" ]; then
  export CANBERRA_DRIVER
fi
