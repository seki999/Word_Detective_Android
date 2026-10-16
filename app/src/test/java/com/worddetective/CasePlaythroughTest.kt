package com.worddetective
import org.junit.Assert.*
import org.junit.Test
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
class CasePlaythroughTest {
 @Test fun solveEntireCaseWithSaveRestoreAfterEveryStep(){
  val c=codec.decodeFromString<Case>(javaClass.getResource("/case01.json")!!.readText())
  var p=Progress()
  for(s in c.steps){
   assertEquals(s.id,p.step)
   val input=if(s.type=="deduction")s.answers.toSet() else if(s.answer.isNotEmpty())setOf(s.answer) else emptySet()
   assertTrue("Unsolvable ${s.id}",Engine.accepts(s,input))
   p=Engine.advance(p,s)
   p=codec.decodeFromString(codec.encodeToString(p))
  }
  assertTrue(p.finished);assertEquals(5,p.clues.size);assertEquals(c.steps.size,p.completed.size)
 }
 @Test fun actualListPreservesDistinctSenses(){
  val list=codec.decodeFromString<WordList>(javaClass.getResource("/list01.json")!!.readText())
  assertEquals(50,list.items.size);assertEquals(31,list.items.map{it.word}.toSet().size)
  assertNotEquals(list.items[0].id,list.items[1].id);assertNotEquals(list.items[0].meaning,list.items[1].meaning)
 }
}
