#!/bin/sh
used_percent=$(free | awk '/Mem/{printf("RAM Usage: %.2f%\n"), ($2-$7)/$2*100}' | awk '{print $3}' | cut -d"." -f1)
echo "The Memory Usage is $used_percent%"
if [ $used_percent -ge 80 ]; then
echo "CRITICAL::Running out of Memory...The Usage is ($used_percent%)\" on $(hostname -i) $(hostname -f) <br>"
else
if [ $used_percent -ge 70 ]; then
 echo "WARNING:Running out of Memory...The Usage is ($used_percent%)\" on $(hostname -i) $(hostname -f) <br>"
fi
fi
