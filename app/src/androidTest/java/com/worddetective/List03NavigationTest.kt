package com.worddetective
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import org.junit.Rule
import org.junit.Test
class List03NavigationTest {
 @get:Rule val rule=createAndroidComposeRule<MainActivity>()
 @Test fun opensThirdCaseAndSwitchesAllThreeLists(){
  rule.waitUntil(10000){rule.onAllNodesWithText("打开案件档案").fetchSemanticsNodes().isNotEmpty()}
  rule.onNodeWithText("打开案件档案").performScrollTo().performClick()
  rule.onNodeWithTag("open-switched-restoration-charter").performScrollTo().performClick()
  rule.onNodeWithText("01 · 修缮协议失踪").assertIsDisplayed()
  rule.onNodeWithText("主菜单").performClick()
  rule.onNodeWithTag("nav-lexicon").performScrollTo().performClick()
  rule.onNodeWithTag("words-list03").performScrollTo().performClick()
  rule.onNodeWithText("高贵的；气度不凡的").assertExists()
  rule.onNodeWithTag("words-list01").performScrollTo().performClick()
  rule.onNodeWithText("戒除；避免（尤指酒、食物等）").assertExists()
  rule.onNodeWithTag("words-list02").performScrollTo().performClick()
  rule.onNodeWithText("调和；使一致；对账").assertExists()
 }
}
