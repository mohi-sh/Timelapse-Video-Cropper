import os
import json

def save(config: dict, config_file_name = None):
   if config_file_name is not None:
      config['config_file_name'] = config_file_name
   with open(config['config_file_name'], 'w') as f:
      json.dump(config, f)

def load(config_file_name):
   with open(config_file_name, 'r') as f:
      config = json.load(f)
   config['config_file_name'] = config_file_name
   return config

def normalize(config: dict, default_config: dict):
   for k,v in default_config.items():
      config[k] = config.get(k, v)

def create_default(default_config: dict):
   config = {}
   normalize(config, default_config)
   save(config)
   print('New config file created.')
   print_config(config)
   return config

def print_file(config_file_name):
   print('Config file located at:\n\t%s\n Current working directory:\n\t%s' % (config_file_name, os.getcwd()))
   print('Current config contents:')
   with open(config_file_name, 'r') as f:
      for line in f:
         print(line)

def print_config(config: dict):
   print_file(config['config_file_name'])
