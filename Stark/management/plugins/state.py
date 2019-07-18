#!/usr/bin/python
# -*-coding:utf-8-*-

import os


from management.backends.base_module import BaseSaltModule

class State(BaseSaltModule):

   def load_state_files(self,state_filename):
      from yaml import load,dump
      try:
         from yaml import CLoader as Loader,CDumper as Dumper
      except ImportError:
         from yaml import Loader,Dumper

      state_file_path = "%s/%s" %(self.settings.SALT_CONFIG_FILES_DIR,state_filename)
      if  os.path.isfile(state_file_path):
            with open(state_file_path) as f:
               data = load(f.read(),Loader=Loader)

               return data
      else:
         exit("%s is not a vaild yaml config file " % state_filename)





   def apply(self):
      '''
      1. load the configations file
      2.parse it
      3.create a task and snet it to the MQ
      4.collect the result with task-callback id
      '''

      if '-f' in self.sys_argvs:
         yaml_file_index = self.sys_argvs.index('-f') + 1
         try:
            yaml_file_name = self.sys_argvs[yaml_file_index]
            state_data = self.load_state_files(yaml_file_name)
            #print('-->state data:',state_data)

            for os_type,os_type_data in self.config_data_dic.items():  #按照不同的操作系统，生成单独的一份配置文件
               for section_name,section_data in state_data.items():
                  #print("Section:",section_name)

                  for mod_name,mod_data in section_data.items():
                     base_mod_name = mod_name.split(".")[0]
                     plugins_file_path = "%s/%s.py" %(self.settings.SALT_PLUGINS_DIR,base_mod_name.capitalize())
                     if os.path.isfile(plugins_file_path):

                        modle_plugins = __import__('plugins.%s' %base_mod_name)
                        special_os_module_name = "%s%s" %(os_type.capitalize(),base_mod_name)
                        #getattr(modle_plugins,base_mod_name)
                        module_file = getattr(modle_plugins,base_mod_name)   #导入模块

                        if hasattr(module_file,special_os_module_name):  #判断有没有根据操作系统的类型进行特殊解析的类，在这个文件里
                           module_instance = getattr(module_file,special_os_module_name)
                        else:
                           module_instance = getattr(module_file,base_mod_name.capitalize())

                        # 开始调用 此module 进行配置解析
                        module_obj= module_instance(self.sys_argvs,self.db_models,self.settings)
                        module_obj.syntax_patser(section_name,mod_name,mod_data)

                     else:
                        exit("module [%s] is not exist" % base_mod_name)
                     #print(" ",mod_name )
                     #for state_item in mod_data:
                     #   print('\t',state_item)

         except ImportError as e:
            exit("state file must be provided after -f ")

      else:
         exit("state file must be specified ")
