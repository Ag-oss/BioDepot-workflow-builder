import json
import logging
import pickle
from base64 import b64decode
from threading import Lock
from typing import Dict, List
from uuid import uuid4, uuid5
import sys
import requests
from requests import get
from flask import Flask, jsonify, request, Response, stream_with_context

class ResourceHostObject:
    @property
    def host_id(self):
        return self.__host_id__

    @property
    def host_name(self):
        return self.__host_name__

    @property
    def host_port(self):
        return self.__host_port__

    @property
    def redis_host(self):
        return self.__redis_host__

    @property
    def redis_port(self):
        return self.__redis_port__

    @property
    def total_memory(self):
        return self.__total_memory__

    @property
    def total_cores(self):
        return self.__total_cores__

    @property
    def used_memory(self):
        return int(self.__available_memory__ * 100 / self.__total_memory__)

    @property
    def used_cores(self):
        return int(self.__available_cores__ * 100 / self.__total_cores__)

    def __init__(self, host_id, host_name, host_port, redis_host, redis_port, total_memory, total_cores):
        self.__lock__ = Lock()
        self.__host_id__ = host_id
        self.__host_name__ = host_name
        self.__host_port__ = host_port
        self.__redis_host__ = redis_host
        self.__redis_port__ = redis_port
        self.__total_memory__ = total_memory
        self.__total_cores__ = total_cores
        self.__available_memory__ = total_memory
        self.__available_cores__ = total_cores

    def use_resources(self, required_memory, required_cores):
        with self.__lock__:
            if self.__available_memory__ - required_memory >= 0 and self.__available_cores__ + required_cores >= 0:
                self.__available_memory__ -= required_memory
                self.__available_cores__ -= required_cores
                return True
            else:
                return False

    def free_resources(self, required_memory, required_cores):
        with self.__lock__:
            self.__available_memory__ = max(self.__total_memory__, self.__available_memory__ + required_memory)
            self.__available_cores__ = max(self.__total_cores__, self.__available_cores__ + required_cores)

    def to_object(self):
        return {'id': self.host_id, 'host_name': self.host_name, 'host_port': self.host_port,
                'used_memory': self.used_memory, 'used_cores': self.used_cores}

    def __repr__(self):
        return json.dumps(self.to_object())
        
class JobUnit:
    def __init__(self,job_id):
        self.hosts=[]
        self.job_id=job_id
    def add_host(self, host):
        self.hosts.append(host)
        

class HostRegistry:
    __SERVICE_HOST_ID__ = uuid4()
    __LOCK__ = Lock()
    __RESOURCES__: Dict[str, ResourceHostObject] = {}

    @staticmethod
    def register_resource(host_name, host_port, redis_host, redis_port, core_count, memory):
        resource_host_id = str(uuid5(HostRegistry.__SERVICE_HOST_ID__, "%s:%d" % (host_name, host_port)))
        resource_host_obj = ResourceHostObject(host_id=resource_host_id, host_name=host_name, host_port=host_port,
                                               total_cores=core_count, total_memory=memory, redis_host=redis_host,
                                               redis_port=redis_port)
        with HostRegistry.__LOCK__:
            HostRegistry.__RESOURCES__[resource_host_id] = resource_host_obj
            return {'id': resource_host_id}

    @staticmethod
    def get_available_host(core_count, memory, maxWorkers, job_id) -> List[ResourceHostObject]:
        job_unit=JobUnit(job_id)
        nhosts=0
        with HostRegistry.__LOCK__:
            for resource_host_obj in HostRegistry.__RESOURCES__.values():
                while nhosts < maxWorkers and resource_host_obj.use_resources(required_cores=core_count, required_memory=memory):
                    job_unit.add_host(resource_host_obj)
                    nhosts=nhosts+1
        return job_unit

    @staticmethod
    def run_command(host, command_queue_id, redis_host, redis_port, job_id, worker_id):
        host_name = host.host_name
        host_port = host.host_port
        uri = "http://%s:%s/run_command" % (host_name, host_port)
        data=json.dumps(
            {'command_queue_id': command_queue_id, 'redis_host': redis_host, 'redis_port': redis_port, 'job_id': job_id, 'worker_id': worker_id })
        r = requests.post(uri, data)
        try:
            response = r.json()
            if r.status_code != 200:
                error = b64decode(response['error'].encode())
                raise RuntimeError(error)
        except Exception as e:
            logging.exception(e)
            raise RuntimeError("Failed to parse response")

    @staticmethod
    def status(host, container_name):
        host_name = host.host_name
        host_port = host.host_port
        uri = "http://%s:%s/status" % (host_name, host_port)
        r = requests.get(uri, params={'container_name': container_name})
        try:
            response = r.json()
        except Exception as e:
            logging.exception(e)
            raise RuntimeError("Failed to parse response")
        if r.status_code != 200:
            error = b64decode(response['error'].encode())
            raise RuntimeError(error)
        status_code = json.loads(b64decode(response['output'].encode()).decode())
        return status_code

    @staticmethod
    def log(job_id,worker_id=0):
        if worker_id:
            r=get('http://logger/logs/name:{}.{}'.format(job_id,worker_id),stream=True)
        else:
            r=get('http://logger/logs/name:{}*'.format(job_id),stream=True)
        return Response(r.iter_content(chunk_size=10*1024),
                    content_type=r.headers['Content-Type'])

