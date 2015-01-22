#!/bin/bash


old_text="1:1:0"

if [ $# == "1" ]
  then
    cmd_text=$1
if [ "$cmd_text" != "$old_text" ]
        then
        M1=`echo $cmd_text | cut -d: -f1`
        M2=`echo $cmd_text | cut -d: -f2`
        Claw=`echo $cmd_text | cut -d: -f3`
        echo $M1 $M2 $Claw
        python /home/ubuntu/orion/control.py $M1 $M2
        if [ $Claw -eq 0 ]
                then
                sudo /home/ubuntu/pololu/maestro_linux/maestro.sh /dev/ttyACM1 1 8500
                sudo /home/ubuntu/pololu/maestro_linux/maestro.sh /dev/ttyACM1 0 9000
                else
                sudo /home/ubuntu/pololu/maestro_linux/maestro.sh /dev/ttyACM1 0 8000
                sudo /home/ubuntu/pololu/maestro_linux/maestro.sh /dev/ttyACM1 1 4000
        fi
        old_text=$cmd_text
fi
  else
while :
do
cmd_text=`cat ~/cmd.txt`
if [ "$cmd_text" != "$old_text" ]
        then
        M1=`echo $cmd_text | cut -d: -f1`
        M2=`echo $cmd_text | cut -d: -f2`
        Claw=`echo $cmd_text | cut -d: -f3`
        echo $M1 $M2 $Claw
	python /home/ubuntu/orion/control.py $M1 $M2
	if [ $Claw -eq 0 ]
		then
                sudo /home/ubuntu/pololu/maestro_linux/maestro.sh /dev/ttyACM1 1 8500
		sudo /home/ubuntu/pololu/maestro_linux/maestro.sh /dev/ttyACM1 0 9000
		else
                sudo /home/ubuntu/pololu/maestro_linux/maestro.sh /dev/ttyACM1 0 8000
                sudo /home/ubuntu/pololu/maestro_linux/maestro.sh /dev/ttyACM1 1 4000
	fi
        old_text=$cmd_text
fi
done
fi
