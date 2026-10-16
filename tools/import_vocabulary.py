"""Import actual upstream list JSON and local pictures without modifying source."""
import argparse,json,shutil,sys
from pathlib import Path

def load_list(file,root):
 d=json.loads(file.read_text(encoding='utf-8-sig')); errors=[]; seen=set()
 if not isinstance(d,dict) or not isinstance(d.get('items'),list): raise ValueError(f'{file}: expected object with items array')
 for i,v in enumerate(d['items']):
  at=f'{file.name}.items[{i}]'
  for k in ['id','word','partOfSpeech','meaning','notes','sourceKey']:
   if not isinstance(v.get(k),str): errors.append(f'{at}.{k}: expected string')
  if v.get('id') in seen: errors.append(f'{at}: duplicate ID {v.get("id")}')
  seen.add(v.get('id'))
  for k,keys in [('ipa',['uk','us']),('example',['en','zh']),('collocation',['en','zh'])]:
   if not isinstance(v.get(k),dict) or any(not isinstance(v[k].get(x),str) for x in keys): errors.append(f'{at}.{k}: invalid bilingual/IPA object')
  if not isinstance(v.get('tags'),list) or any(not isinstance(t,str) for t in v.get('tags',[])): errors.append(f'{at}.tags: expected string array')
  if not isinstance(v.get('images'),list): errors.append(f'{at}.images: expected array'); continue
  for im in v['images']:
   src=im.get('src','') if isinstance(im,dict) else ''
   f=(root/src).resolve()
   if not src or not f.is_relative_to(root.resolve()) or not f.is_file(): errors.append(f'{at}: missing/unsafe image {src}')
 if errors: raise ValueError('\n'.join(errors))
 return d

def run(source,out,lists):
 root=Path(source)/'public'; out=Path(out); out.mkdir(parents=True,exist_ok=True); ids=set()
 for name in lists:
  d=load_list(root/'data'/f'{name}.json',root)
  for v in d['items']:
   if v['id'] in ids: raise ValueError('duplicate ID across lists: '+v['id'])
   ids.add(v['id'])
   for im in v['images']:
    dest=out/im['src']; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/im['src'],dest)
  (out/f'{name}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
  print(f'{name}: {len(d["items"])} senses; {len(set(v["word"] for v in d["items"]))} spellings; {sum(len(v["images"]) for v in d["items"])} pictures')
if __name__=='__main__':
 a=argparse.ArgumentParser(); a.add_argument('source'); a.add_argument('--out',default='app/src/main/assets'); a.add_argument('--lists',nargs='+',default=['list01']); x=a.parse_args()
 try: run(x.source,x.out,x.lists)
 except (ValueError,OSError,KeyError,TypeError) as e: print(str(e),file=sys.stderr); sys.exit(1)
