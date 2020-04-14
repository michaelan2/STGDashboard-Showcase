#converts due dates from datetime to date 
def getAllPOs(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, PO.VendCode, POReleases.PONum AS CoZPONum, Orders.CustCode, Orders.PONum AS CustPONum, POReleases.JobNo, POReleases.PartNo, POReleases.Qty, convert(date, POReleases.DueDate) AS DueDate, PODet.Status, POReleases.Comments, PO.User_Text1 from POReleases JOIN PODet ON (POReleases.PONum=PODet.PONum AND POReleases.PartNo=PODet.PartNo) LEFT JOIN PO ON POReleases.PONum=PO.PONum LEFT JOIN OrderDet ON OrderDet.JobNo=POReleases.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE POReleases.DateReceived IS NULL AND PODet.Status!='Closed' ORDER BY Orders.PONum")
	return cursor.fetchall()

def getAllPOs1Week(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, PO.VendCode, POReleases.PONum AS CoZPONum, Orders.CustCode, Orders.PONum AS CustPONum, POReleases.JobNo, POReleases.PartNo, POReleases.Qty, convert(date, POReleases.DueDate) AS DueDate, PODet.Status, POReleases.Comments, PO.User_Text1 from POReleases JOIN PODet ON (POReleases.PONum=PODet.PONum AND POReleases.PartNo=PODet.PartNo) LEFT JOIN PO ON POReleases.PONum=PO.PONum LEFT JOIN OrderDet ON OrderDet.JobNo=POReleases.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE POReleases.DateReceived IS NULL AND PODet.Status!='Closed' AND POReleases.DueDate<=DATEADD(week, 1, convert(date, GETDATE())) ORDER BY Orders.PONum")
	return cursor.fetchall()

def getAllPOs2Week(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, PO.VendCode, POReleases.PONum AS CoZPONum, Orders.CustCode, Orders.PONum AS CustPONum, POReleases.JobNo, POReleases.PartNo, POReleases.Qty, convert(date, POReleases.DueDate) AS DueDate, PODet.Status, POReleases.Comments, PO.User_Text1 from POReleases JOIN PODet ON (POReleases.PONum=PODet.PONum AND POReleases.PartNo=PODet.PartNo) LEFT JOIN PO ON POReleases.PONum=PO.PONum LEFT JOIN OrderDet ON OrderDet.JobNo=POReleases.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE POReleases.DateReceived IS NULL AND PODet.Status!='Closed' AND POReleases.DueDate<=DATEADD(week, 2, convert(date, GETDATE())) ORDER BY Orders.PONum")
	return cursor.fetchall()

def getAllPOs1Month(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, PO.VendCode, POReleases.PONum AS CoZPONum, Orders.CustCode, Orders.PONum AS CustPONum, POReleases.JobNo, POReleases.PartNo, POReleases.Qty, convert(date, POReleases.DueDate) AS DueDate, PODet.Status, POReleases.Comments, PO.User_Text1 from POReleases JOIN PODet ON (POReleases.PONum=PODet.PONum AND POReleases.PartNo=PODet.PartNo) LEFT JOIN PO ON POReleases.PONum=PO.PONum LEFT JOIN OrderDet ON OrderDet.JobNo=POReleases.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE POReleases.DateReceived IS NULL AND PODet.Status!='Closed' AND POReleases.DueDate<=DATEADD(month, 1, convert(date, GETDATE())) ORDER BY Orders.PONum")
	return cursor.fetchall()


def getLatePOs(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, PO.VendCode, POReleases.PONum AS CoZPONum, Orders.CustCode, Orders.PONum AS CustPONum, POReleases.JobNo, POReleases.PartNo, POReleases.Qty, convert(date, POReleases.DueDate) AS DueDate, PODet.Status, POReleases.Comments, PO.User_Text1 from POReleases JOIN PODet ON (POReleases.PONum=PODet.PONum AND POReleases.PartNo=PODet.PartNo) LEFT JOIN PO ON POReleases.PONum=PO.PONum LEFT JOIN OrderDet ON OrderDet.JobNo=POReleases.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE POReleases.DateReceived IS NULL AND PODet.Status!='Closed' AND POReleases.DueDate<convert(date, GETDATE()) ORDER BY Orders.PONum")
	return cursor.fetchall()

def getRejectedPOs(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, PO.VendCode, POReleases.PONum AS CoZPONum, Orders.CustCode, Orders.PONum AS CustPONum, POReleases.JobNo, POReleases.PartNo, POReleases.Qty, POReleases.QtyRejected, convert(date, POReleases.DueDate) AS DueDate, PODet.Status, POReleases.Comments, PO.User_Text1 from POReleases JOIN PODet ON (POReleases.PONum=PODet.PONum AND POReleases.PartNo=PODet.PartNo) LEFT JOIN PO ON POReleases.PONum=PO.PONum LEFT JOIN OrderDet ON OrderDet.JobNo=POReleases.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE POReleases.QtyRejected>0 AND PODet.Status!='Closed' ORDER BY Orders.PONum")
	return cursor.fetchall()

#If JobHasRoutingSteps = Y then link job number to Job Details page, if MasterJobHasRoutingSteps = Y then link Master Job number to Job Details page	
def getJobsNeedPurchasing(cursor):
	cursor.execute("SELECT (CASE WHEN EXISTS(SELECT OrderRouting.JobNo FROM OrderRouting WHERE OrderRouting.JobNo=OrderDet.JobNo) THEN 'Y' ELSE 'N' END) AS JobHasRoutingSteps, (CASE WHEN EXISTS(SELECT OrderRouting.JobNo FROM OrderRouting WHERE OrderRouting.JobNo=OrderDet.MasterJobNo) THEN 'Y' ELSE 'N' END) AS MasterJobHasRoutingSteps, Estim.DrawingFileName, Orders.CustCode, JobReq.JobNo, OrderDet.MasterJobNo, JobReq.VendCode, JobReq.PartNo, JobReq.PartDesc, JobReq.PurchQty, JobReq.PurchUnit, convert(date, JobReq.JobDue) AS DueDate FROM JobReq LEFT JOIN OrderDet ON JobReq.JobNo=OrderDet.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE OutsideService = 'N' AND (Jobreq.PONum IS NULL OR Jobreq.PONum = '') AND OrderDet.Status='Open' ORDER BY OrderDet.JobNo")
	return cursor.fetchall()

#for vendor stats
def getAllJobsPerVendorAllTime(cursor): #gets VendCode, TotalPO, TotalLatePO, and TotalRejectedPO
	cursor.execute("SELECT PO.VendCode, COUNT(PODet.JobNo) AS TotalPO, COUNT(CASE WHEN ((PODet.DateFinished IS NOT NULL AND PODet.DueDate<PODet.DateFinished) OR (PODet.DateFinished IS NULL AND CONVERT(date, GETDATE()) > PODet.DueDate)) THEN 1 ELSE NULL END) AS TotalLatePO, COUNT(CASE WHEN PODet.QtyReject>0 THEN 1 ELSE NULL END) AS TotalRejectedPO FROM PO JOIN PODet ON PO.PONum=PODet.PONum GROUP BY VendCode ORDER BY VendCode")
	return cursor.fetchall()

def getAllJobsPerVendorFromXMonthsAgo(cursor, months):
	cursor.execute("SELECT PO.VendCode, COUNT(PODet.JobNo) AS TotalPO, COUNT(CASE WHEN (PODet.DateFinished IS NOT NULL AND PODet.DueDate<PODet.DateFinished) THEN 1 ELSE NULL END) AS TotalLatePO, COUNT(CASE WHEN PODet.QtyReject>0 THEN 1 ELSE NULL END) AS TotalRejectedPO FROM PO JOIN PODet ON PO.PONum=PODet.PONum WHERE PODet.DueDate >= DATEADD(MONTH, ?, CONVERT(DATE, GETDATE())) AND PODet.DueDate <= CONVERT(DATE, GETDATE()) GROUP BY VendCode ORDER BY VendCode", (-months))
	return cursor.fetchall()


#don't touch this one, used by Stats page (separate tab)
def getAllVendorOrdersNum(cursor):
	cursor.execute("SELECT COUNT(POdet.JobNo) FROM PO JOIN POdet ON PO.PONum=POdet.PONum")
	return cursor.fetchone()[0]
#used by Stats page
def getAllVendorLateOrdersNum(cursor):
	cursor.execute("SELECT COUNT(POdet.JobNo) FROM PO JOIN POdet ON PO.PONum=POdet.PONum WHERE ((POdet.DateFinished IS NOT NULL AND POdet.DateFinished<=POdet.DueDate) OR (POdet.DateFinished IS NULL AND convert(date, GETDATE())<=POdet.DueDate))")
	return cursor.fetchone()[0]
	#to convert pyodbc.row's attributes into numbers, recognize that pyodbc.row behaves like a list. FetchOne returns a row, and row[0] returns the first item of that row, which is the result of our 'count' query.
def getAllPOsNum(cursor):
	cursor.execute("SELECT COUNT(*) from POReleases JOIN PODet ON (POReleases.PONum=PODet.PONum AND POReleases.PartNo=PODet.PartNo) LEFT JOIN PO ON POReleases.PONum=PO.PONum LEFT JOIN OrderDet ON OrderDet.JobNo=POReleases.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE POReleases.DateReceived IS NULL AND PODet.Status!='Closed' ")
	return cursor.fetchone()[0]
def getLatePOsNum(cursor):
	cursor.execute("SELECT COUNT(*) from POReleases JOIN PODet ON (POReleases.PONum=PODet.PONum AND POReleases.PartNo=PODet.PartNo) LEFT JOIN PO ON POReleases.PONum=PO.PONum LEFT JOIN OrderDet ON OrderDet.JobNo=POReleases.JobNo LEFT JOIN Orders ON OrderDet.OrderNo=Orders.OrderNo LEFT JOIN Estim ON OrderDet.PartNo=Estim.PartNo WHERE POReleases.DateReceived IS NULL AND PODet.Status!='Closed' AND POReleases.DueDate<convert(date, GETDATE()) ")
	return cursor.fetchone()[0]
