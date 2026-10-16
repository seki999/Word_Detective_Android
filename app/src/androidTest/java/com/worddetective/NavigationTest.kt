package com.worddetective
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import org.junit.Rule
import org.junit.Test
class NavigationTest {
 @get:Rule val rule=createAndroidComposeRule<MainActivity>()
 @Test fun opensCaseAndSettings(){
  rule.waitUntil(10000){rule.onAllNodesWithText("打开案件档案").fetchSemanticsNodes().isNotEmpty()}
  rule.onNodeWithText("打开案件档案").performScrollTo().performClick()
  rule.onNodeWithText("The Missing Sapphire").assertIsDisplayed()
  rule.onNodeWithText("主菜单").performClick()
  rule.onNodeWithText("设置").performScrollTo().performClick()
  rule.onNodeWithText("英语语速").assertIsDisplayed()
  rule.onNodeWithText("英语语速").performTextClearance()
  rule.onNodeWithText("英语语速").performTextInput("0.9")
 }
}
