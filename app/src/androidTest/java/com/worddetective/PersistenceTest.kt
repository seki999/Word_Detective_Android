package com.worddetective
import android.content.Context
import androidx.room.Room
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import kotlinx.coroutines.runBlocking
class PersistenceTest {
 @Test fun reopeningSameDatabaseKeepsSave()=runBlocking {
  val context=InstrumentationRegistry.getInstrumentation().targetContext
  val name="retention-test.db";context.deleteDatabase(name)
  val db=Room.databaseBuilder(context,DetectiveDb::class.java,name).build()
  db.store().put(Stored("progress","saved-evidence"));db.close()
  val updated=Room.databaseBuilder(context,DetectiveDb::class.java,name).build()
  assertEquals("saved-evidence",updated.store().read("progress")?.json)
  updated.close();context.deleteDatabase(name)
 }
}
