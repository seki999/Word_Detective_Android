package com.worddetective
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import org.junit.Rule
import org.junit.Test
class List02NavigationTest {
 @get:Rule val rule=createAndroidComposeRule<MainActivity>()
 private fun home(){rule.waitUntil(10000){rule.onAllNodesWithText("打开案件档案").fetchSemanticsNodes().isNotEmpty()}}
 @Test fun secondCaseUsesOwnStoryAndHints(){
  home()
  rule.onNodeWithText("打开案件档案").performScrollTo().performClick()
  rule.onNodeWithTag("open-missing-relief-fund").performScrollTo().performClick()
  rule.onNodeWithText("01 · 义演后的求助").assertIsDisplayed()
  rule.onNodeWithText("查看提示").performScrollTo().performClick()
  rule.onNodeWithText("提示：重读已呈现的英文与中文记录。").assertExists()
  rule.onNodeWithText("主菜单").performClick()
  rule.onNodeWithTag("nav-lexicon").performScrollTo().performClick()
  rule.onNodeWithTag("words-list02").performClick()
  rule.onNodeWithText("调和；使一致；对账").assertExists()
  rule.onNodeWithTag("words-list01").performClick()
  rule.onNodeWithText("戒除；避免（尤指酒、食物等）").assertExists()
 }
}
