package com.worddetective

import kotlinx.serialization.*
import kotlinx.serialization.json.*

val codec = Json { ignoreUnknownKeys = true; encodeDefaults = true }
@Serializable data class Bilingual(val en:String="", val zh:String="")
@Serializable data class Picture(val src:String, val alt:String="")
@Serializable data class Word(val id:String,val word:String,val meaning:String,val partOfSpeech:String="",val example:Bilingual=Bilingual(),val collocation:Bilingual=Bilingual(),val images:List<Picture> = emptyList())
@Serializable data class WordList(val id:String,val items:List<Word>)
@Serializable data class Choice(val id:String,val text:String)
@Serializable data class Character(val id:String,val name:String)
@Serializable data class Clue(val id:String,val title:String)
@Serializable data class Step(val id:String,val type:String,val title:String,val en:String,val zh:String,val speaker:String="emma",val words:List<String> = emptyList(),val options:List<Choice> = emptyList(),val answer:String="",val answers:List<String> = emptyList(),val clue:String?=null,val requires:List<String> = emptyList(),val next:String?=null,val hint:String="")
@Serializable data class Case(val caseId:String,val schemaVersion:Int,val title:String,val description:String,val vocabularyListId:String="list01",val sceneLabel:String="MERIDIAN MUSEUM",val requiredVocabularyIds:List<String>,val characters:List<Character>,val clues:List<Clue>,val steps:List<Step>)
@Serializable data class Progress(val step:String="brief",val clues:Set<String> = emptySet(),val completed:Set<String> = emptySet(),val mistakes:Int=0,val xp:Int=0,val finished:Boolean=false)
@Serializable data class Review(val wordId:String,val reviewCount:Int=0,val correctCount:Int=0,val wrongCount:Int=0,val lastReviewedAt:Long=0,val nextReviewAt:Long=0,val masteryLevel:String="新词",val interval:Int=0,val repetitions:Int=0,val ease:Double=2.5)
object Scheduler {
 // Simplified SM-2, revision WD-1: correct quality 4, incorrect quality 1.
 fun grade(r:Review,correct:Boolean,now:Long):Review {
  val days=if(!correct) 1 else when(r.repetitions) { 0->1; 1->6; else->(r.interval*r.ease).toInt().coerceAtLeast(1) }
  return r.copy(reviewCount=r.reviewCount+1,correctCount=r.correctCount+if(correct)1 else 0,wrongCount=r.wrongCount+if(correct)0 else 1,lastReviewedAt=now,nextReviewAt=now+days*86400000L,interval=days,repetitions=if(correct)r.repetitions+1 else 0,ease=(r.ease+if(correct)0.0 else -0.54).coerceAtLeast(1.3),masteryLevel=if(!correct)"需要强化" else if(days>=21)"已掌握" else if(r.correctCount>0)"复习中" else "学习中")
 }
}
object Engine {
 fun accepts(s:Step,input:Set<String>) = when(s.type) { "multiple_choice","listening","image_choice","fill_blank" -> input.singleOrNull()?.trim()?.lowercase()==s.answer.lowercase(); "deduction"->input==s.answers.toSet(); else->true }
 fun advance(p:Progress,s:Step):Progress {
  require(p.clues.containsAll(s.requires))
  return p.copy(step=s.next?:s.id,clues=p.clues+listOfNotNull(s.clue),completed=p.completed+s.id,xp=p.xp+if(s.id in p.completed)0 else 10,finished=p.finished||s.type=="ending")
 }
}

@Serializable data class Catalog(val cases:List<String>)
/** One persisted snapshot prevents a selection from being paired with another case's progress. */
@Serializable data class Campaign(val activeCaseId:String="missing-sapphire",val saves:Map<String,Progress> = emptyMap()) {
 fun progressFor(case:Case)=saves[case.caseId]?:Progress(step=case.steps.first().id)
 fun select(case:Case)=copy(activeCaseId=case.caseId)
 fun update(case:Case,progress:Progress)=copy(saves=saves+(case.caseId to progress))
 companion object {
  fun restore(campaignJson:String?,legacyJson:String?):Campaign = if(campaignJson!=null) codec.decodeFromString(campaignJson)
   else Campaign(saves=legacyJson?.let{mapOf("missing-sapphire" to codec.decodeFromString<Progress>(it))}?:emptyMap())
 }
}
