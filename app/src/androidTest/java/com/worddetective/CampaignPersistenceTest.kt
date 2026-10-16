package com.worddetective
import androidx.room.Room
import androidx.test.platform.app.InstrumentationRegistry
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import org.junit.Assert.*
import org.junit.Test
class CampaignPersistenceTest {
 @Test fun legacyRoomPayloadUpgradesAndBothCasesSurviveReopening()=runBlocking {
  val context=InstrumentationRegistry.getInstrumentation().targetContext
  val name="campaign-retention-test.db";context.deleteDatabase(name)
  fun open()=Room.databaseBuilder(context,DetectiveDb::class.java,name).build()
  fun case(file:String)=codec.decodeFromString<Case>(context.assets.open(file).bufferedReader().use{it.readText()})
  val first=case("case01.json");val second=case("case02.json")
  val legacy=Progress(step="deduce",xp=80,clues=setOf("access","camera"))
  val db=open();db.store().put(Stored("progress",codec.encodeToString(legacy)));db.close()
  val upgraded=open()
  var campaign=Campaign.restore(upgraded.store().read("campaign")?.json,upgraded.store().read("progress")?.json)
  assertEquals(legacy,campaign.progressFor(first))
  campaign=campaign.select(second).update(second,Progress(step="ledger",xp=90,clues=setOf("income")))
  upgraded.store().put(Stored("campaign",codec.encodeToString(campaign)));upgraded.close()
  val reopened=open()
  val restored=Campaign.restore(reopened.store().read("campaign")?.json,reopened.store().read("progress")?.json)
  assertEquals(campaign,restored);assertEquals(legacy,restored.progressFor(first))
  assertEquals(setOf("income"),restored.progressFor(second).clues)
  assertNotNull(reopened.store().read("progress"));reopened.close();context.deleteDatabase(name)
 }
}
