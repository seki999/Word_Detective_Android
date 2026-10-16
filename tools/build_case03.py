"""Bilingual List03 story. Run from repository root; existing catalog entries are preserved."""
import json
from pathlib import Path
steps=[]
def add(id,type,title,en,zh,nums=(),**kw):
 steps.append(dict(id=id,type=type,title=title,en=en,zh=zh,words=[f'v{x:06d}' for x in nums],**kw))
def choices(*items):return [dict(id=i,text=t) for i,t in items]
add('brief','dialogue','01 · 修缮协议失踪',
 'Emma: The campaign to restore Harbour Library has reached a critical evening. A distinguished woman in a dark suit, Councillor Helen Brooks, meets us at the entrance. The signed restoration charter has vanished from the archive desk. A draft lies in its place.',
 'Emma：海港图书馆的修缮活动迎来了关键的一晚。一位身穿深色套装、气度不凡的女士——议员Helen Brooks——在入口迎接我们。签署完毕的修缮协议从档案桌上消失，原处只剩一份草稿。',[102,101],speaker='emma')
add('appeal','dialogue','01 · 修缮的意义',
 'Helen: Residents will campaign for the library to stay open. Damp walls are a prevalent problem in this densely populated district. We want to repair the facade without losing the reading rooms that serve the vicinity.',
 'Helen：居民们将开展活动，争取让图书馆继续开放。在这片人口稠密的地区，墙壁受潮是普遍存在的问题。我们希望修复建筑正面，同时保留服务附近居民的阅览室。',[103,104,134,150,121],speaker='helen')
add('terms','clue','02 · 核实补贴条件',
 'Helen: Our grant agreement requires the signed original by 20:00 tonight to release a $40,000 subsidy. A scanned copy is not a substitute for the original under this agreement. The trustees voted to ratify the charter at 17:30. The vote minutes and the grant terms are now in your evidence folder.',
 'Helen：我们的补贴协议规定，今晚20:00前必须提交签署原件，才能发放40,000美元补贴。按照这份协议，扫描件不能代替原件。理事在17:30投票正式批准了协议。表决记录和补贴条款现已收入你的证物档案。',[127,114,124],clue='terms',speaker='helen')
add('contract','dialogue','02 · 分清罚则的用语',
 'Mara: The exhibit’s sample contract uses several forms of the same word: “A contractor may forfeit its deposit after a serious breach. A separate forfeit of $500 applies to unauthorized removal of documents. In that situation, the deposit is forfeit.” These are this exhibit’s sample terms, not evidence that a breach occurred tonight.',
 'Mara：展览中的合同范本使用了同一个词的几种形式：“承包方严重违约后可能丧失押金。擅自移走文件还另有500美元罚金。在这种情形下，押金将被没收。”这些是本展览的示例条款，并不能证明今晚已经发生违约。',[105,106,107],speaker='mara')
add('obligations','dialogue','02 · 违约与责任',
 'Helen: Owen’s firm would lose its provisional maintenance contract if the new charter took effect. A note warns of default if the firm fails to perform its existing duties. Owen says he will not default on those duties. That financial interest may arouse suspicion, but it does not identify who removed the original.',
 'Helen：如果新协议生效，Owen的公司就会失去临时维护合同。一份备忘录警告，该公司若不履行现有职责，就会构成违约。Owen表示自己不会不履行这些职责。这种经济利益或许会引起怀疑，却不能据此认定是谁拿走了原件。',[109,111,136],speaker='helen')
add('identity','clue','03 · 原件与草稿的区别',
 'Mara: At 17:50 I made the certified archive scan. The identity sheet defines R17 as the signed original: blue serial R17, trustee signatures, and a watermark. D04 is an unsigned grey draft with no watermark. The sheet includes close photographs of both. It never permits staff to substitute a draft for the original.',
 'Mara：17:50，我制作了经过核验的档案扫描件。识别表规定，R17是签署原件，具有蓝色R17编号、理事签名和水印。D04则是没有水印、未签名的灰色草稿。识别表附有两者的近照，绝不允许工作人员用草稿替换原件。',[115],clue='identity',speaker='mara')
add('materials','dialogue','03 · 修复师的说明',
 'Felix: Substitute paper is suitable for practice models, not for official submission. Damp can penetrate ordinary paper, so the original was kept in a dry transparent sleeve. Owen’s firm hopes to penetrate the heritage-maintenance market. That business ambition is background information, not physical proof.',
 'Felix：代用纸适合练习模型，不适合正式提交文件。潮气能渗入普通纸张，因此原件一直放在干燥的透明保护套内。Owen的公司希望打入古建筑维护市场。这种商业抱负只是背景信息，并非实物证据。',[116,130,131],speaker='felix')
add('identity-question','multiple_choice','03 · 识别正式原件',
 'Alex: Use the identity sheet we collected. Which document is the signed original required by the grant agreement?',
 'Alex：请使用我们已经收集的识别表。哪份文件才是补贴协议要求的签署原件？',speaker='alex',requires=['terms','identity'],
 options=choices(('r17','Blue R17, signatures and watermark / 蓝色R17编号、签名与水印'),('d04','Grey D04 with no signatures / 未签名的灰色D04'),('scan','Any printed scan / 任意打印的扫描件'),('model','Practice model on substitute paper / 代用纸制作的练习模型')),answer='r17',hint='将识别表中的R17特征与补贴协议要求的“签署原件”对应起来。')
add('crowd','dialogue','04 · 现场为什么嘈杂',
 'Emma: The launch was tumultuous. A sudden surge of visitors filled the hall, and staff expected numbers to surge again after the evening news. The upsurge in interest explains the noise outside; it does not explain a change of documents inside the archive room.',
 'Emma：启动活动现场十分喧闹。突然激增的访客挤满了大厅，工作人员预计晚间新闻播出后，人数还会再次猛增。关注度的急剧高涨解释了外面的噪声，却解释不了档案室内文件被更换的事实。',[120,123,122,141],speaker='emma')
add('rumors','dialogue','04 · 排除传言',
 'Helen: Posters are ubiquitous, and online rumors can proliferate just as quickly. Our media workshop aims to inoculate volunteers against false claims by teaching them to check sources. We cannot treat an implicit accusation on a poster as proof against Mara.',
 'Helen：海报随处可见，网络传言也能同样迅速地扩散。我们的媒体工作坊教志愿者核实来源，目的是让他们对虚假说法具有抵抗力。我们不能把海报上含蓄的指控当成针对Mara的证据。',[132,133,139,112],speaker='helen')
add('health-exhibit','dialogue','04 · 社区展览的资料',
 'Priya: The library also hosts a public-health history exhibit. One panel describes efforts to inoculate children against disease; another discusses the eradication of smallpox. A glossary explains the terminology. These are educational displays, not instructions for your investigation or a record of tonight’s visitors.',
 'Priya：图书馆还举办公共卫生历史展。一块展板描述给儿童接种疫苗以预防疾病的工作，另一块讨论天花的消灭。术语表解释了专业用语。这些是教育展板，不是调查指令，也不是今晚访客的记录。',[138,149,140],speaker='priya')
add('access','clue','05 · 封存出入记录',
 'Emma: The archive door log records Owen’s personal key O1 entering at 18:10 and leaving at 18:14. No other entry occurred between 17:50 and 18:20. The independent corridor video confirms that he entered alone. Owen had signed for sole possession of O1. The log is corroboration; it does not show which paper he handled.',
 'Emma：档案室门禁日志记录，Owen的个人钥匙O1于18:10进入、18:14离开。17:50至18:20之间没有其他出入记录。独立的走廊录像确认他独自进入，且Owen签字确认独自保管O1。日志是佐证，但并不显示他处理了哪份纸质文件。',clue='access',speaker='emma')
add('security','dialogue','05 · 安保并非结论',
 'Emma: Visible cameras should deter interference. The incident guide says officers may confiscate unauthorized access cards, with a receipt. A safety report says the alarm is loud enough to arouse a sleeping attendant. None of these policies proves that an alarm sounded tonight; the recordings and logs must answer that.',
 'Emma：可见的摄像头应能威慑干扰行为。事件处理指引说，警员可在出具收据后没收未经授权的门禁卡。安全报告说，警报声足以唤醒熟睡的值班员。但这些规定都不能证明今晚警报确实响过；这必须由录像和日志回答。',[117,108,137],speaker='emma')
add('camera','listening','05 · 听取连续录像报告',
 'Emma: The desk camera is continuous and its clock matches the door log. At 18:11, Owen lifts the sheet with blue serial R17 from the tray. At 18:12, he puts grey D04 in that tray. He places R17 inside crate C6, locks the crate, and leaves. Both serials and his face are readable in the original recording.',
 'Emma：桌面摄像机的录像连续完整，时钟与门禁日志一致。18:11，Owen从托盘拿起带蓝色R17编号的文件。18:12，他将灰色D04放进该托盘。随后他把R17装进C6箱子、锁上箱子并离开。原始录像能辨认出两个编号和他的脸。',clue='camera',speaker='emma',requires=['identity','access'],
 options=choices(('swap','Owen replaces R17 with D04. / Owen用D04换走R17。'),('mara','Mara carries R17 away. / Mara拿走R17。'),('blank','The camera stops before 18:11. / 摄像机在18:11前停止。'),('same','R17 remains in the tray. / R17一直在托盘里。')),answer='swap',hint='留意18:11被拿走的编号与18:12被放回的编号，以及操作人。')
add('system','clue','06 · 检查所谓系统故障',
 'Owen: The scanner’s default setting must have replaced the original. Alex: The scanner only makes digital copies; it cannot move paper. The technician’s signed diagnostic report confirms no scanner error or network outage at the relevant time. The alleged system failure does not explain a physical exchange.',
 'Owen：一定是扫描仪的默认设置替换了原件。Alex：扫描仪只生成电子副本，不能搬动纸张。技术员签字的诊断报告确认，相关时段没有扫描仪错误或网络中断。所谓系统故障无法解释实体文件的交换。',[110],clue='system',speaker='alex',requires=['camera'])
add('costs','dialogue','06 · 不急于下结论',
 'Helen: A delay could incur extra storage costs. A careless accusation could incur public anger as well. I once had implicit trust in every contractor. Now I want us to check records without assuming that guilt is inevitable just because someone has a financial motive.',
 'Helen：延误可能带来额外仓储费用，草率指控也可能招致公众不满。我曾经对每位承包商都有绝对的信任。现在，我希望我们核查记录，不要仅因为某人有经济动机，就认定其有罪是必然的。',[118,119,113,135],speaker='helen')
add('support','dialogue','06 · 赞助不等于控制',
 'Felix: Local foundations provide patronage for the restoration. The bookshop next door depends on readers’ patronage. Neither kind of support gives a sponsor the right to hide public records. Owen’s firm has a commercial interest, but the case still depends on the documented exchange.',
 'Felix：本地基金会为修缮提供资助。隔壁书店则依靠读者惠顾。但无论哪一种支持，都不赋予赞助方隐藏公共记录的权利。Owen的公司有商业利益，不过案件仍应依据有记录的文件交换。',[125,126],speaker='felix')
add('reprieve','dialogue','07 · 争取核查时间',
 'Helen: The grant office has issued a written reprieve until 22:00 while we recover the original. Its notice says, “We will reprieve the project from the submission penalty for two hours.” The original must still be produced. This temporary relief does not turn D04 into an acceptable charter.',
 'Helen：补贴办公室已书面给予暂缓，期限延至22:00，让我们追回原件。通知写道：“本项目未及时提交的处罚暂缓两小时执行。”原件仍必须交出。这种暂时解脱不会使D04变成合格的协议。',[128,129],speaker='helen')
add('barriers','dialogue','07 · 修缮的迫切性',
 'Priya: A lack of suitable space is a handicap for our reading groups. Closing the only accessible room would handicap those groups further. Neglect creates a vicious cycle: damage drives readers away, reduced use cuts support, and repairs are postponed again.',
 'Priya：缺少合适场地，是我们阅读小组面临的不利条件。关闭唯一方便使用的房间会进一步妨碍这些小组。疏于维护形成了恶性循环：损坏使读者离开，使用率降低又削弱支持，修缮于是再次推迟。',[142,143,147],speaker='priya')
add('incident','dialogue','07 · 无关的小事故',
 'Emma: An earlier mishap involved a visitor dropping a camera after a vicious dog barked outside. The hall report and video place that event at 16:00, well before the charter was scanned. The dog never entered the archive. A dramatic incident is not automatically a clue to the missing document.',
 'Emma：早些时候发生了一起小意外，一只凶猛的狗在外面吠叫，吓得一位访客掉落了相机。大厅报告和录像将此事定位在16:00，远早于协议被扫描的时间。那只狗从未进入档案室。戏剧性的事件并不自动成为文件失踪的线索。',[148,146],speaker='emma')
add('contest','dialogue','07 · 避免将奖品误当证物',
 'Mara: The library’s photo contest gave a small consolation prize to a young entrant. His family found consolation in seeing his work displayed. The prize envelope was opened on the public stage, not at the archive desk. Its resemblance to a document sleeve is not proof of a connection.',
 'Mara：图书馆的摄影比赛给了一名年轻参赛者一份小小的安慰奖。他的家人因看到作品展出而感到欣慰。奖品信封是在公共舞台上打开的，不是在档案桌上。它与文件保护套相似，不能证明两者有关。',[145,144],speaker='mara')
add('reconstruct','fill_blank','08 · 准确表述动机',
 'Alex: Owen’s firm stood to keep its provisional job if the new project failed. That is motive, not the physical proof. Complete this sentence using the grant terms: The original is required to release the $40,000 ____.',
 'Alex：如果新项目失败，Owen的公司就可能保住临时工作。这是动机，不是实物证据。请根据补贴条款补全句子：提交原件是发放40,000美元____的条件。',[127],speaker='alex',requires=['terms'],answer='subsidy',hint='回看补贴条款，寻找表示“补贴”的名词。')
add('confront','dialogue','08 · 出示已经取得的记录',
 'Alex: You blamed a scanner setting. The continuous video shows a physical exchange by you, and the identity sheet explains why R17 is the original while D04 is only a draft. Owen: I was protecting the documents. Alex: Then why leave the unsigned draft in the original’s submission tray and lock R17 in C6?',
 'Alex：你归咎于扫描仪设置。但连续录像显示你亲手交换了文件，识别表也解释了为何R17是原件、D04仅是草稿。Owen：我是在保护文件。Alex：那为什么把未签名的草稿放在原件提交托盘里，又将R17锁进C6箱子？',speaker='alex',requires=['identity','access','camera','system'])
add('deduce','deduction','09 · 调包证据的最终组合',
 'Alex: Select exactly two records that together establish both which sheet is the signed original and who physically exchanged it for the draft. A deadline or a motive alone cannot establish those facts.',
 'Alex：请选择恰好两份记录，共同证明哪份是签署原件，以及是谁亲手将它换成了草稿。单靠截止时间或动机不能证明这两点。',speaker='alex',requires=['terms','identity','access','camera','system'],
 options=choices(('identity','Original/draft identity sheet / 原件与草稿识别表'),('camera','Continuous desk-camera recording / 连续桌面监控录像'),('terms','Grant deadline and subsidy terms / 补贴截止时间与条款'),('system','Scanner diagnostic report / 扫描仪诊断报告')),answers=['identity','camera'],hint='识别表定义R17/D04各是什么；连续录像记录谁把哪个编号拿走、又放回哪个编号。')
add('recovery','clue','09 · 打开C6并追回原件',
 'Owen: I hid the original to delay the new contract and keep my firm’s maintenance work. Emma: With Owen present, we open C6 and recover R17. Mara checks its serial, signatures, and watermark against the certified scan. Helen receives a signed handover receipt before 22:00. The grant office confirms acceptance of the original.',
 'Owen：我藏起原件，是想拖延新合同，让我的公司继续做维护工作。Emma：在Owen在场时，我们打开C6并追回R17。Mara将编号、签名和水印与核验过的扫描件比对。Helen在22:00前收到签字的交接回执，补贴办公室确认接受了原件。',clue='recovered',speaker='emma')
add('end','ending','10 · 结案报告',
 'The identity sheet distinguished R17 from D04. Continuous video established Owen’s physical substitution; the door log corroborated his access. The diagnostic report refuted his scanner story. His commercial interest explained the motive, but the case rested on records, not rumors. R17 was recovered, authenticated, and submitted within the written extension.',
 '识别表区分了R17与D04。连续录像证实Owen亲手调包，门禁日志佐证其进入档案室。诊断报告推翻了他关于扫描仪的说法。商业利益解释了动机，但案件立足于记录，而非传言。R17已被追回、核验，并在书面延长期内提交。',speaker='emma',requires=['terms','identity','access','camera','system','recovered'])
for i,s in enumerate(steps):s['next']=steps[i+1]['id'] if i+1<len(steps) else None
used=sorted({id for s in steps for id in s['words']})
c=dict(caseId='switched-restoration-charter',schemaVersion=1,title='The Switched Restoration Charter',description='被调包的修缮协议 · List03',vocabularyListId='list03',sceneLabel='HARBOUR LIBRARY · RESTORATION',requiredVocabularyIds=used,characters=[dict(id=i,name=n) for i,n in [('alex','Alex Chen'),('emma','Emma Wilson'),('helen','Helen Brooks'),('mara','Mara Bell'),('felix','Felix Hart'),('priya','Priya Rao'),('owen','Owen Mercer')]],scenes=[],chapters=[dict(id=str(i),title=t) for i,t in enumerate(['失踪的协议','补贴与合同','识别原件','嘈杂现场','安保与录像','检验借口','核查干扰信息','重建事实','最终推理与追回','结案报告'],1)],dialogue=[],questions=[],clues=[dict(id=i,title=n) for i,n in [('terms','补贴条款及批准记录'),('identity','R17原件与D04草稿识别表'),('access','O1出入日志及走廊录像'),('camera','连续桌面监控录像'),('system','扫描仪独立诊断报告'),('recovered','R17核验及提交回执')]],deductions=[],branches=[],endings=['end'],rewards={'xp':len(steps)*10},unlockConditions=[],steps=steps)
a=Path('app/src/main/assets');(a/'case03.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catalog=json.loads((a/'catalog.json').read_text(encoding='utf-8'))
if 'case03.json' not in catalog['cases']:catalog['cases'].append('case03.json')
(a/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8')
print('Case03:',len(steps),'steps;',len(used),'senses; missing:',[f'v{x:06d}' for x in range(101,151) if f'v{x:06d}' not in used])
