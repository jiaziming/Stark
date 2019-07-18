#!/usr/bin/python
# -*-coding:utf-8-*-

import os,sys



def main():
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stark.settings')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(BASE_DIR)
    sys.path.append(BASE_DIR)
    from management.action_list import actions
    from management.backends.utils import ArgvManagement
    obj = ArgvManagement(sys.argv)

if __name__ == '__main__':
    main()