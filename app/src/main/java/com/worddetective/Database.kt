package com.worddetective
import androidx.room.*

@Entity data class Stored(@PrimaryKey val key:String,val json:String)
@Dao interface StoreDao {
 @Query("SELECT * FROM Stored WHERE `key`=:key") suspend fun read(key:String):Stored?
 @Insert(onConflict=OnConflictStrategy.REPLACE) suspend fun put(value:Stored)
}
@Database(entities=[Stored::class],version=1,exportSchema=true)
abstract class DetectiveDb:RoomDatabase() { abstract fun store():StoreDao }
