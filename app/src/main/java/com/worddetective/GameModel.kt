package com.worddetective

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import androidx.room.Room
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.encodeToString
import kotlinx.serialization.decodeFromString

class GameModel(private val app:Application):AndroidViewModel(app) {
 private val db=Room.databaseBuilder(app,DetectiveDb::class.java,"detective.db").build()
 private val writes=Channel<Stored>(Channel.UNLIMITED)
 private fun asset(name:String)=app.assets.open(name).bufferedReader().use{it.readText()}
 val cases=codec.decodeFromString<Catalog>(asset("catalog.json")).cases.map { codec.decodeFromString<Case>(asset(it)) }
 val wordLists=cases.map{it.vocabularyListId}.distinct().associateWith{codec.decodeFromString<WordList>(asset("$it.json")).items}
 val campaign=MutableStateFlow(Campaign(activeCaseId=cases.first().caseId))
 val case get()=cases.first{it.caseId==campaign.value.activeCaseId}
 val words get()=wordLists.getValue(case.vocabularyListId)
 val progress get()=campaign.value.progressFor(case)
 val totalXp get()=campaign.value.saves.values.sumOf{it.xp}
 val reviews=MutableStateFlow<Map<String,Review>>(emptyMap())
 val settings=MutableStateFlow(mapOf("en" to "0.8","zh" to "1.2","keep" to "true"))
 val ready=MutableStateFlow(false)
 val feedback=MutableStateFlow("")
 init {
  viewModelScope.launch { for(write in writes) db.store().put(write) }
  viewModelScope.launch {
   val saved=Campaign.restore(db.store().read("campaign")?.json,db.store().read("progress")?.json)
   campaign.value=if(cases.any{it.caseId==saved.activeCaseId})saved else saved.select(cases.first())
   db.store().read("reviews")?.let { reviews.value=codec.decodeFromString(it.json) }
   db.store().read("settings")?.let { settings.value=codec.decodeFromString(it.json) }
   // Persist the upgraded payload while retaining the old v0.1 key for recovery.
   save("campaign",codec.encodeToString(campaign.value))
   ready.value=true
  }
 }
 fun selectCase(id:String) {
  if(!ready.value)return
  val selected=cases.firstOrNull{it.caseId==id}?:return
  campaign.value=campaign.value.select(selected)
  feedback.value=""
  save("campaign",codec.encodeToString(campaign.value))
 }
 val step get()=case.steps.first{it.id==progress.step}
 fun submit(input:Set<String>) {
  if(!ready.value||progress.finished)return
  val s=step;val p=progress
  if(!p.clues.containsAll(s.requires)){feedback.value="请先收集所需证物。";return}
  val ok=Engine.accepts(s,input)
  // Reading a line is not a recall test; only grade answers to interactive questions.
  if(s.type in setOf("multiple_choice","listening","image_choice","fill_blank","deduction"))s.words.forEach{grade(it,ok)}
  val updated=if(ok){feedback.value="";Engine.advance(p,s)}
   else{feedback.value="线索尚不支持这个答案。请重读记录，再试一次。";p.copy(mistakes=p.mistakes+1)}
  campaign.value=campaign.value.update(case,updated)
  save("campaign",codec.encodeToString(campaign.value))
 }
 fun grade(id:String,correct:Boolean) {
  if(!ready.value||wordLists.values.none{list->list.any{it.id==id}})return
  reviews.value=reviews.value+(id to Scheduler.grade(reviews.value[id]?:Review(id),correct,System.currentTimeMillis()))
  save("reviews",codec.encodeToString(reviews.value))
 }
 fun replay(){
  if(!ready.value)return
  campaign.value=campaign.value.update(case,progress.copy(step=case.steps.first().id,clues=emptySet(),mistakes=0,finished=false))
  save("campaign",codec.encodeToString(campaign.value));feedback.value=""
 }
 fun setting(key:String,value:String){settings.value=settings.value+(key to value);save("settings",codec.encodeToString(settings.value))}
 private fun save(key:String,json:String){writes.trySend(Stored(key,json))}
 override fun onCleared(){db.close()}
}
