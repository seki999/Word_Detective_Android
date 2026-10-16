package com.worddetective

import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import org.junit.Assert.*
import org.junit.Test

class CampaignTest {
 private fun case(file:String)=codec.decodeFromString<Case>(javaClass.getResource("/$file")!!.readText())
 @Test fun catalogCasesSolveWithIndependentSaveAfterEveryStep(){
  val cases=codec.decodeFromString<Catalog>(javaClass.getResource("/catalog.json")!!.readText()).cases.map{case(it)};var campaign=Campaign()
  for(c in cases){
   campaign=campaign.select(c)
   for(s in c.steps){
    val p=campaign.progressFor(c);assertEquals(s.id,p.step)
    val input=if(s.type=="deduction")s.answers.toSet() else if(s.answer.isNotBlank())setOf(s.answer) else emptySet()
    assertTrue("Unsolvable ${c.caseId}/${s.id}",Engine.accepts(s,input))
    campaign=campaign.update(c,Engine.advance(p,s))
    campaign=codec.decodeFromString(codec.encodeToString(campaign))
   }
   assertTrue(campaign.progressFor(c).finished)
   assertEquals(c.clues.size,campaign.progressFor(c).clues.size)
  }
  assertEquals(cases.size,campaign.saves.size)
  assertTrue(campaign.progressFor(cases.first()).finished)
  assertEquals(cases.sumOf{it.steps.size}*10,campaign.saves.values.sumOf{it.xp})
 }
 @Test fun switchingDoesNotShareCluesEvenWhenStepIdsMatch(){
  val a=case("case01.json");val b=case("case02.json")
  var campaign=Campaign().update(a,Progress(step="gallery",clues=setOf("access"),xp=40))
  campaign=campaign.select(b)
  assertEquals("brief",campaign.progressFor(b).step);assertTrue(campaign.progressFor(b).clues.isEmpty())
  campaign=campaign.update(b,Progress(step="ledger",clues=setOf("income"),xp=20)).select(a)
  assertEquals(setOf("access"),campaign.progressFor(a).clues);assertEquals(40,campaign.progressFor(a).xp)
 }
 @Test fun legacySaveMigratesToOnlyTheOriginalCase(){
  val p=Progress(step="deduce",clues=setOf("access","camera"),completed=setOf("brief"),xp=90)
  val campaign=Campaign.restore(null,codec.encodeToString(p))
  assertEquals(p,campaign.progressFor(case("case01.json")))
  assertEquals(Progress(),campaign.progressFor(case("case02.json")))
 }
 @Test fun newCampaignWinsOverStaleLegacySave(){
  val original=Campaign().select(case("case02.json")).update(case("case02.json"),Progress(step="ownership",xp=50))
  assertEquals(original,Campaign.restore(codec.encodeToString(original),codec.encodeToString(Progress(xp=900))))
 }
 @Test fun emptyInstallHasTwoFreshIndependentCases(){
  val c=Campaign.restore(null,null)
  assertEquals(Progress(),c.progressFor(case("case01.json")))
  assertEquals(Progress(),c.progressFor(case("case02.json")))
 }
 @Test fun list02KeepsAllFiftySensesAndLocalImages(){
  val list=codec.decodeFromString<WordList>(javaClass.getResource("/list02.json")!!.readText())
  assertEquals(50,list.items.size);assertEquals(33,list.items.map{it.word}.toSet().size)
  assertEquals((51..100).map{"v%06d".format(it)}.toSet(),list.items.map{it.id}.toSet())
  assertTrue(list.items.all{it.images.isNotEmpty()&&it.images.all{im->im.src.startsWith("images/list02/")}})
 }
 @Test fun finalDeductionCannotBeGuessedUsingOnlyPhoto(){
  val c=case("case02.json");val step=c.steps.first{it.type=="deduction"}
  assertFalse(Engine.accepts(step,setOf("photo","income")))
  assertTrue(Engine.accepts(step,setOf("transfer","ownership")))
  assertThrows(IllegalArgumentException::class.java){Engine.advance(Progress(),step)}
 }
 @Test fun replayOfSecondCaseKeepsFirstCaseUntouched(){
  val a=case("case01.json");val b=case("case02.json")
  val first=Progress(step="end",clues=setOf("recovered"),xp=120,finished=true)
  val second=Progress(step="end",xp=240,finished=true,completed=b.steps.map{it.id}.toSet())
  val c=Campaign().update(a,first).update(b,second)
  val replay=c.update(b,second.copy(step=b.steps.first().id,clues=emptySet(),mistakes=0,finished=false))
  assertEquals(first,replay.progressFor(a));assertEquals(240,replay.progressFor(b).xp)
  assertEquals(240,Engine.advance(replay.progressFor(b),b.steps.first()).xp)
 }
}
