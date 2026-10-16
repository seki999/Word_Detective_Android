package com.worddetective

import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import org.junit.Assert.*
import org.junit.Test

class List03Test {
 private fun case(file:String)=codec.decodeFromString<Case>(javaClass.getResource("/$file")!!.readText())
 private val third get()=case("case03.json")
 @Test fun list03HasFiftySensesAndFiftyLocalImages(){
  val words=codec.decodeFromString<WordList>(javaClass.getResource("/list03.json")!!.readText()).items
  assertEquals(50,words.size);assertEquals(32,words.map{it.word}.toSet().size)
  assertEquals((101..150).map{"v%06d".format(it)}.toSet(),words.map{it.id}.toSet())
  assertEquals(50,words.sumOf{it.images.size});assertTrue(words.all{it.images.all{im->im.src.startsWith("images/list03/")}})
 }
 @Test fun version02CampaignRestoresWithoutChangingEitherPriorCase(){
  val a=case("case01.json");val b=case("case02.json")
  val pa=Progress(step="deduce",xp=80,clues=setOf("access","camera"))
  val pb=Progress(step="ownership",xp=140,clues=setOf("transfer","photo"))
  val old=Campaign().update(a,pa).update(b,pb).select(b)
  val restored=Campaign.restore(codec.encodeToString(old),null)
  val selected=restored.select(third)
  assertEquals(pa,selected.progressFor(a));assertEquals(pb,selected.progressFor(b))
  assertEquals(Progress(),selected.progressFor(third));assertEquals(old.saves,selected.saves)
 }
 @Test fun originalLegacySaveDoesNotBecomeAThirdCaseSave(){
  val p=Progress(step="lab",xp=60)
  val restored=Campaign.restore(null,codec.encodeToString(p))
  assertEquals(p,restored.progressFor(case("case01.json")))
  assertEquals(Progress(),restored.progressFor(third))
 }
 @Test fun thirdCaseStatePersistsAlongsideTheOtherTwo(){
  val a=case("case01.json");val b=case("case02.json");val c=third
  val campaign=Campaign().update(a,Progress(xp=10)).update(b,Progress(xp=20))
   .update(c,Progress(step="system",xp=150,clues=setOf("identity","camera","access"))).select(c)
  val restored=codec.decodeFromString<Campaign>(codec.encodeToString(campaign))
  assertEquals(campaign,restored);assertEquals(3,restored.saves.size)
  assertEquals("system",restored.progressFor(c).step);assertEquals(180,restored.saves.values.sumOf{it.xp})
 }
 @Test fun deadlineAndMotiveCannotReplacePhysicalProof(){
  val s=third.steps.first{it.type=="deduction"}
  assertFalse(Engine.accepts(s,setOf("terms","system")))
  assertFalse(Engine.accepts(s,setOf("camera")))
  assertTrue(Engine.accepts(s,setOf("identity","camera")))
  assertThrows(IllegalArgumentException::class.java){Engine.advance(Progress(clues=setOf("terms")),s)}
 }
 @Test fun originalMustBeRecoveredBeforeTheEnding(){
  val end=third.steps.last()
  val collected=end.requires.toSet()-"recovered"
  assertThrows(IllegalArgumentException::class.java){Engine.advance(Progress(clues=collected),end)}
  assertTrue(Engine.advance(Progress(clues=collected+"recovered"),end).finished)
 }
 @Test fun replayingThirdCaseDoesNotAlterEarlierRewards(){
  val a=case("case01.json");val b=case("case02.json");val c=third
  val done=Progress(step="end",xp=c.steps.size*10,finished=true,completed=c.steps.map{it.id}.toSet())
  val old=Campaign().update(a,Progress(xp=120)).update(b,Progress(xp=240)).update(c,done)
  val replay=old.update(c,done.copy(step="brief",finished=false,clues=emptySet()))
  assertEquals(old.progressFor(a),replay.progressFor(a));assertEquals(old.progressFor(b),replay.progressFor(b))
  assertEquals(done.xp,Engine.advance(replay.progressFor(c),c.steps.first()).xp)
 }
 @Test fun homographMasteryIsIndependentAcrossLists(){
  val reviews=mapOf("v000100" to Scheduler.grade(Review("v000100"),true,10),"v000101" to Scheduler.grade(Review("v000101"),false,20))
  val restored=codec.decodeFromString<Map<String,Review>>(codec.encodeToString(reviews))
  assertEquals("学习中",restored.getValue("v000100").masteryLevel)
  assertEquals("需要强化",restored.getValue("v000101").masteryLevel)
  assertEquals(0,restored.getValue("v000100").wrongCount)
 }
}
