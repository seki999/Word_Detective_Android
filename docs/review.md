# 复习调度 WD-1

简化SM-2变体，版本WD-1；不是完整SM-2或FSRS。每个词义ID独立记录，不按英文拼写合并。

字段：wordId、reviewCount、correctCount、wrongCount、lastReviewedAt、nextReviewAt、masteryLevel。retention参数采用interval（天）、repetitions（连续正确次数）、ease（默认2.5，下限1.3）三个显式字段保存。

- 正确：连续第1次间隔1天，第2次6天，以后floor(旧间隔×ease)，至少1天；连续计数+1，总正确数+1。
- 错误：间隔1天，ease减少0.54，下限1.3，连续正确计数归零，总错误数+1，状态需要强化。
- nextReviewAt = now + interval × 86,400,000毫秒。使用传入时间，单元测试可固定时间。
- 正确时：间隔>=21天为已掌握，否则累计正确>1为复习中，首次为学习中；无记录为新词。
- 每日复习显示到期或需要强化词条。当前采用用户自评，尚未实现复习随机题。

这是透明的入门调度，不提供真实记忆保持率估计。未来更换算法需保留旧参数并提供转换，不能删除既有学习记录。
