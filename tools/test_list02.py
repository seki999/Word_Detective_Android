import json,re,unittest
from pathlib import Path
from validate_content import validate,ASSETS
from import_vocabulary import load_list

class List02Tests(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ASSETS/'case02.json').read_text(encoding='utf-8'))
  self.words={w['id']:w for w in load_list(ASSETS/'list02.json',ASSETS)['items']}
 def test_valid_case02(self):self.assertEqual([],validate(self.c,self.words))
 def test_all_50_ids_have_actual_english_occurrences(self):
  self.assertEqual(50,len(self.words))
  for id,w in self.words.items():
   occurrences=[s for s in self.c['steps'] if id in s.get('words',[])]
   self.assertTrue(occurrences,id)
   self.assertTrue(any(re.search(r'\b'+re.escape(w['word'])+r'\b',s['en'],re.I) for s in occurrences),id)
 def test_two_lists_never_merge_shared_spelling(self):
  first=json.loads((ASSETS/'list01.json').read_text(encoding='utf-8'))['items']
  first_ids={w['id'] for w in first};self.assertFalse(first_ids & self.words.keys())
  self.assertEqual('reconciliation',self.words['v000051']['word'])
  self.assertNotEqual(first[-1]['meaning'],self.words['v000051']['meaning'])
 def test_invalid_final_answer(self):
  next(s for s in self.c['steps'] if s['type']=='deduction')['answers']=['not-an-option']
  self.assertTrue(validate(self.c,self.words))
 def test_invalid_listening_answer(self):
  next(s for s in self.c['steps'] if s['type']=='listening')['answer']='not-an-option'
  self.assertTrue(validate(self.c,self.words))
 def test_requires_uncollected_evidence(self):
  self.c['steps'][0]['requires']=['ownership'];self.assertTrue(validate(self.c,self.words))
 def test_final_deduction_has_explicit_required_sources(self):
  s=next(s for s in self.c['steps'] if s['type']=='deduction')
  self.assertEqual({'transfer','ownership'},set(s['answers']))
  self.assertTrue(set(s['answers'])<=set(s['requires']))
 def test_end_cannot_skip_recovery(self):
  self.assertIn('recovered',self.c['steps'][-1]['requires'])
  next(s for s in self.c['steps'] if s['id']=='recovery').pop('clue')
  self.assertTrue(validate(self.c,self.words))
 def test_missing_step_is_rejected(self):
  self.c['steps'][0]['next']='does-not-exist';self.assertTrue(validate(self.c,self.words))
 def test_catalog_has_both_cases_and_matching_lists(self):
  files=json.loads((ASSETS/'catalog.json').read_text(encoding='utf-8'))['cases']
  self.assertTrue({'case01.json','case02.json'}<=set(files))
  self.assertTrue({'list01','list02'}<={json.loads((ASSETS/f).read_text(encoding='utf-8'))['vocabularyListId'] for f in files})
if __name__=='__main__':unittest.main()
