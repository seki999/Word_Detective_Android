package com.worddetective
import org.junit.Assert.*
import org.junit.Test
class SpeechCursorTest {
 @Test fun completesOnlyThroughCallback(){val q=SpeechCursor();q.start(2);assertEquals(0,q.index);assertTrue(q.complete(q.revision));assertEquals(1,q.index)}
 @Test fun staleCallbackCannotAdvanceNewQueue(){val q=SpeechCursor();q.start(2);val old=q.revision;q.start(3);assertFalse(q.complete(old));assertEquals(0,q.index)}
 @Test fun pausedCallbackCannotAdvance(){val q=SpeechCursor();q.start(2);val old=q.revision;q.pause();assertFalse(q.complete(old));q.resume();assertTrue(q.complete(q.revision))}
 @Test fun stopsAtEnd(){val q=SpeechCursor();q.start(1);q.complete(q.revision);assertFalse(q.complete(q.revision));q.move(-1);assertEquals(0,q.index)}
 @Test fun lapseResetsReviewIntervals(){var r=Review("x");repeat(4){r=Scheduler.grade(r,true,0)};r=Scheduler.grade(r,false,0);r=Scheduler.grade(r,true,100);assertEquals(1,r.interval);assertEquals(5,r.correctCount)}
}
