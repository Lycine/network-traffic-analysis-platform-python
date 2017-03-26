# -*- coding: utf-8 -*-
import json
import sys
import time
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from csv2es_python.helper import convert_time

from csv2es_python.helper import speak

from csv2es_python.helper import check_pending_task

from csv2es_python.helper import send_email

from csv2es_python.helper import mv_pending2finished

from csv2es_python.helper import mapping

from csv2es_python.helper import PENDING_DIR

ES_INDEX = "bistu-internet-data-"
ES_TYPE = "network-metadata"
ES_USERNAME = "elastic"
ES_PASSWORD = "changeme"
ES_HOSTNAME = "localhost"
ES_PORT = "9200"

IS_MUTE = False

AVERAGE_SPEED = 4100

IS_CONTINUE = True

REMAIN_TASK = "null"

actionsSize = 16000
# actionsSize = 2000

realErrorRate = 0.0

taskFailure = False
errorRate = 0.05


# def show_status():
#     end = time.clock()
#     global AVERAGE_SPEED
#     AVERAGE_SPEED = round(count / (end - START_TIME), 2)
#     print '\r\r\r',
#     print(
#         'used time: %s' % convert_time((end - START_TIME)) +
#         ', aErrCont: ' + str(totalErrorCount) +
#         ', tErrCont: ' + str(taskErrorCount) +
#         ', ErrRate: ' + str(realErrorRate) +
#         ', speed: ' + str(round(count / (end - START_TIME), 2)) + 'r/s' +
#         ', cont/all: ' + str(count) + '/' + str(total) +
#         ', eta: ' + convert_time(round((total - count) / (count / (end - START_TIME)), 0)) +
#         ', fin: ' + str(round((count + 0.0) / total * 100, 2)) + '%' +
#         ', now: ' + str(time.strftime('%H:%M:%S', time.localtime(time.time())))),


speak("launch script", IS_MUTE)
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
    es = Elasticsearch(
        [
            'http://' + ES_USERNAME + ':' + ES_PASSWORD + '@' + ES_HOSTNAME + ':' + ES_PORT + '/'
        ],
        verify_certs=True,
    )
    d = es.indices.stats(index='bistu-internet-data-2016080517')
    json.load()
    print d['_all']['total']['docs']['count']
    # actions = []
    # totalErrorCount = 0
    # while IS_CONTINUE:
    #     if not taskFailure:
    #         next_task = check_pending_task()
    #     if next_task.strip(" ").strip("\n") == "":
    #         IS_CONTINUE = False
    #         break
    #     next_task_array = next_task.split("-")[0:4]
    #     next_task_path = PENDING_DIR + next_task
    #     index_suffix = ""
    #     for part in next_task_array:
    #         index_suffix += part
    #     temp_index = ES_INDEX + index_suffix
    #     print "index: " + temp_index
    #     taskErrorCount = 0
    #     es = Elasticsearch(
    #         [
    #             'http://' + ES_USERNAME + ':' + ES_PASSWORD + '@' + ES_HOSTNAME + ':' + ES_PORT + '/'
    #         ],
    #         verify_certs=True,
    #     )
    #     es.cluster.health(wait_for_status='yellow', request_timeout=60)
    #     if es.indices.exists(index=temp_index):
    #         print "delete old index"
    #         es.indices.delete(index=temp_index)
    #     es.indices.create(index=temp_index, body=mapping)
    #     es.indices.refresh(index=temp_index)
    #     START_TIME = time.clock()
    #     count = 0
    #     speak("new task begin", IS_MUTE)
    #     next_task_path = next_task_path.strip('\n')
    #     print "Running file:" + next_task_path
    #     lines = open(next_task_path, 'rb').readlines()
    #     total = len(lines)
    #     print "Total rows: " + str(total)
    #     content = next_task + " start! <br>eta: " + str(convert_time(int(total / AVERAGE_SPEED)))
    #     send_email(content)
    #     source_file = open(next_task_path, 'rb')
    #     for line in source_file:
    #         count += 1
    #         realErrorRate = (0.0 + taskErrorCount) * actionsSize / total
    #         if realErrorRate > errorRate:
    #             taskFailure = True
    #             print next_task + " failure"
    #             content = next_task + " failure! <br>taskErrorCount: " + str(taskErrorCount)
    #             subject = "csv2es task failure"
    #             send_email(content, subject=subject)
    #             break
    #         try:
    #             line = line.split(',')
    #             action = {
    #                 "_index": temp_index,
    #                 "_type": ES_TYPE,
    #                 "_id": count,
    #                 "_source": {
    #                     "source_ip": line[0],
    #                     "destination_ip": line[1],
    #                     "sourceTransportPort": str(line[2]),
    #                     "destinationTransportPort": str(line[3]),
    #                     "flowStartSeconds": datetime.fromtimestamp(int(line[4]) + 0.0),
    #                     "flowEndSecond": datetime.fromtimestamp(int(line[5]) + 0.0),
    #                     "applicationProtocolName": str(line[6]),
    #                     "applicationName": str(line[7]),
    #                     "applicationCategoryName": str(line[8]),
    #                     "applicationSubCategoryName": str(line[9]),
    #                     "http_method": str(line[10]),
    #                     "status": str(line[11]),
    #                     "http_hostname": str(line[12]),
    #                     "http_referer": str(line[13]),
    #                     "httpRequestLabelNum": line[14],
    #                     "httpReplyLabelNum": str(line[15]),
    #                     "httpRequestVersion": str(line[16]),
    #                     "httpReplyVersion": str(line[17]),
    #                     "fileName": str(line[18]),
    #                     "fileEncrypt": str(line[19]),
    #                     "fileType": str(line[20]),
    #                     "fileSize": str(line[21]),
    #                     "fileMd5": str(line[22]),
    #                     "DNSReplyCode": line[23],
    #                     "DNSQueryName": str(line[24]),
    #                     "DNSDelay": str(line[25]),
    #                     "DNSReplyIPv4": str(line[26]),
    #                     "SrcArea": str(line[28]),
    #                     "DestArea": str(line[29]),
    #                     "SrcIPUser": str(line[30]),
    #                     "DestIPUser": str(line[31]),
    #                     "SrcGeographyLocationCountryOrRegion": str(line[32]),
    #                     "SrcGeographyLocationCity": str(line[33]),
    #                     "SrcGeographyLocationLatitudeLongitude": str(line[35]) + ", " + str(line[34]),
    #                     "DestGeographyLocationCountryOrRegion": str(line[36]),
    #                     "DestGeographyLocationCity": str(line[37]),
    #                     "DestGeographyLocationLatitudeLongitude": str(line[39]) + ", " + str(line[38])
    #                 }
    #             }
    #             actions.append(action)
    #         except Exception, e:
    #             print e
    #         if len(actions) == actionsSize:
    #             try:
    #                 for ok, info in helpers.parallel_bulk(es, actions=actions, thread_count=8, chunk_size=40000,
    #                                                       max_chunk_bytes=8 * 100 * 100 * 1024):
    #                 # for ok, info in helpers.parallel_bulk(es, actions=actions):
    #                     if not ok:
    #                         print('A document failed:', info)
    #             except Exception, e:
    #                 print e
    #                 totalErrorCount += 1
    #                 taskErrorCount += 1
    #             del actions[0:len(actions)]
    #             show_status()
    #
    #     if len(actions) > 0:
    #         for ok, info in helpers.parallel_bulk(es, actions=actions, thread_count=8, chunk_size=40000,
    #                                               max_chunk_bytes=8 * 100 * 100 * 1024):
    #         # for ok, info in helpers.parallel_bulk(es, actions=actions):
    #             if not ok:
    #                 print('A document failed:', info)
    #         del actions[0:len(actions)]
    #         source_file.close()
    #         show_status()
    #     source_file.close()
    #     if not taskFailure:
    #         speak("task complete", IS_MUTE)
    #         content = next_task + " complete! <br>Remain task: " + str(REMAIN_TASK)
    #         send_email(content)
    #         mv_pending2finished(filename=next_task_path)
    #         IS_CONTINUE = False
    #     print " "
    #     time.sleep(1)
    # del es
    # # speak("All task complete", IS_MUTE)
    # # print "All task complete"
    # # subject = "csv2es所有任务已完成"
    # # send_email(content="All task complete", subject=subject)

except Exception, e:
    # subject = "csv2es运行出现错误"
    # content = "Something wrong: <br>" + str(e)
    # send_email(content=content, subject=subject)
    print e
