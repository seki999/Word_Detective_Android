# JSON案件内容与状态机 v1

`case.schema.json` 定义内容结构，schemaVersion固定为1。基础资源数组保留扩展位置；当前执行器读取steps，未实现的branches不得写成已支持功能。

起点为steps首项。每步包含id、type、title、en、zh、next（末步为null）；speaker引用characters，words引用独立词条ID，clue引用clues。requires要求证据集合已收集。

| 类型 | 输入/完成条件 | 下一状态 |
|---|---|---|
| dialogue | 用户阅读后继续 | next |
| vocabulary | 显示words指定的本地词卡后继续 | next |
| multiple_choice / listening | 从4个options选择answer | 正确next，错误原地重试 |
| fill_blank | 忽略大小写、首尾空格匹配answer | 正确next，错误原地重试 |
| clue | 用户确认记录证据 | 将clue加入集合后next |
| deduction | 所选ID集合与answers严格相等，且满足requires | 正确next，错误原地重试 |
| ending | 用户确认结案 | finished=true并保存 |
| image_choice | 预留类型，当前没有专用图片选项渲染器 | 尚未实现 |

错误会增加mistakes，绑定的words写入强化池。星级：0错3星、1–2错2星、更多1星；与词汇掌握度分离。首次完成每步10XP，重玩同一步0XP。rewards字段为未来扩展，当前计分按步骤；不宣称可配置奖励已完成。

Room保存step、证据、完成步骤集合、错误数、XP及finished。重玩清空本轮证据和错误，保留已读集合与既有XP。当前顺序推进，不支持地图任意跳转；已读内容可直接继续。

validate_content.py检查引用有效性、正确答案ID、重复ID、主线路径循环、未到达步骤/结局、证据前置时序。Schema为编辑器结构文档；运行Python验证器无需第三方包，不是通用JSON Schema解释器。

首案逻辑：只有经理持有的M1在21:10打开完好展柜，同步录像显示Robert在展柜旁；照片佐证21:12携袋离开，检验证明展柜留下的是玻璃。最终问题限定“21:10身处展柜旁”，避免照片也成为同等正确答案。Robert供述后实际追回蓝宝石才结案。

## 0.2多案件扩展

catalog.json以cases数组列出案件文件。每案以vocabularyListId绑定词汇列表，sceneLabel提供场景名，Step.hint提供针对该题的提示。List02所有词义均在剧情及调查资料中明确引用；原始学习例句保留在词卡，不当成案件事实。

campaign为Room Stored表中的一个JSON快照：activeCaseId记录当前案件，saves以caseId保存Progress，避免相同step ID在切换时串档。所有案件都可直接开始。两个案件的XP分别累计、主菜单求和；复习仍以全局独立wordId保存，同拼写不同词义不合并。

首次0.2启动优先读取campaign，若不存在则将旧progress归入missing-sapphire；Case02保持新档。旧progress不删除，已存在campaign时不再次覆盖。没有Room表结构变化，schema仍为v1；这是应用存档载荷的兼容读取，并非虚构的数据库DDL迁移。

本次增加步骤词汇自评，只有互动答题和用户明确自评会更新掌握度，阅读剧情不自动被计作答题正确。听力默认隐藏原文，玩家可主动展开进入文字模式。

第二案逻辑：入账凭证排除捐款迟到；银行转账记录确认收款公司，认证的公司登记确认Victor控制该收款方；独占令牌与同步校时的现场照片确认其参与并推翻离场说法。最终组合题明确要求“收款去向”与“法律控制人”两个维度，因此正确组合是银行转账记录与公司登记，照片不与它们同等正确。追回记录先收集，再允许结案。

## 0.3第三案

catalog新增case03.json，绑定list03。campaign和Room表结构保持不变，第三案仅新增以switched-restoration-charter为键的独立Progress；旧案的同名步骤不会串档。累计XP为所有案件之和。

第三案中的补贴、合同和安保条款均为虚构案件内的文件内容，不能当作实际法规。关于医疗、合同等难以自然融入核心证据的词义，放在社区图书馆展览和背景资料里，不将其伪装成可定罪的证据。

核心推理：识别表定义R17为带签名/水印的正式原件，D04为未签名草稿；连续录像显示Owen将R17装进C6并在托盘放回D04。门禁佐证独自进入，诊断报告排除系统故障借口。最终组合要求“文件身份”与“物理交换人”，故识别表+连续录像为唯一正确组合；补贴期限或系统正常不能替代这两点。原件追回、核验与正式接收完成后才能结案。
