import copy,json,tempfile,unittest
from pathlib import Path
from validate_content import validate,ASSETS
from import_vocabulary import load_list
class ContentTests(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ASSETS/'case01.json').read_text(encoding='utf-8'));self.words={x['id'] for x in json.loads((ASSETS/'list01.json').read_text(encoding='utf-8'))['items']}
 def test_valid(self): self.assertEqual([],validate(self.c,self.words))
 def test_duplicate(self): self.c['steps'][1]['id']='brief';self.assertTrue(validate(self.c,self.words))
 def test_word(self): self.c['steps'][0]['words']=['none'];self.assertTrue(validate(self.c,self.words))
 def test_character(self): self.c['steps'][0]['speaker']='none';self.assertTrue(validate(self.c,self.words))
 def test_answer(self): self.c['steps'][4]['answer']='none';self.assertTrue(validate(self.c,self.words))
 def test_cycle(self): self.c['steps'][-1]['next']='brief';self.assertTrue(validate(self.c,self.words))
 def test_unreachable(self): self.c['steps'][0]['next']=None;self.assertTrue(validate(self.c,self.words))
 def test_early_clue(self): self.c['steps'][0]['requires']=['glass'];self.assertTrue(validate(self.c,self.words))
 def test_invalid_json(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'bad.json';p.write_text('{')
   with self.assertRaises(ValueError):load_list(p,Path(t))
 def test_missing_picture(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaisesRegex(ValueError,'missing/unsafe image'):load_list(ASSETS/'list01.json',Path(t))
if __name__=='__main__': unittest.main()
