#!/usr/bin/python
# -*-coding:utf-8-*-

import sys

from management import action_list
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stark.settings")

import django
django.setup()

from Stark import settings
from management import models



class ArgvManagement(object):
    '''
        接收用户指令 分配到指定的模块
    '''

    def __init__(self,argvs):
        self.argvs = argvs
        self.argv_parse()

    def help_msg(self):
        print(" Acailable modules ")
        for registered_module in action_list.actions:
            print(" %s" %registered_module)
        exit()

    def argv_parse(self):
        print(self.argvs)
        if len(self.argvs) <2:
            self.help_msg()

        module_name = self.argvs[1]

        if '.' in module_name:
            mod_name,module_method = module_name.split('.')
            module_instance = action_list.actions.get(mod_name)
            if module_instance: #matched
                module_obj = module_instance(self.argvs,models,settings)
                module_obj.process()    #提取 主机
                if hasattr(module_obj,module_method):  #解析任务，发送到队列，取任务结果
                    module_method_obj = getattr(module_obj,module_method)
                    module_method_obj()
                else:
                    print("module [%s] doesn't have [%s] method " % (mod_name,module_method))


        else:
            exit("invalid module name argument ")