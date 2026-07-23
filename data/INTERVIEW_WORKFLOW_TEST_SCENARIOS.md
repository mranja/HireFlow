# Interview Workflow Test Scenarios

## Objective
Verify that the interview workflow functions correctly from interview scheduling through final hiring decisions.

---

## Test Case 1 – Schedule Interview

**Precondition**
- Candidate exists.

**Steps**
1. Open Candidate Profile.
2. Click "Schedule Interview".
3. Select interview round.
4. Assign interviewer.
5. Select interview date.
6. Save.

**Expected Result**
- Interview is scheduled successfully.
- Candidate status changes to "Interview Scheduled".

---

## Test Case 2 – Submit Interview Feedback

**Precondition**
- Interview has been scheduled.

**Steps**
1. Open interview.
2. Enter Technical Score.
3. Enter Communication Score.
4. Enter Problem Solving Score.
5. Enter Culture Fit Score.
6. Select Recommendation.
7. Submit feedback.

**Expected Result**
- Feedback is saved.
- Overall score is calculated.
- Candidate profile displays interview feedback.

---

## Test Case 3 – View Interview Feedback

**Steps**
1. Open candidate profile.
2. Navigate to Interview Feedback.

**Expected Result**
- All submitted feedback is displayed correctly.

---

## Test Case 4 – Edit Interview Feedback

**Steps**
1. Open existing feedback.
2. Modify scores/comments.
3. Save changes.

**Expected Result**
- Updated feedback is saved successfully.

---

## Test Case 5 – Delete Interview Feedback

**Steps**
1. Open interview feedback.
2. Click Delete.
3. Confirm deletion.

**Expected Result**
- Feedback is removed from the system.

---

## Test Case 6 – Search Interview Feedback

**Steps**
1. Search using candidate name.
2. Search using Candidate ID.
3. Search using interviewer name.

**Expected Result**
- Matching records are displayed.

---

## Test Case 7 – Filter Interview Feedback

**Steps**
1. Filter by Interview Round.
2. Filter by Interviewer.
3. Filter by Recommendation.

**Expected Result**
- Only matching records are displayed.

---

## Test Case 8 – Sort Interview Feedback

**Steps**
1. Sort by Date.
2. Sort by Overall Score.

**Expected Result**
- Records are sorted correctly.

---

## Test Case 9 – Candidate Recommended for Hiring

**Steps**
1. Submit feedback with Recommendation = Hire.

**Expected Result**
- Candidate status updates to "Selected" or "Ready for Offer".

---

## Test Case 10 – Candidate Rejected

**Steps**
1. Submit feedback with Recommendation = Reject.

**Expected Result**
- Candidate status updates to "Rejected".

---

## Test Case 11 – Missing Required Fields

**Steps**
1. Leave Technical Score empty.
2. Click Submit.

**Expected Result**
- Validation error is displayed.

---

## Test Case 12 – Invalid Score

**Steps**
1. Enter Technical Score = 15.
2. Submit.

**Expected Result**
- Validation prevents submission.

---

## Test Case 13 – Invalid Candidate ID

**Steps**
1. Attempt to submit feedback for a non-existent candidate.

**Expected Result**
- Appropriate error message is displayed.

---

## Test Case 14 – Duplicate Interview Feedback

**Steps**
1. Submit feedback twice for the same interview.

**Expected Result**
- Duplicate entries are prevented.

---

## Test Case 15 – Cancel Interview

**Steps**
1. Open scheduled interview.
2. Click Cancel Interview.

**Expected Result**
- Interview status changes to "Cancelled".

---

## Test Case 16 – Complete Interview Workflow

**Workflow**

Candidate Created
↓
Interview Scheduled
↓
Interview Conducted
↓
Feedback Submitted
↓
Recommendation Generated
↓
Candidate Status Updated
↓
Analytics Dashboard Updated

**Expected Result**

Entire workflow completes successfully without data loss.

---

# Edge Case Testing

## EC-01

Search with empty keyword.

Expected:
Returns all interview records.

---

## EC-02

Search with special characters.

Expected:
No application crash.

---

## EC-03

SQL Injection Attempt

Input

' OR 1=1 --

Expected:
Input safely handled.

---

## EC-04

Very Long Feedback (1000+ characters)

Expected:
Feedback saved correctly.

---

## EC-05

Future Interview Date

Expected:
Allowed if scheduling interviews in advance.

---

## EC-06

Past Interview Date

Expected:
Validation according to business rules.

---

## EC-07

Multiple Interviews for Same Candidate

Expected:
Each interview stored separately.

---

## EC-08

Concurrent Feedback Submission

Expected:
No duplicate or corrupted records.

---

# Acceptance Criteria

- Interview scheduling works.
- Feedback submission works.
- Candidate status updates correctly.
- Search works.
- Filters work.
- Sorting works.
- Validation works.
- Duplicate prevention works.
- Dashboard updates correctly.
- No unexpected errors occur.
