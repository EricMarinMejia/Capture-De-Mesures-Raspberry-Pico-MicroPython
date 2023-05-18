import unittest
import moduleMesure as mod
import datetime
from time import sleep


class Tester(unittest.TestCase):
    def test_egalite(self):
        date = datetime.datetime.now()
        dateStr = date.strftime("%c")
        objet1 = mod.Mesure(dateStr, "test1", 30, "distance")
        objet2 = mod.Mesure(dateStr, "test1", 30, "distance")
        
        self.assertTrue(objet1.dateHeureMesure == objet2.dateHeureMesure)
        #self.assertEqual(objet1, objet2)
    
    def test_inegalite(self):
        date = datetime.datetime.now()
        dateStr = date.strftime("%c")
        objet1 = mod.Mesure(dateStr, "test1", 30, "distance")
        
        sleep(1)
        
        date2 = datetime.datetime.now()
        dateStr2 = date2.strftime("%c")
        objet2 = mod.Mesure(dateStr2, "test1", 30, "distance")
        
        print(objet1.dateHeureMesure)
        print(objet2.dateHeureMesure)
        
        self.assertFalse(objet1.dateHeureMesure == objet2.dateHeureMesure)
        
if __name__ == "__main__":
    unittest.main()
        