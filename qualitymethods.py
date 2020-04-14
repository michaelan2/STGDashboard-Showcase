def getCustomerReturnStatus(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, CustReturn.CustCode, convert(date, CustReturn.IssueDate) AS IssueDate, CustReturnDet.PartNo, CustReturn.CustRMANo, CustReturn.Status, CustReturnDet.QtyToRework, CustReturnDet.OrigQtyShipped, CustReturnDet.ReworkJobNo, ISNULL(OrderRouting.WorkCntr, OrderRouting.VendCode) AS Location, ISNULL(OrderRouting.OperCode, '') AS OperCode, ISNULL(OrderDet.User_Text1, '') AS JobComments FROM CustReturn JOIN CustReturnDet ON CustReturn.CustRMANo=CustReturnDet.CustRMANo LEFT JOIN OrderDet ON (CustReturnDet.ReworkJobNo=OrderDet.JobNo AND CustReturnDet.PartNo=OrderDet.PartNo) LEFT JOIN OrderRouting ON (OrderDet.JobNo=OrderRouting.JobNo AND OrderRouting.Status='Current') LEFT JOIN Estim ON CustReturnDet.PartNo=Estim.PartNo WHERE CustReturn.Status!='Complete' AND CustReturn.Status!='Refused' ")
	return cursor.fetchall()

def getVendorReturnStatus(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, VendReturn.VendReturnNo, VendReturn.VendCode, convert(date, VendReturn.IssueDate) AS IssueDate, VendReturn.Status, VendReturnDet.PartNo, VendReturnDet.JobNo, VendReturnDet.QtyToReject, VendReturnDet.OrigQtyReceived, VendReturn.QCComment, ISNULL(OrderDet.User_Text1, '') AS JobComments FROM VendReturn LEFT JOIN VendReturnDet ON VendReturn.VendReturnNo=VendReturnDet.VendReturnNo LEFT JOIN OrderDet ON VendReturnDet.JobNo=OrderDet.JobNo LEFT JOIN Estim ON VendReturnDet.PartNo=Estim.PartNo WHERE VendReturn.Status!='Complete'")
	return cursor.fetchall()

def getNonConformance(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, ISNULL(NonConformance.JobNo, '') AS JobNo, NonConformance.PartNo, NonConformance.ReturnType, ISNULL(NonConformance.CustCode, '') AS CustCode, ISNULL(NonConformance.VendCode, '') AS VendCode, convert(date, NonConformance.NonConfDate) AS NonConfDate, NonConformance.Status, NonConformance.NCDescrip FROM NonConformance LEFT JOIN Estim ON NonConformance.PartNo=Estim.PartNo WHERE status!='Closed'")
	return cursor.fetchall()

def getCAPA(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, ISNULL(CAR.CustRMANo, '') AS CustRMANo, CAR.CorrectiveActionCode, CAR.PartNo, convert(date, CAR.CARDate) AS CARDate, CAR.Status, CAR.Description FROM CAR LEFT JOIN Estim ON CAR.PartNo=Estim.PartNo WHERE Status!='Closed'")
	return cursor.fetchall()

def getCustReturnCount(cursor):
	cursor.execute("SELECT COUNT(*) AS NumCustReturn FROM CustReturn JOIN CustReturnDet ON CustReturn.CustRMANo=CustReturnDet.CustRMANo WHERE CustReturn.Status!='Complete' AND CustReturn.Status!='Refused'")
	return cursor.fetchone()[0]

def getVendorReturnCount(cursor):
	cursor.execute("SELECT COUNT(*) AS NumVendReturn FROM VendReturn LEFT JOIN VendReturnDet ON VendReturn.VendReturnNo=VendReturnDet.VendReturnNo WHERE VendReturn.Status!='Complete'")
	return cursor.fetchone()[0]

def getNonConformanceCount(cursor):
	cursor.execute("SELECT COUNT(*) AS NumNonConformance FROM NonConformance WHERE Status !='Closed'")
	return cursor.fetchone()[0]

def getCAPACount(cursor):
	cursor.execute("SELECT COUNT(*) AS NumCAPA FROM CAR WHERE Status!='Closed'")
	return cursor.fetchone()[0]