"""Validate packaged content, graph, references and produce honest story coverage."""
import json,sys
from pathlib import Path
from import_vocabulary import load_list
ASSETS=Path('app/src/main/assets')
TYPES={'dialogue','vocabulary','multiple_choice','listening','image_choice','fill_blank','clue','deduction','ending'}
def validate(c,words,assets=ASSETS):
 errors=[]
 def err(s): errors.append(s)
 if c.get('schemaVersion')!=1: err('unsupported schemaVersion')
 steps=c.get('steps',[]); ids=[s.get('id') for s in steps]
 if len(ids)!=len(set(ids)): err('duplicate step ID')
 if not steps: return ['no steps']
 chars=[x['id'] for x in c.get('characters',[])]; clues=[x['id'] for x in c.get('clues',[])]
 if len(chars)!=len(set(chars)):err('duplicate character ID')
 if len(clues)!=len(set(clues)):err('duplicate clue ID')
 for id in c.get('requiredVocabularyIds',[]):
  if id not in words:err('missing vocabulary '+id)
 for s in steps:
  at=s['id']
  if s.get('type') not in TYPES:err(at+': invalid type')
  if not all(isinstance(s.get(k),str) and s[k] for k in ['title','en','zh']):err(at+': missing bilingual text')
  if s.get('speaker','emma') not in chars:err(at+': missing character')
  if s.get('next') is not None and s['next'] not in ids:err(at+': missing next')
  for w in s.get('words',[]):
   if w not in words:err(at+': missing word '+w)
  if s.get('clue') and s['clue'] not in clues:err(at+': unknown clue')
  for x in s.get('requires',[]):
   if x not in clues:err(at+': unknown required clue')
  opts=[x['id'] for x in s.get('options',[])]
  if len(opts)!=len(set(opts)):err(at+': duplicate answer ID')
  if s['type'] in ['multiple_choice','listening','image_choice']:
   if len(opts)!=4 or s.get('answer') not in opts:err(at+': answer absent or not four choices')
  if s['type']=='fill_blank' and not s.get('answer'):err(at+': missing fill answer')
  if s['type']=='deduction' and (not s.get('answers') or not set(s['answers'])<=set(opts)):err(at+': invalid deduction answers')
 visited=set();collected=set();cur=steps[0]['id'];by={s['id']:s for s in steps}
 while cur in by:
  if cur in visited:err('unreasonable story cycle at '+cur);break
  visited.add(cur);s=by[cur]
  if not set(s.get('requires',[]))<=collected:err(cur+': clue needed before collection')
  if s.get('clue'):collected.add(s['clue'])
  cur=s.get('next')
 for s in steps:
  if s['id'] not in visited:err('unreachable step/ending '+s['id'])
 if not any(s['type']=='ending' and s['id'] in visited for s in steps):err('unreachable ending')
 return errors

def main():
 catalog=json.loads((ASSETS/'catalog.json').read_text(encoding='utf-8'))
 files=catalog.get('cases',[])
 if not files or len(files)!=len(set(files)):raise ValueError('empty/duplicate case catalog')
 if set(files)!={p.name for p in ASSETS.glob('case*.json')}:raise ValueError('catalog must include every packaged case')
 all_words=set();case_ids=set();lists={}
 for filename in files:
  if Path(filename).name!=filename:raise ValueError('unsafe catalog path')
  c=json.loads((ASSETS/filename).read_text(encoding='utf-8'))
  if c['caseId'] in case_ids:raise ValueError('duplicate case ID '+c['caseId'])
  case_ids.add(c['caseId']);list_id=c['vocabularyListId']
  if Path(list_id).name!=list_id:raise ValueError('unsafe list ID')
  if list_id not in lists:
   d=load_list(ASSETS/f'{list_id}.json',ASSETS)
   if d['id']!=list_id:raise ValueError('list ID mismatch')
   words={w['id']:w for w in d['items']}
   if all_words & words.keys():raise ValueError('duplicate word IDs across lists')
   all_words.update(words);lists[list_id]=words
  words=lists[list_id];errors=validate(c,words)
  used={w for step in c['steps'] for w in step.get('words',[])}
  if used!=set(c['requiredVocabularyIds']):errors.append('requiredVocabularyIds differs from actual step references')
  if errors:raise ValueError(filename+': '+chr(10).join(errors))
  coverage={id:[step['id'] for step in c['steps'] if id in step.get('words',[])] for id in words}
  covered=sum(bool(v) for v in coverage.values())
  image_count=sum(len(w['images']) for w in words.values())
  missing_images=[id for id,w in words.items() if not w['images']]
  lines=[f'# {list_id.title()} 剧情词汇覆盖报告','',f'案件：{c["title"]}（{c["caseId"]}）',f'词义/独立ID：{len(words)}；不同拼写：{len(set(w["word"] for w in words.values()))}。',f'剧情已覆盖：{covered}；未覆盖：{len(words)-covered}。图鉴不单独计入剧情覆盖。',f'本地图片：{image_count}张，所有图片引用已检查；缺图词条：{", ".join(missing_images) or "无"}。','覆盖由步骤引用ID统计，表中保留独立词义；同拼写不同词义需要结合双语剧情人工审校。','','| ID | 单词与独立词义 | 剧情步骤 |','|---|---|---|']
  lines += [f'| {id} | {w["word"]} · {w["meaning"]} | {", ".join(coverage[id]) or "未覆盖"} |' for id,w in words.items()]
  output='docs/coverage.md' if list_id=='list01' else f'docs/coverage-{list_id}.md'
  Path(output).write_text(chr(10).join(lines)+chr(10),encoding='utf-8')
  print(f'PASS {filename}/{list_id}: {len(c["steps"])} steps; {len(words)} senses; story coverage {covered}/{len(words)}; {image_count} local pictures')
 print(f'PASS catalog: {len(case_ids)} cases; {len(lists)} lists; {len(all_words)} unique sense IDs')
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,TypeError,OSError) as e:print(e,file=sys.stderr);sys.exit(1)
