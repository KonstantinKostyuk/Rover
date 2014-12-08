#!/bin/bash

old_text="1:1:0"

while :
do
cmd_text=`cat ~/cmd.txt`
if [ "$cmd_text" != "$old_text" ]
        then
        M1=`echo $cmd_text | cut -d: -f1`
        M2=`echo $cmd_text | cut -d: -f2`
        Claw=`echo $cmd_text | cut -d: -f3`
        echo $M1 $M2 $Claw
        old_text=$cmd_text
fi
done