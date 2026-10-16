package com.worddetective
import android.content.Context
import android.os.Handler
import android.os.Looper
import android.speech.tts.*
import java.util.Locale
import kotlinx.coroutines.flow.MutableStateFlow
class Speech(context:Context) {
 val status=MutableStateFlow("语音初始化中")
 val current=MutableStateFlow(-1)
 private var ready=false
 private var queue:List<Pair<String,String>> = emptyList()
 private val cursor=SpeechCursor()
 private val handler=Handler(Looper.getMainLooper())
 private var tts:TextToSpeech?=null
 var englishRate=0.8f; var chineseRate=1.2f
 init { tts=TextToSpeech(context){result -> ready=result==TextToSpeech.SUCCESS;status.value=if(ready)"就绪" else "语音不可用，请使用文字模式" } }
 fun play(lines:List<Pair<String,String>>) {stop();queue=lines;cursor.start(lines.size);say()}
 private fun say(){
  val engine=tts?:return
  if(!ready||cursor.index !in queue.indices){current.value=-1;return}
  val (text,lang)=queue[cursor.index];val locale=if(lang=="zh")Locale.SIMPLIFIED_CHINESE else Locale.US
  val voice=engine.voices?.firstOrNull{it.locale.language==locale.language&&!it.isNetworkConnectionRequired}
  if(voice==null){status.value="缺少离线${if(lang=="zh")"中文" else "英语"}语音包；可继续阅读文字。";current.value=-1;return}
  engine.voice=voice;engine.setSpeechRate(if(lang=="zh")chineseRate else englishRate)
  val token=cursor.revision
  engine.setOnUtteranceProgressListener(object:UtteranceProgressListener(){
   override fun onStart(id:String?){if(id=="$token")status.value="朗读中"}
   override fun onDone(id:String?){handler.post{if(id=="$token"&&cursor.complete(token)){if(cursor.index<queue.size)say() else {current.value=-1;status.value="朗读完成"}}}}
   @Deprecated("platform callback") override fun onError(id:String?){if(id=="${cursor.revision}")status.value="朗读失败；请使用文字模式"}
  });current.value=cursor.index
  if(engine.speak(text,TextToSpeech.QUEUE_FLUSH,null,token.toString())==TextToSpeech.ERROR)status.value="无法朗读；请使用文字模式"
 }
 fun pause(){cursor.pause();tts?.stop();current.value=-1;status.value="已暂停（恢复时从本句开始）"}
 fun resume(){cursor.resume();say()}
 fun next(){cursor.move(1);tts?.stop();say()}
 fun previous(){cursor.move(-1);tts?.stop();say()}
 fun stop(){cursor.stop();tts?.stop();current.value=-1}
 fun close(){stop();tts?.shutdown()}
}
