#!/usr/bin/env python
#  coding=utf-8
#!C:\Python27\python.exe
from builtins import ValueError

from k8s import Connection
from kuby import Kuby
import argparse
from pymongo import MongoClient , InsertOne, DeleteOne, ReplaceOne
import datetime, sys, os
from config import Config
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
class Main():
    data = Config("/k8s/kubelog/kubelog.json")
    client = MongoClient(data.getDados("MONGODB"))
    db = client['k8s']
    collection = db['LOG']
    clusters = collection.find().distinct("ClusterName")
    #Purge all data on collection
    #collection.remove({})
    for cluster in clusters:
        dates = collection.find({"ClusterName":cluster}).distinct("date")
        for date in dates:
            RC=os.path.exists(data.getDados("LOGPATH") + "/" + cluster + "/" + date)
            if RC == False:
                try:
                    print("Path not found, purging records from database: " + data.getDados("LOGPATH") + "/" + cluster + "/" + date)
                    collection.remove({"ClusterName":cluster,"date":date})
                except ValueError:
                    print("Fail to purge old records")

    client.close()
    for cluster in data.getData("KUBESERVER"):
        try:
            k8s = Kuby(cluster["VIP"], cluster["TOKEN"])
            result = k8s.getNamespaces()
            if result == False:
                print("Error")
            else:
                for namespace in result:
                    result = k8s.getNamespacesDetails(namespace)
                    if result == False:
                        print("Error")
                    else:
                        for namespaceDetails in result:

                            # print(namespaceDetails.metadata.uid)
                            # print(namespaceDetails.metadata.name)
                            # print(namespaceDetails.status.phase)
                            # print(namespaceDetails.metadata.resource_version)

                            result = k8s.getPodsOnNamespace(namespaceDetails.metadata.name)
                            if result == False:
                                print("Erro")
                            else:
                                for pod in result:
                                    try:
                                        # print("#####################################")
                                        # print("Pod Name" + pod.name)
                                        # print("Pod uid" + pod.uid)
                                        # print("Pod generate_name" + pod.generate_name)
                                        # print("Pod resource_version" + pod.resource_version)
                                        # print("Pod Namespace " + namespaceDetails.metadata.name)
                                        # print(pod.metadata.uid)
                                        # print(pod.metadata.generate_name)
                                        # print(pod.metadata.resource_version)
                                        result = k8s.getPodContainers(namespaceDetails.metadata.name, pod.name)
                                        if result == False:
                                            print("Error")
                                        else:
                                            for container in result:
                                                result = k8s.getPodLog(namespaceDetails.metadata.name, pod.name,
                                                                       container)
                                                if result == False:
                                                    print("Error")
                                                else:
                                                    size = sys.getsizeof(result)
                                                    print(
                                                        namespaceDetails.metadata.name + " " + namespaceDetails.metadata.uid + " " + pod.name + " " + pod.uid + " " + container)
                                                    file_path = data.getDados("LOGPATH") + "/" + cluster[
                                                        "NAME"] + "/" + now + "/" + namespaceDetails.metadata.name + "/" + namespaceDetails.metadata.uid + "/" + pod.name + "/" + pod.uid + "/" + container + ".log"
                                                    directory = os.path.dirname(file_path)
                                                    try:
                                                        os.stat(directory)
                                                    except:
                                                        os.makedirs(directory)
                                                    file = open(file_path, "w+")
                                                    file.write(result)
                                                    file.close()
                                                    client = MongoClient(data.getDados("MONGODB"))
                                                    db = client['k8s']
                                                    collection = db['LOG']
                                                    LOG = {"namespace": namespaceDetails.metadata.name,
                                                           "namespaceuid": namespaceDetails.metadata.uid,
                                                           "podname": pod.name,
                                                           "poduid": pod.uid,
                                                           "containername": container,
                                                           "date": now,
                                                           "logsizebyte": size,
                                                           "filepath": file_path,
                                                           "ClusterName": cluster["NAME"]
                                                           }
                                                    LOGs = db.LOG

                                                    try:
                                                        LOG_id = LOGs.insert_one(LOG).inserted_id
                                                    except ValueError:
                                                        print("Fail to add record to mongodb")
                                                    print(LOG_id)
                                                    client.close()


                                    except ValueError:
                                        print("Error acquiring log for " + pod.name + "Could not print KeyValue")
                                        print(ValueError)
        except ValueError:
            print("Fail to connect to cluster")
            print(ValueError)