import json,re,unittest
from validate_content import ASSETS,validate
from import_vocabulary import load_list

class List03Tests(unittest.TestCase):
 def setUp(self):
  self.case=json.loads((ASSETS/'case03.json').read_text(encoding='utf-8'))
  self.words={w['id']:w for w in load_list(ASSETS/'list03.json',ASSETS)['items']}
 def test_valid_case03(self):self.assertEqual([],validate(self.case,self.words))
 def test_exact_fifty_independent_ids(self):
  self.assertEqual({f'v{x:06d}' for x in range(101,151)},set(self.words))
  self.assertEqual(32,len({w['word'] for w in self.words.values()}))
 def test_every_sense_appears_in_linked_english_context(self):
  self.assertEqual(set(self.words),set(self.case['requiredVocabularyIds']))
  for id,w in self.words.items():
   occurrences=[s for s in self.case['steps'] if id in s.get('words',[])]
   self.assertTrue(occurrences,id)
   self.assertTrue(any(re.search(r'\b'+re.escape(w['word'])+r'\b',s['en'],re.I) for s in occurrences),id)
 def test_all_fifty_images_local_and_present(self):
  images=[im for w in self.words.values() for im in w['images']]
  self.assertEqual(50,len(images))
  self.assertTrue(all(im['src'].startswith('images/list03/') and (ASSETS/im['src']).is_file() for im in images))
 def test_prior_distinguished_sense_is_not_merged(self):
  prior=json.loads((ASSETS/'list02.json').read_text(encoding='utf-8'))['items'][-1]
  current=self.words['v000101'];self.assertEqual(prior['word'],current['word'])
  self.assertNotEqual(prior['id'],current['id']);self.assertNotEqual(prior['meaning'],current['meaning'])
 def test_deduction_requires_collected_identity_and_video(self):
  s=next(s for s in self.case['steps'] if s['type']=='deduction')
  self.assertEqual({'identity','camera'},set(s['answers']))
  self.assertTrue(set(s['answers'])<=set(s['requires']))
 def test_identity_before_listening(self):
  s=next(s for s in self.case['steps'] if s['type']=='listening');self.assertIn('identity',s['requires'])
  self.case['steps'][0]['requires']=['identity'];self.assertTrue(validate(self.case,self.words))
 def test_invalid_listening_answer_is_rejected(self):
  next(s for s in self.case['steps'] if s['type']=='listening')['answer']='none'
  self.assertTrue(validate(self.case,self.words))
 def test_recovery_must_precede_ending(self):
  self.assertIn('recovered',self.case['steps'][-1]['requires'])
  next(s for s in self.case['steps'] if s['id']=='recovery').pop('clue')
  self.assertTrue(validate(self.case,self.words))
 def test_wrong_case_clue_is_rejected(self):
  self.case['steps'][0]['requires']=['ownership'];self.assertTrue(validate(self.case,self.words))
 def test_all_interactive_steps_have_specific_hints(self):
  for s in self.case['steps']:
   if s['type'] in {'multiple_choice','listening','fill_blank','deduction'}:self.assertTrue(s.get('hint'),s['id'])
 def test_catalog_covers_three_lists(self):
  catalog=json.loads((ASSETS/'catalog.json').read_text(encoding='utf-8'))
  self.assertEqual(3,len(catalog['cases']))
  self.assertEqual({'list01','list02','list03'},{json.loads((ASSETS/f).read_text(encoding='utf-8'))['vocabularyListId'] for f in catalog['cases']})
if __name__=='__main__':unittest.main()
