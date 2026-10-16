# Word Detective / 英语侦探

Kotlin原生Android离线侦探学习游戏，当前版本 **0.3.0**。Android Studio可直接打开根目录。

## 三个可玩案件

| 案件 | 词汇 | 流程 | 剧情词义覆盖 |
|---|---|---|---|
| The Missing Sapphire / 消失的蓝宝石 | List01 | 12步案件切片 | 3/50，剩余47个尚未融入剧情 |
| The Missing Relief Fund / 失踪的救助款 | List02 | 10章、24步，6份证物 | 50/50，包含调查资料中的词义 |
| The Switched Restoration Charter / 被调包的修缮协议 | List03 | 10章、26步，6份证物 | 50/50，包含调查资料中的词义 |

List01有50个独立词义、31种拼写；List02有50个独立词义、33种拼写；List03有50个独立词义、32种拼写。共150个词义和150张WebP图片全部随APK打包，不按相同拼写合并。完整保留原始JSON中的IPA、英语/中文例句、多个图片、tags、notes和sourceKey。

## 当前功能

- Compose Material 3主菜单、三案件选择、调查地图、双语剧情、取证、听力、四选一、填空、证据组合、结案星级、证物背包、图鉴、每日复习及设置。
- 图鉴和复习可切换List01/List02/List03，切换栏支持横向滚动。剧情中的“本段词汇”展开原始词卡，可朗读和自评。
- 听力题默认隐藏原文；提供系统离线TTS与可选文字模式。词条自评和互动题错误进入独立ID的复习池；仅阅读剧情不会被自动当成答对题。
- Room存储三案件进度、证据、结案、XP、词义复习和设置。切案相互隔离，重玩已读步骤不重复奖励XP；主菜单显示三案累计XP。
- 兼容0.1旧存档：首次读取将旧`progress`归入Case01，写入`campaign`；旧记录仍保留。不改Room表结构，不使用破坏性迁移。0.2的campaign载荷无需改写即可加入Case03；APK versionCode现为3。
- 手机上下布局、宽屏剧情左右布局、长文字滚动、系统字号、可关闭常亮、可清空再输入的语速设置。

内容入口是`app/src/main/assets/catalog.json`。每个案件声明自己的vocabularyListId、sceneLabel和步骤hint，界面不再硬编码第一案的提示。

## 构建

JDK17；Android SDK35；Gradle8.9；AGP8.7.3；Kotlin1.9.24；Compose compiler1.5.14；Room2.6.1。运行支持Android10/API29起。

首次构建需联网下载开发依赖；运行不需要网络，清单未申请INTERNET权限。系统TTS需预先安装离线英语/中文包，缺少时可读文字。

```powershell
# 配置local.properties中的sdk.dir，或设置ANDROID_HOME
.\gradlew.bat assembleDebug testDebugUnitTest lintDebug assembleDebugAndroidTest
python tools/validate_content.py
python -m unittest discover -s tools -p 'test_*.py'
# 或
.\tools\build.ps1 -Python '你的Python3路径'
```

APK：`app/build/outputs/apk/debug/app-debug.apk`。升级安装：`adb install -r app/build/outputs/apk/debug/app-debug.apk`，需保持同一签名。

Release：`./gradlew assembleRelease`生成未签名包；使用Android Studio的Generate Signed Bundle / APK及本地私有keystore签名。保持applicationId与原签名一致；不要提交密钥或密码。

## 导入与验证

```powershell
git clone https://github.com/seki999/toeic-visual-vocabulary.git ../vocabulary-source
python tools/import_vocabulary.py ../vocabulary-source --lists list01 list02 list03
python tools/validate_content.py
python tools/resource_manifest.py
```

导入器只读源仓库public目录，不修改Web项目。`images[].src`对应`file:///android_asset/images/...`，逐一验证字段、类型、重复ID、图片存在及路径安全。支持未来新增List；新案件还需加入catalog.json。

验证器检查全部目录案件、跨List重复ID、角色/词汇/答案引用、证据前置、循环、结局可达性，并输出逐词义报告：

- [List01覆盖](docs/coverage.md)、[List02覆盖](docs/coverage-list02.md)、[List03覆盖](docs/coverage-list03.md)
- [Schema](docs/case.schema.json)、[状态机与多案件存档](docs/content.md)
- [资源来源与哈希](docs/resources.md)、[复习调度](docs/review.md)
- [交付状态与待验证项](docs/status.md)

CI执行资源验证、Python/JVM测试、Lint、Debug APK和设备测试APK编译，上传APK及报告。设备测试是否执行会单独说明。

## 尚未实现

后台/锁屏持续播放、通知与耳机控制、音频焦点、多角色音色/音高编辑、整案循环、图片选择界面、剧情分支、正式插画与肖像、连续学习/任务/成就，以及List01剩余剧情覆盖。当前前台外会暂停朗读，场景卡明确标注占位。
