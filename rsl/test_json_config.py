import os
import unittest
import json_config

k1, v1 = 'config_file_name', 'test_json_config_config.json'
k2, v2 = 'string_value', 'this is a string'
k3, v3 = 'int_value', 123
k4, v4 = 'boolean_value', False

default_config = {
   k1: v1,
   k2: v2,
   k3: v3,
   k4: v4
   }

v2_2 = 'some other string'
v3_2 = -560

class Test_test1 (unittest.TestCase):

   def assert_config_file_exists(self):
      self.assertTrue(os.path.exists(default_config[k1]))

   def assert_custom_config_file_exists(self, custom_filename):
      self.assertTrue(os.path.exists(custom_filename))

   def assert_config_file_doesnt_exist(self):
      self.assertFalse(os.path.exists(default_config[k1]))

   def clean_up(self):
      if os.path.exists(default_config[k1]):
         os.remove(default_config[k1])
      self.assert_config_file_doesnt_exist()

   def clean_up_custom_filename(self, custom_filename):
      if os.path.exists(custom_filename):
         os.remove(custom_filename)

   def tearDown(self):
      self.clean_up()
      return super().tearDown()

   def test_create_default(self):
      self.clean_up()
      config = json_config.create_default(default_config)
      self.assert_config_file_exists()
      self.assertTrue(config[k1] == default_config[k1])
      self.assertTrue(config[k2] == v2)
      self.assertTrue(config[k3] == default_config[k3])
      self.assertTrue(config[k3] == v3)
      self.assertFalse(config[k4])
      config[k4] = True
      self.assertTrue(config[k4])
      self.assertFalse(config[k4] == default_config[k4])

   def test_normalize(self):
      partial_config = {
            k2: v2_2
         }
      self.assertTrue(partial_config.get(k1) is None)
      self.assertTrue(partial_config[k2] == v2_2)
      self.assertTrue(default_config[k2] == v2)
      self.assertFalse(v2 == v2_2)
      json_config.normalize(partial_config, default_config)
      self.assertFalse(v2 == v2_2)
      self.assertTrue(partial_config[k1] == v1)
      self.assertTrue(partial_config[k2] == v2_2)
      self.assertTrue(partial_config[k3] == v3)
      self.assertTrue(partial_config[k4] == v4)

   def assert_saved(self, config):
      self.assertFalse(config[k2] == default_config[k2])
      self.assertTrue(config[k2] == v2_2)
      self.assertFalse(config[k3] == default_config[k3])
      self.assertTrue(config[k3] == v3_2)
      self.assertTrue(config.get(k4) is None)

   def assert_saved_1(self, config):
      self.assertTrue(config[k1] == default_config[k1])
      self.assert_saved(config)

   def assert_saved_2(self, config, custom_filename):
      self.assertTrue(config[k1] == custom_filename)
      self.assert_saved(config)

   def test_save_1(self):
      self.clean_up()
      partial_config = {
         k1: v1,
         k2: v2_2,
         k3: v3_2}
      self.assert_saved_1(partial_config)
      json_config.save(partial_config)
      self.assert_config_file_exists()
      self.assert_saved_1(partial_config)

   def test_load_1(self):
      self.test_save_1()
      config = json_config.load(default_config[k1])
      self.assert_saved_1(config)

   def test_save_2(self):
      self.clean_up()
      custom_filename = 'custom_' + v1
      self.clean_up_custom_filename(custom_filename)
      partial_config = {
         k1: v1,
         k2: v2_2,
         k3: v3_2}
      self.assert_saved_1(partial_config)
      json_config.save(partial_config, config_file_name = custom_filename)
      self.assert_custom_config_file_exists(custom_filename)
      self.assert_saved_2(partial_config, custom_filename)

if __name__ == '__main__':
    unittest.main()
