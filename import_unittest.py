import unittest
import individual
import family
class marriage_before_divorce(unittest.TestCase):
  def marriage_before_divorce(self):
    self.assertTrue(family.Marriagebeforedivorce(datetime(2008,11,22).date(),datetime(2010,11,22).date()))
    self.assertEqual(family.Marriagebeforedivorce(datetime(2008,11,22).date(),datetime(2008,11,22).date()))
    self.assertIsInstance(family.Marriagebeforedivorce(datetime(2008,11,22).date(),datetime(2008,11,22).date()))
    with self.assertRaises(Exception):
      family.Marriagebedoredeath(datetime(2008,11,22).date(),datetime(2010,11,22).date())
    self.asserIsNone(family.Marriagebedoredeath(None,datetime(2010,11,22).date()))
class child_birthdate(unittest.TestCase):
    def child_birthdate(self):
        self.assertTrue(family.clidernbdate(datetime(2008,11,22).date(),datetime(2010,11,22).date()))
        self.assertEqual(family.clidernbdate(datetime(2008,11,22).date(),datetime(2010,11,22).date()))
        self.assertIsInstance(family.clidernbdate(datetime(2008,11,22).date(),datetime(2010,11,22).date()))
        with self.assertRaises(Exception):
            family.clidernbdate(datetime(2008,11,22).date(),datetime(2010,11,22).date())
if __name__ == '__main__':
  unittest.main(argv=['first-arg-is-ignored'], exit=False)