package com.worddetective
/** Callbacks must carry a revision so stopped utterances cannot advance a new queue. */
class SpeechCursor {
 var index=0; private set
 var revision=0; private set
 var paused=true; private set
 var size=0; private set
 fun start(count:Int){revision++;size=count;index=0;paused=false}
 fun pause(){revision++;paused=true}
 fun resume(){revision++;paused=false}
 fun move(delta:Int){revision++;index=(index+delta).coerceIn(0,size);paused=false}
 fun complete(token:Int):Boolean{if(token!=revision||paused||index>=size)return false;index++;revision++;return true}
 fun stop(){pause();size=0;index=0}
}
