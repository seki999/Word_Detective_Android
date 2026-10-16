package com.worddetective
import org.junit.Assert.*
import org.junit.Test
import kotlinx.serialization.encodeToString
import kotlinx.serialization.decodeFromString
class LogicTest {
 @Test fun restoredProgressKeepsEvidence(){val p=Progress(step="deduce",clues=setOf("access","camera"),completed=setOf("brief"),xp=20);assertEquals(p,codec.decodeFromString<Progress>(codec.encodeToString(p)))}
 @Test fun repeatedStepsCannotFarmXp(){val s=Step("a","dialogue","a","a","a",next="b");val p=Engine.advance(Progress(),s);assertEquals(p.xp,Engine.advance(p,s).xp)}
 @Test fun missingClueBlocksDeduction(){val s=Step("a","deduction","a","a","a",requires=listOf("proof"));assertThrows(IllegalArgumentException::class.java){Engine.advance(Progress(),s)}}
 @Test fun deductionNeedsExactSet(){val s=Step("a","deduction","a","a","a",answers=listOf("one","two"));assertTrue(Engine.accepts(s,setOf("one","two")));assertFalse(Engine.accepts(s,setOf("one")));assertFalse(Engine.accepts(s,setOf("one","two","three")))}
 @Test fun firstCorrectSchedulesOneDay(){val r=Scheduler.grade(Review("x"),true,100);assertEquals(86400100L,r.nextReviewAt);assertEquals("学习中",r.masteryLevel)}
 @Test fun secondCorrectSchedulesSixDays(){val r=Scheduler.grade(Scheduler.grade(Review("x"),true,0),true,100);assertEquals(518400100L,r.nextReviewAt)}
 @Test fun wrongAnswerNeedsReinforcement(){val r=Scheduler.grade(Review("x"),false,0);assertEquals("需要强化",r.masteryLevel);assertEquals(1,r.wrongCount);assertEquals(86400000L,r.nextReviewAt)}
 @Test fun invalidJsonFails(){assertThrows(kotlinx.serialization.SerializationException::class.java){codec.decodeFromString<Progress>("{")}}
 @Test fun blankAnswersAreSafe(){val s=Step("a","fill_blank","a","a","a",answer="word");assertFalse(Engine.accepts(s,setOf("")));assertTrue(Engine.accepts(s,setOf(" Word ")))}
}
