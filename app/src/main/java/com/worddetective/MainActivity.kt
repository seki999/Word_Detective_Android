package com.worddetective

import android.os.Bundle
import android.view.WindowManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.layout.ContentScale
import coil.compose.AsyncImage

class MainActivity:ComponentActivity(){
 private val vm:GameModel by viewModels()
 private lateinit var speech:Speech
 override fun onCreate(savedInstanceState:Bundle?){super.onCreate(savedInstanceState);speech=Speech(this)
  setContent{MaterialTheme(colorScheme=darkColorScheme(primary=Color(0xFFE4BD70),background=Color(0xFF091624),surface=Color(0xFF132638))){Surface(Modifier.fillMaxSize()){Detective(vm,speech){keep->if(keep)window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON) else window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)}}}}
 }
 override fun onStop(){super.onStop();speech.pause()}
 override fun onDestroy(){speech.close();super.onDestroy()}
}
@Composable fun Detective(vm:GameModel,speech:Speech,keep:(Boolean)->Unit){
 val campaign by vm.campaign.collectAsState(); val p=campaign.progressFor(vm.case); val reviews by vm.reviews.collectAsState();val settings by vm.settings.collectAsState();val ready by vm.ready.collectAsState()
 var page by remember{mutableStateOf("home")}
 var selectedList by remember(vm.case.caseId){mutableStateOf(vm.case.vocabularyListId)}
 LaunchedEffect(settings){speech.englishRate=settings["en"]?.toFloatOrNull()?:0.8f;speech.chineseRate=settings["zh"]?.toFloatOrNull()?:1.2f;keep(settings["keep"]=="true")}
 LaunchedEffect(page){speech.stop()}
 Column(Modifier.fillMaxSize().statusBarsPadding().navigationBarsPadding()){
  Row(Modifier.fillMaxWidth().padding(16.dp),horizontalArrangement=Arrangement.SpaceBetween){Text("WORD DETECTIVE",fontWeight=FontWeight.Bold,color=MaterialTheme.colorScheme.primary);if(page!="home")TextButton(onClick={page="home"}){Text("主菜单")}}
  if(!ready){Text("正在读取本地档案…",Modifier.padding(24.dp));return@Column}
  when(page){
   "home" -> Column(Modifier.verticalScroll(rememberScrollState()).padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)){
    Text("英语侦探",fontSize=36.sp,fontWeight=FontWeight.Bold);Text(vm.case.sceneLabel,color=MaterialTheme.colorScheme.primary)
    ScenePlaceholder(vm.case.sceneLabel)
    Text(vm.case.title,fontSize=24.sp);Text(vm.case.description)
    Text("离线案件切片 · 阅读、聆听、取证与推理")
    Text("总XP ${vm.totalXp}  ·  等级 ${vm.totalXp/100+1}  ·  当前案件 ${p.completed.size}/${vm.case.steps.size}")
    Button(onClick={page="cases"},modifier=Modifier.fillMaxWidth()){Text("打开案件档案")}
    listOf("map" to "调查地图 / 继续游戏","bag" to "证物背包","lexicon" to "词汇图鉴 / 离线学习","review" to "每日复习","settings" to "设置").forEach{(id,label)->OutlinedButton(onClick={page=id},modifier=Modifier.fillMaxWidth().testTag("nav-$id")){Text(label)}}
   }
   "cases" -> LazyColumn(Modifier.padding(horizontal=24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)) {
    item { Text("案件档案",fontSize=28.sp);Text("各案件分别保存进度、证物和结案成绩。") }
    items(vm.cases,key={it.caseId}) { c ->
     val saved=campaign.progressFor(c)
     Card(Modifier.fillMaxWidth()) { Column(Modifier.padding(20.dp),verticalArrangement=Arrangement.spacedBy(12.dp)) {
      Text(c.title,fontSize=25.sp);Text(c.description)
      Text("${c.steps.size}个步骤 · ${c.requiredVocabularyIds.size}/${vm.wordLists.getValue(c.vocabularyListId).size}个剧情词义")
      Text("已读 ${saved.completed.size}/${c.steps.size} · 案件XP ${saved.xp}")
      Button(onClick={speech.stop();vm.selectCase(c.caseId);page="game"},modifier=Modifier.testTag("open-${c.caseId}")){Text(if(saved.finished)"查看结案报告" else "开始 / 继续调查")}
      OutlinedButton(onClick={speech.stop();vm.selectCase(c.caseId);vm.replay();page="game"}){Text("重玩案件（保留已获XP与词汇记录）")}
     } }
    }
    item { Spacer(Modifier.height(16.dp)) }
   }
   "map" -> LazyColumn(Modifier.padding(horizontal=24.dp)){item{Text("案件地图",fontSize=28.sp);Text("按顺序调查，证据在取得后才能用于推理。")};items(vm.case.steps){s->Card(Modifier.fillMaxWidth().padding(vertical=6.dp)){Column(Modifier.padding(16.dp)){Text(s.title);Text(if(s.id in p.completed)"已完成" else if(s.id==p.step)"当前调查" else "待解锁");if(s.id==p.step)TextButton(onClick={page="game"}){Text("进入")}}}}}
   "game" -> GameScreen(vm,speech)
   "bag" -> LazyColumn(Modifier.padding(24.dp)){item{Text("证物背包",fontSize=28.sp);if(p.clues.isEmpty())Text("尚未取得证物。请先调查现场。")};items(vm.case.steps.filter{it.clue in p.clues}){s->Card(Modifier.fillMaxWidth().padding(vertical=8.dp)){Column(Modifier.padding(16.dp)){Text(vm.case.clues.first{it.id==s.clue}.title,fontWeight=FontWeight.Bold);Text("来源：${s.title}");Text(s.en);Text(s.zh)}}}}
   "lexicon","review" -> {
    val selectedWords=vm.wordLists.getValue(selectedList)
    val list=if(page=="lexicon")selectedWords else selectedWords.filter{(reviews[it.id]?.nextReviewAt?:Long.MAX_VALUE)<=System.currentTimeMillis()||reviews[it.id]?.masteryLevel=="需要强化"}
    LazyColumn(Modifier.padding(horizontal=24.dp),verticalArrangement=Arrangement.spacedBy(12.dp)){
     item{
      Text(if(page=="lexicon")"词汇图鉴 · ${list.size}个词义" else "每日复习 · ${list.size}词",fontSize=26.sp)
      Row(Modifier.horizontalScroll(rememberScrollState())) { vm.wordLists.keys.forEach { id -> TextButton(onClick={speech.stop();selectedList=id},modifier=Modifier.testTag("words-$id")){Text("${if(selectedList==id)"● " else ""}${id.replace("list","List ")}")} } }
      if(list.isEmpty())Text("本List目前没有到期复习。可以先在图鉴学习单词。")
     }
     items(list,key={it.id}){w->Card{Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)){WordCard(w,speech);Text("${w.id} · ${reviews[w.id]?.masteryLevel?:"新词"}");Row{TextButton(onClick={vm.grade(w.id,false)}){Text("需要强化")};TextButton(onClick={vm.grade(w.id,true)}){Text("记住了")}}}}}
    }
   }
   "settings" -> Column(Modifier.verticalScroll(rememberScrollState()).padding(24.dp),verticalArrangement=Arrangement.spacedBy(16.dp)){
    Text("设置",fontSize=28.sp);RateField("英语语速",settings["en"]?:"0.8"){vm.setting("en",it)};RateField("中文语速",settings["zh"]?:"1.2"){vm.setting("zh",it)}
    Row{Checkbox(settings["keep"]=="true",onCheckedChange={vm.setting("keep",it.toString())});Text("前台保持屏幕常亮")}
    Text("语音使用系统离线音色。若缺少语言包，请在系统TTS设置下载；所有剧情均可使用文字模式。")
    Text("当前版本仅支持前台朗读；切到后台或锁屏将暂停。后台媒体服务、多角色音色编辑尚未实现。")
   }
  }
 }
}
@Composable fun ScenePlaceholder(label:String){Card(Modifier.fillMaxWidth().heightIn(min=160.dp)){Column(Modifier.padding(24.dp)){Text("◇  $label",fontSize=23.sp,color=MaterialTheme.colorScheme.primary);Spacer(Modifier.height(20.dp));Text("场景插画 · 本地占位画面");Text("正式场景与角色肖像待制作",style=MaterialTheme.typography.bodySmall)}}}
@Composable fun GameScreen(vm:GameModel,speech:Speech){
 val campaign by vm.campaign.collectAsState(); val p=campaign.progressFor(vm.case);val feedback by vm.feedback.collectAsState();val s=vm.case.steps.first{it.id==p.step}
 var selected by remember(vm.case.caseId,s.id){mutableStateOf(setOf<String>())};var input by remember(vm.case.caseId,s.id){mutableStateOf("")};var translation by remember{mutableStateOf(true)}
 val status by speech.status.collectAsState();val current by speech.current.collectAsState();val scroll=rememberScrollState()
 LaunchedEffect(vm.case.caseId,s.id){speech.stop();scroll.scrollTo(0)}
 var showWords by remember(vm.case.caseId,s.id){mutableStateOf(s.type=="vocabulary")}
 var transcriptVisible by remember(vm.case.caseId,s.id){mutableStateOf(s.type!="listening")}
 LaunchedEffect(current){if(current>=0)scroll.animateScrollTo(0)}
 Column(Modifier.fillMaxSize().verticalScroll(scroll).padding(24.dp),verticalArrangement=Arrangement.spacedBy(14.dp)){
  Text(s.title,fontSize=26.sp,fontWeight=FontWeight.Bold,color=MaterialTheme.colorScheme.primary)
  if(s.type=="ending"){
   Text("案件已侦破",fontSize=32.sp);Text("${if(p.mistakes==0)"★★★" else if(p.mistakes<=2)"★★☆" else "★☆☆"} · 错误 ${p.mistakes} 次 · XP ${p.xp}")
  }
  BoxWithConstraints {
   val textBlock: @Composable () -> Unit = {
    Column(verticalArrangement=Arrangement.spacedBy(12.dp)) {
     Text(vm.case.characters.firstOrNull{it.id==s.speaker}?.name?:"档案",color=MaterialTheme.colorScheme.primary)
     if(transcriptVisible) {
      Text(s.en,fontSize=21.sp,color=if(current>=0)MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface)
      if(translation)Text(s.zh,fontSize=18.sp)
     } else Text("请先播放英语，听取证词后回答。若语音不可用，可显示原文继续文字模式。",fontSize=20.sp)
    }
   }
   if(maxWidth>=720.dp) Row(horizontalArrangement=Arrangement.spacedBy(24.dp)) {
    Box(Modifier.weight(1f)){ScenePlaceholder(vm.case.sceneLabel)};Box(Modifier.weight(1f)){textBlock()}
   } else Column(verticalArrangement=Arrangement.spacedBy(16.dp)) {if(s.type!="ending")ScenePlaceholder(vm.case.sceneLabel);textBlock()}
  }
  if(s.type=="listening")TextButton(onClick={transcriptVisible=!transcriptVisible}){Text(if(transcriptVisible)"隐藏听力原文" else "显示听力原文 / 文字模式")}
  TextButton(onClick={translation=!translation}){Text(if(translation)"隐藏中文" else "显示中文")}
  Row(Modifier.horizontalScroll(rememberScrollState())){
   TextButton(onClick={speech.play(listOf(s.en to "en"))}){Text("▶ 英语")}
   TextButton(onClick={speech.play(listOf(s.en to "en",s.zh to "zh"))}){Text("英 + 中")}
   TextButton(onClick={speech.pause()}){Text("暂停")};TextButton(onClick={speech.resume()}){Text("恢复")}
  };Text(status,style=MaterialTheme.typography.bodySmall)
  if(s.words.isNotEmpty())OutlinedButton(onClick={showWords=!showWords}){Text("${if(showWords)"收起" else "学习"}本段词汇 · ${s.words.size}个词义")}
  if(showWords)s.words.forEach{id->vm.words.firstOrNull{it.id==id}?.let{w->
   Card { Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
    WordCard(w,speech)
    Row { TextButton(onClick={vm.grade(id,false)}){Text("需要强化")};TextButton(onClick={vm.grade(id,true)}){Text("记住了")} }
   } }
  }}
  s.options.forEach{c->OutlinedButton(onClick={selected=if(s.type=="deduction")if(c.id in selected)selected-c.id else selected+c.id else setOf(c.id)},modifier=Modifier.fillMaxWidth()) {Text("${if(c.id in selected)"●" else "○"} ${c.text}")}}
  if(s.type=="fill_blank")OutlinedTextField(value=input,onValueChange={input=it},label={Text("输入英文单词")},modifier=Modifier.fillMaxWidth())
  if(feedback.isNotBlank())Text(feedback,color=MaterialTheme.colorScheme.error)
  TextButton(onClick={vm.feedback.value="提示："+s.hint.ifBlank{"重读已呈现的英文与中文记录。"}}){Text("查看提示")}
  if(!p.finished)Button(onClick={speech.stop();vm.submit(if(s.type=="fill_blank")setOf(input) else selected)},modifier=Modifier.fillMaxWidth()){Text(when(s.type){"clue"->"收集证据并继续";"ending"->"保存结案结果";"dialogue","vocabulary"->"继续调查";else->"提交答案"})}
  else Text("结案结果已自动保存。可从主菜单重玩或复习词汇。")
  Spacer(Modifier.height(24.dp))
 }
}
@Composable fun WordCard(w:Word,speech:Speech){
 Text("${w.word}  ${w.partOfSpeech}",fontSize=25.sp,fontWeight=FontWeight.Bold);Text(w.meaning,fontSize=18.sp)
 w.images.forEach{im->AsyncImage(model="file:///android_asset/${im.src}",contentDescription=im.alt,modifier=Modifier.fillMaxWidth().heightIn(max=240.dp),contentScale=ContentScale.Fit,onError={android.util.Log.e("LocalAssets","Missing or invalid image: ${im.src}",it.result.throwable)})}
 Text(w.collocation.en);Text(w.collocation.zh);Text(w.example.en,fontSize=18.sp);Text(w.example.zh)
 Row{TextButton(onClick={speech.play(listOf(w.word to "en"))}){Text("读单词")};TextButton(onClick={speech.play(listOf(w.example.en to "en",w.example.zh to "zh"))}){Text("读例句")}}
}
@Composable fun RateField(label:String,initial:String,save:(String)->Unit){
 var text by remember(initial){mutableStateOf(initial)};val value=text.toFloatOrNull();val valid=value!=null&&value.isFinite()&&value in 0.2f..2f
 Column{OutlinedTextField(value=text,onValueChange={text=it},label={Text(label)},isError=!valid,supportingText={Text("范围 0.2–2.0；清空后可重新输入")});Row{
 TextButton(onClick={text=((value?:0.8f)-0.1f).coerceIn(0.2f,2f).let{String.format(java.util.Locale.US,"%.1f",it)}}){Text("−")}
 TextButton(onClick={text=((value?:0.8f)+0.1f).coerceIn(0.2f,2f).let{String.format(java.util.Locale.US,"%.1f",it)}}){Text("+")}
 Button(onClick={if(valid)save(text)},enabled=valid){Text("保存")}
 }}
}
