"""Author the bilingual List02 case; all evidence is fictional, bundled game content."""
import json
from pathlib import Path
steps=[]
def add(id,type,title,en,zh,nums=(),**kw):
 steps.append(dict(id=id,type=type,title=title,en=en,zh=zh,words=[f'v{x:06d}' for x in nums],**kw))
def options(*pairs):return [dict(id=i,text=t) for i,t in pairs]
add('brief','dialogue','01 · 义演后的求助',
 'Emma: A municipal clinic held a benefit concert at Civic Hall. Its distinguished guest, Dr. Patel, helped solicit donations for families. The treasurer says the event raised $24,000, but only $18,000 remains. Alex, help us trace the missing $6,000.',
 'Emma：一家市立诊所在市民礼堂举办了慈善义演。著名嘉宾Patel医生帮助募集善款。财务负责人说活动筹得24,000美元，但现在只剩18,000美元。Alex，请帮我们追查失踪的6,000美元。', [90,100,79],speaker='emma')
add('mission','dialogue','01 · 查账前先厘清事实',
 'Alex: Altruism brought the donors here, but good intentions are not proof of honest bookkeeping. A facile explanation such as “the bank must be slow” is not enough. We need a reconciliation of the donor register, bank statement, and ledger.',
 'Alex：利他之心让捐款人聚集于此，但善意不能证明账目诚实。“银行一定处理得慢”这种肤浅的解释并不足够。我们需要核对捐款登记簿、银行流水和分类账，使三者一致。',[60,56,51],speaker='alex')
add('beneficiaries','dialogue','02 · 诊所的项目说明',
 'Dr. Patel: The fund will repair ventilation in our clinic after a sewage leak. It also supports children with congenital heart conditions. One patient described the exquisite pain she felt before treatment. These details explain the appeal; none identifies a thief.',
 'Patel医生：这笔资金将用于污水泄漏后诊所通风系统的维修，也会帮助患有先天性心脏病的儿童。一名患者描述了治疗前感受到的剧痛。这些资料说明募款的用途，并不能据此认定谁是窃贼。',[91,82,74,86],speaker='patel')
add('medical-note','dialogue','02 · 医疗资料的边界',
 'Dr. Patel: A teaching poster discusses pulmonary congestion in a clinical case; it is unrelated to the traffic delay outside. Another poster asks why some people are immune to certain infections. Patient privacy is important. No patient records are needed for this financial inquiry.',
 'Patel医生：一张教学海报在一个临床病例中讨论了肺淤血；它与外面的交通延误无关。另一张海报提出，为什么一些人对某些感染具有免疫力。患者隐私很重要，这次财务调查不需要患者病历。',[77,98],speaker='patel')
add('charter','dialogue','02 · 章程与志愿者',
 'Nora: I am the director-designate, so I have not taken office yet. The old charter uses formal language: “The trustees ordain that relief money be used only for clinic work.” I am a congenital optimist, but even I insist that a charity must never be immune from scrutiny.',
 'Nora：我是已获任命但尚未就职的主任。旧章程用了正式措辞：“理事规定，救助款只能用于诊所工作。”我向来是个乐观主义者，但即便如此，我也坚持慈善机构绝不能免于审查。',[59,54,75,99],speaker='nora')
add('volunteer','dialogue','02 · 志愿者的背景资料',
 'Nora: One volunteer is preparing a church ceremony. “Our bishop will ordain two deacons next week,” he told me. He had no access to our accounts. Please do not mistake an unfamiliar occupation for evidence of wrongdoing.',
 'Nora：一名志愿者正在筹备教会仪式。他对我说：“我们的主教下周将授予两位执事圣职。”他没有访问我们账目的权限。请不要把不熟悉的职业误当成违法证据。',[53],speaker='nora')
add('stage','dialogue','03 · 舞台与活动记录',
 'Mateo: Tonight was singer Iris Lane’s debut. A versatile musician, she can sing and play three instruments. Her facile piano playing made the difficult passage sound effortless. A youth ensemble will debut its new work here next month.',
 'Mateo：今晚是歌手Iris Lane的首次亮相。她是一位多才多艺的音乐人，能唱歌，还能演奏三种乐器。她流畅自如的钢琴演奏使那段困难的乐句听起来毫不费力。一支青年乐团下个月将在这里首次演出他们的新作品。',[80,89,57,81],speaker='mateo')
add('auction','dialogue','03 · 拍卖清单',
 'Lena: The auction catalogue lists a signed football jersey and a scarf made from soft jersey fabric. An exquisite silver brooch has a small blemish on its clasp. Its intrinsic value lies in its craftsmanship, not in the fame of the donor. All auction proceeds are already included in the $24,000 total.',
 'Lena：拍卖目录列有一件签名足球球衣和一条柔软针织面料制成的围巾。一枚精美的银胸针在搭扣处有个小瑕疵。它的内在价值在于工艺，而非捐赠者的名气。所有拍卖款都已计入24,000美元的总额。',[61,62,85,72,65],speaker='lena')
add('publicity','dialogue','03 · 宣传资料',
 'Emma: The event manager chose to tout the concert as the season’s highlight. Outside, a ticket tout offered seats at inflated prices. The poster promised to solicit suggestions from residents about future events. None of this accounts for money already received by the bank.',
 'Emma：活动经理将这场音乐会大力宣传为本季的亮点。外面，一名黄牛以高价兜售座位。海报承诺向居民征求今后活动的建议。这些情况都无法解释银行已经收到的款项为何减少。',[63,64,78],speaker='emma')
add('register','clue','04 · 核对收入来源',
 'Emma: The sealed donor register totals $24,000. The bank statement confirms all $24,000 arrived. There were no pending deposits. This rules out the suggestion that delayed incoming payments caused the $6,000 gap.',
 'Emma：封存的捐款登记簿合计24,000美元。银行流水确认24,000美元全部到账，没有待处理的入账。这排除了“入账延迟造成6,000美元差额”的说法。',clue='income',speaker='emma')
add('ledger','clue','04 · 一笔不寻常的转账',
 'Emma: The ledger labels a $6,000 payment at 21:14 as “donor refund.” The authenticated bank statement instead names BrightStage Services as the recipient. BrightStage is not listed as a donor. Nora did not authorize a purchase from that company.',
 'Emma：分类账把21:14的一笔6,000美元付款标为“捐款人退款”。经过核验的银行流水却将收款方列为BrightStage Services。BrightStage不在捐款人名单上，Nora也没有批准向该公司采购。',clue='transfer',speaker='emma')
add('bank-question','multiple_choice','04 · 判断已知事实',
 'Alex: The full $24,000 arrived, and $6,000 then went to BrightStage. Which explanation is directly contradicted by the bank record?',
 'Alex：24,000美元全部到账，之后有6,000美元转给了BrightStage。哪种解释被银行记录直接否定？',speaker='alex',requires=['income','transfer'],
 options=options(('late','Some donations have not arrived. / 有些捐款尚未到账。'),('outgoing','An outgoing transfer reduced the balance. / 一笔转出使余额减少。'),('received','The bank received $24,000. / 银行收到24,000美元。'),('recipient','BrightStage received $6,000. / BrightStage收到6,000美元。')),answer='late',hint='区分尚未入账的收入与已经发生的支出。银行确认24,000美元全部到账。')
add('permissions','clue','05 · 谁能操作账户',
 'Nora: Our policy is to designate one payment officer. This month that officer is Victor Shaw, the treasurer. The signed access register says only Victor holds token V7. It cannot be shared remotely. The terminal log records his token and personal PIN approving the 21:14 transfer.',
 'Nora：我们的规定是指定一名付款负责人。本月的负责人是财务主管Victor Shaw。签字确认的权限登记表显示，只有Victor持有令牌V7，且不能远程共享。终端日志记录了他的令牌和个人密码批准21:14转账的操作。',[58],clue='token',speaker='nora')
add('witness','listening','05 · 听取摄影师证词',
 'Lena: I value punctuality, so I arrived at 21:00 despite the traffic congestion. At 21:14 I took a candid photograph through the open office door. It clearly shows Victor at the payment terminal. The terminal clock and my camera clock were checked against the same hall clock.',
 'Lena：我重视守时，因此尽管交通拥堵，仍在21:00到达。21:14，我透过敞开的办公室门抓拍了一张照片，清楚拍到了付款终端前的Victor。终端时钟和我的相机时钟都已与同一座礼堂时钟核对。',[55,76,67],clue='photo',speaker='lena',requires=['token'],
 options=options(('victor','Victor was at the terminal at 21:14. / Victor在21:14位于终端前。'),('mateo','Mateo approved the transfer. / Mateo批准了转账。'),('refund','Lena received a donor refund. / Lena收到了捐款退款。'),('left','Victor left before 21:00. / Victor在21:00之前离开。')),answer='victor',hint='留意Lena报出的21:14，以及她照片中出现的人。')
add('statement','dialogue','06 · 财务主管的说法',
 'Victor: Let me be candid: I left at 21:00. I was oblivious to any later transfer. Alex: That conflicts with the photograph and token log. Please do not allude to unnamed volunteers; give us a specific explanation.',
 'Victor：我坦率地说，我21:00就离开了。我完全不知道之后的任何转账。Alex：这与你的照片和令牌日志矛盾。请不要影射没有姓名的志愿者，请给出具体解释。',[66,88,71],speaker='victor',requires=['token','photo'])
add('ownership','clue','06 · 查明收款公司',
 'Emma: A certified company extract shows that BrightStage is a wholly owned subsidiary of Shaw Events, and Victor is Shaw Events’ sole owner. The extract predates the concert. The charity has no contract or unpaid invoice with either company.',
 'Emma：经认证的公司登记摘录显示，BrightStage是Shaw Events的全资子公司，而Victor是Shaw Events的唯一所有者。该摘录形成于音乐会之前。慈善机构与这两家公司都没有合同或未付发票。',[92],clue='ownership',speaker='emma')
add('distractions','dialogue','07 · 排除无关损坏',
 'Mateo: A peripheral device, the receipt printer, failed earlier. A subsidiary report discusses that repair. The printer fault is peripheral to the transfer: the bank’s independent record is intact. We should not let a broken printer distract us from the money trail.',
 'Mateo：一台计算机外设——收据打印机——早先出了故障。一份附属报告讨论了这项维修。打印机故障对于转账只是次要问题，银行的独立记录完好。我们不应让坏掉的打印机分散追查资金去向的注意力。',[95,93,94],speaker='mateo')
add('report','dialogue','07 · 不能以文风定罪',
 'Emma: Some paragraphs in the public report match last year’s text. The editor admits, “I chose to plagiarize the old introduction.” Copying may blemish the charity’s reputation, but it does not prove who transferred the money. The payment evidence must stand on its own.',
 'Emma：公开报告的某些段落与去年的文本相同。编辑承认：“我选择抄袭了旧的引言。”抄袭可能损害慈善机构的声誉，却不能证明是谁转走了钱。付款证据必须独立成立。',[52,73],speaker='emma')
add('impact','dialogue','07 · 回到受损的援助',
 'Dr. Patel: Delayed repairs can inflict hardship on families and deprive patients of a suitable place for care. The bank has offered to compensate the charity if its investigation establishes liability. Extra volunteer hours may compensate for some disruption, but they cannot replace the missing cash.',
 'Patel医生：维修延误可能使家庭遭受困难，并剥夺患者获得合适照护场所的机会。银行表示，若调查确认其承担责任，将赔偿慈善机构。增加志愿服务时间或许能弥补部分干扰，却不能取代失踪的现金。',[83,84,96,97],speaker='patel')
add('method','fill_blank','08 · 重建付款路径',
 'Alex: We do not need an ingenious theory about stolen cash. The records show an electronic transfer to a company Victor controls. BrightStage is a wholly owned ____ of Shaw Events.',
 'Alex：我们不需要编造巧妙的现金失窃理论。记录显示，款项被电子转账至Victor控制的公司。BrightStage是Shaw Events的全资____。',[87,92],speaker='alex',answer='subsidiary',requires=['transfer','ownership'],hint='查看公司登记摘录：BrightStage与Shaw Events是子公司关系。')
add('confront','dialogue','08 · 与财务主管对质',
 'Alex: Music can beguile an audience, but a misleading label must not beguile the committee. Victor: It was a legitimate expense. Alex: There is no authorized contract or unpaid invoice. A label cannot change the bank’s named recipient.',
 'Alex：音乐可以迷住观众，但一个误导性的标签不能欺骗委员会。Victor：那是一笔合法开支。Alex：没有经过授权的合同，也没有未付的发票。标签改变不了银行记录中的收款方。',[69,70],speaker='victor',requires=['transfer','token','photo','ownership'])
add('deduce','deduction','09 · 资金去向的最终推理',
 'Alex: Select exactly two documents: one identifies where the $6,000 was sent, and the other establishes who legally controls that recipient. We have already collected both.',
 'Alex：请选择恰好两份文件：一份确认6,000美元汇往何处，另一份确认谁在法律上控制该收款方。这两份文件我们都已经收集。',speaker='alex',requires=['transfer','ownership','token','photo'],
 options=options(('transfer','Authenticated bank transfer / 经核验的银行转账记录'),('ownership','Certified ownership extract / 经认证的公司所有权摘录'),('photo','Lena’s photograph / Lena的照片'),('income','Donor income register / 捐款收入登记簿')),answers=['transfer','ownership'],hint='照片说明谁在现场，收入登记说明收到多少；题目要求的是收款去向和公司所有权。')
add('recovery','clue','09 · 追回捐款',
 'Victor: I will capitulate. I moved the money to my company without permission and called it a refund. Emma: With Victor’s written authorization, the bank has returned the full $6,000. The new statement confirms the charity again holds $24,000. This is recovery of funds, not a promise of future repayment.',
 'Victor：我认输了。我未经许可把钱转到自己的公司，还把它称为退款。Emma：依据Victor的书面授权，银行已将6,000美元全额转回。新流水确认慈善机构再次持有24,000美元。这是已经追回的资金，而不是将来还钱的承诺。',[68],clue='recovered',speaker='emma')
add('end','ending','10 · 结案报告',
 'The bank record traced the missing funds to BrightStage. The ownership extract linked that company to Victor. His exclusive token and Lena’s photograph established his involvement and refuted his departure claim. The complete incoming deposit ruled out delayed donations. The $6,000 has been recovered; the clinic’s repairs can proceed.',
 '银行记录追踪到失踪款项进入BrightStage，公司所有权摘录证明该公司与Victor的关系。他独占的令牌和Lena的照片证实了他的参与，并推翻了其已经离开的说法。完整入账记录排除了捐款延迟到账的解释。6,000美元已被追回，诊所维修可以继续。',requires=['income','transfer','token','photo','ownership','recovered'],speaker='emma')
for i,s in enumerate(steps):s['next']=steps[i+1]['id'] if i+1<len(steps) else None
used=sorted({w for s in steps for w in s['words']})
case=dict(caseId='missing-relief-fund',schemaVersion=1,title='The Missing Relief Fund',description='失踪的救助款 · List02',vocabularyListId='list02',requiredVocabularyIds=used,sceneLabel='CIVIC HALL · BENEFIT CONCERT',characters=[dict(id=i,name=n) for i,n in [('alex','Alex Chen'),('emma','Emma Wilson'),('patel','Dr. Patel'),('nora','Nora Ellis'),('mateo','Mateo Ruiz'),('lena','Lena Park'),('victor','Victor Shaw')]],scenes=[],chapters=[dict(id=str(i),title=t) for i,t in enumerate(['义演后的求助','诊所与志愿者','活动记录','核对账目','操作权限与证词','追查收款公司','排除干扰','嫌疑人对质','最终推理与追回','结案报告'],1)],dialogue=[],questions=[],clues=[dict(id=i,title=n) for i,n in [('income','捐款登记与全额入账确认'),('transfer','21:14银行转账记录'),('token','V7令牌权限与终端日志'),('photo','Lena的21:14抓拍照片'),('ownership','BrightStage公司所有权摘录'),('recovered','6,000美元转回确认')]],deductions=[],branches=[],endings=['end'],rewards={'xp':len(steps)*10},unlockConditions=[],steps=steps)
Path('app/src/main/assets/case02.json').write_text(json.dumps(case,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catalog_path=Path('app/src/main/assets/catalog.json')
catalog=json.loads(catalog_path.read_text(encoding='utf-8')) if catalog_path.exists() else {'cases':['case01.json']}
if 'case02.json' not in catalog['cases']:catalog['cases'].append('case02.json')
catalog_path.write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8')
print('Case02:',len(steps),'steps;',len(used),'independent senses; missing:',[f'v{x:06d}' for x in range(51,101) if f'v{x:06d}' not in used])
