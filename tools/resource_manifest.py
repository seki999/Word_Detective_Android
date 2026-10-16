import json,hashlib
from pathlib import Path
assets=Path('app/src/main/assets');items=[w for file in sorted(assets.glob('list*.json')) for w in json.loads(file.read_text(encoding='utf-8'))['items']]
lines=['# 本地资源清单','','来源：https://github.com/seki999/toeic-visual-vocabulary','源commit：a73abcc51131f1e221464df499d77ca94465115f','导入：public/data/list01.json、list02.json、list03.json及images[].src对应的public文件。源仓库只读，未修改。','','正式剧情插画：未提供。界面明确显示占位卡，不将词汇例句图片作为案件现场实证。人物肖像待制作。','图标：本工程本地VectorDrawable放大镜与宝石。','','| 词条ID | 本地assets路径 | SHA-256 |','|---|---|---|']
for w in items:
 for im in w['images']:lines.append(f'| {w["id"]} | {im["src"]} | {hashlib.sha256((assets/im["src"]).read_bytes()).hexdigest()} |')
Path('docs/resources.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
