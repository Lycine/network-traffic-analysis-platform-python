#!/bin/bash
 
#test_MemoryUsageShell
 
 
while :
        do
        threshold=90
        csv2es_pid=`ps -ef |grep csv2es|grep python |awk '{print $2}'`
        mem_total=`free | grep "Mem:" |awk '{print $2}'`
        mem_used=`free | grep "Mem:" |awk '{print $3}'`
        mem_used_rate=`awk 'BEGIN{printf"%.2f\n",('$mem_used'/'$mem_total')*100}'`
#        echo $mem_used_rate
        flag=$(echo "$mem_used_rate > $threshold" | bc)
        if [ $flag -eq 1 ];then
            printf '\r''Less available memory: '$mem_used_rate'>'$threshold' '
            sleep 30
            if [ "$csv2es_pid" =  "" ];then
                printf 'pid: empty'
                kill -9 $csv2es_pid
            else :
                printf 'pid: '$csv2es_pid
            fi
        else :
            printf '\r''Memory safe: '$mem_used_rate'<='$threshold' '
            if [ "$csv2es_pid" =  "" ];then
                printf 'pid: empty'

                is_pedning_empty=`ls /toshibaVolume/BISTU-NETWORK-DATA/pending/`

                if [ "$is_pedning_empty" = "" ]; then
                    break
                else :
                    printf '\nrun csv2es_python\n'
#                    nohup csv2es_python /home/hongyu/PycharmProjects/bistu-internet-analysis/csv2es_python/csv2es-entrance.py &
                    python /home/hongyu/PycharmProjects/bistu-internet-analysis/python/csv2es.py
                fi

            else :
                printf 'pid: '$csv2es_pid
            fi
        fi
        sleep 60
        done
