
def getOnTimeDelivery(cursor):
	cursor.execute("SELECT COUNT(DISTINCT JobNo) FROM OrderDet WHERE (DateFinished IS NOT NULL AND DueDate>=DateFinished) OR (DateFinished IS NULL AND Duedate>=convert(date, GETDATE()))")
	return cursor.fetchone()[0]

def getAllDelivery(cursor):
	cursor.execute("SELECT COUNT(DISTINCT JobNo) FROM OrderDet")
	return cursor.fetchone()[0]

def getQuotesWon(cursor): #returns an int
	cursor.execute("SELECT COUNT(QuoteNo) FROM QuoteDet WHERE Status='WON'")
	return cursor.fetchone()[0]

def getQuotesLost(cursor):
	cursor.execute("SELECT COUNT(QuoteNo) FROM QuoteDet WHERE Status='LOST'")
	return cursor.fetchone()[0]

def getQuotesExpired(cursor):
	cursor.execute("SELECT COUNT(QuoteNo) FROM QuoteDet WHERE Status='EXP'")
	return cursor.fetchone()[0]

def getTotalQuotes(cursor): #obsolete
	cursor.execute("SELECT COUNT(QuoteNo) FROM QuoteDet")
	return cursor.fetchone()
	#NOTE: this includes PENDING quotes, which are not included in the pie chart anymore.

def getJobsInProg_Late_BehindSched_Count(cursor):
	cursor.execute("SELECT COUNT(*) AS NumJobsInProgress, COUNT(CASE WHEN (CONVERT(DATE, GETDATE())>OrderDet.DueDate) THEN 1 ELSE NULL END) AS NumLateJobsInProgress, COUNT(CASE WHEN (OrderRouting.ActualStartDate IS NULL AND OrderRouting.EstimStartDate < GETDATE() OR (OrderRouting.ActualEndDate IS NULL AND OrderRouting.EstimEndDate IS NOT NULL AND GETDATE() > OrderRouting.EstimEndDate)) THEN 1 ELSE NULL END) AS NumBehindScheduleJobsInProgress FROM OrderDet LEFT JOIN OrderRouting ON OrderDet.JobNo = OrderRouting.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE OrderRouting.Status='Current' AND OrderDet.Status!='Closed' AND (OrderDet.DateFinished IS NULL OR OrderDet.DateFinished='')")
	return cursor.fetchone()
	#[0] =NumJobsInProgress, [1]=NumLateJobsInProgress, [2]=NumBehindScheduleJobsInProgress

def getJobsDueToday_Tomorrow_ThisWeek_Count(cursor):
	cursor.execute("SELECT COUNT(CASE WHEN OrderDet.DueDate=CONVERT(DATE, GETDATE()) THEN 1 ELSE NULL END) AS NumJobsDueToday, COUNT(CASE WHEN OrderDet.DueDate=DATEADD(DAY, 1, CONVERT(DATE, GETDATE())) THEN 1 ELSE NULL END) AS NumJobsDueTomorrow, COUNT(CASE WHEN (OrderDet.DueDate>CONVERT(DATE, GETDATE()) AND OrderDet.DueDate<=DATEADD(WEEK, 1, CONVERT(DATE, GETDATE()))) THEN 1 ELSE NULL END) AS NumJobsDueThisWeek FROM OrderRouting JOIN OrderDet ON OrderRouting.JobNo=OrderDet.JobNo WHERE (OrderRouting.Status = 'Current')")
	return cursor.fetchone()
	#[0] = NumJobsDueToday, [1]=NumJobsDueTomorrow, [2]=NumJobsDueThisWeek

#returns a list of summed total positive feedback and total negative feedback for all dates within THIS quarter (e.g. 7/01/18 to <10/01/18)
#ISNULL around sums ensures the graph displays 0 instead of breaking when a new quarter has no feedback values in it

def getCustSurveyQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT SUM(CASE WHEN FeedbackType='Positive' THEN 1 ELSE 0 END) AS NumPositive, SUM(CASE WHEN FeedbackType='Negative' THEN 1 ELSE 0 END) AS NumNegative FROM Feedback WHERE FeedbackDate >= DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) AND FeedbackDate < DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0)", (-qtrsago), (-qtrsago+1))
	return cursor.fetchall()

#returns a start and end date, qtr 0 is this qtr
def getQtrXAgoDateStart_End(cursor, qtrsago):
	cursor.execute("SELECT CONVERT(date, DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) ), CONVERT(date, DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) )", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()

#input 3 returns 10/01 to 1/01, 3 quarters ago

#input 2 returns 1/01 to 4/01 non-inclusive, 2 quarters ago

#input 1 returns 4/01 to 7/01 non-inclusive, last quarter

#input 0 returns this quarter: 7/01 to 10/01
 

#this qtr is 0 qtrs ago. Calling on [0] of the result gives us the int directly
def getVendJobsLateQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT COUNT(JobNo) FROM POdet WHERE DateFinished>DueDate AND DueDate >= CONVERT(date, DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) ) AND DueDate < CONVERT(date, DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) )", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()[0] 

def getVendJobsTotalQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT COUNT(JobNo) FROM POdet WHERE DueDate >= CONVERT(date, DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) ) AND DueDate < CONVERT(date, DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) )", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()[0]

#returns total parts rejected in [0] and total parts ordered in [1]
def getVendPartsRejectedQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT SUM(QtyReject), SUM(QtyOrd) FROM POdet WHERE DueDate >= CONVERT(date, DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) ) AND DueDate < CONVERT(date, DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) )", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()

#CoZ Rejects (qtr)
def getCoZPartsRejectedQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT SUM(Quantity) FROM NonConformance WHERE ReturnType='CUSTOMER' AND NonConfDate >= DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) AND NonConfDate < DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0)", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()[0]

def getCoZTotalPartsQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT SUM(QtyOrdered) FROM OrderDet WHERE DueDate >= DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) AND DueDate < DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0)", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()[0]

def getCoZJobsLateQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT COUNT(JobNo) FROM OrderDet WHERE DueDate<DateFinished AND DueDate >= DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) AND DueDate < DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0)", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()[0]

def getCoZJobsTotalQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT COUNT(JobNo) FROM OrderDet WHERE DueDate >= DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) AND DueDate < DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0)", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()[0]


#don't do division within SQL query; it will round the output to 0. Do the division in the JS of the Google Chart
#% Parts Scrapped (Qtr)
def getPartsScrapped_PartsGoodQtrXAgo(cursor, qtrsago):
	cursor.execute("SELECT SUM(OrderRouting.ActualPcsScrap) AS TotalPartsScrap, SUM(OrderRouting.ActualPcsGood) AS TotalPartsGood from OrderRouting JOIN OrderDet ON OrderRouting.JobNo=OrderDet.JobNo WHERE OrderDet.Status = 'Closed' AND OrderDet.DueDate >= DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0) AND OrderDet.DueDate < DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1)), 0)", (-qtrsago), (-qtrsago+1))
	return cursor.fetchone()