import pyodbc #allows python methods to execute SQL queries
from flask import Flask, render_template, redirect #allows use of HTML templates and hosting local webserver
#user-defined methods below:
from pyodbcmethods import connect #establishes cursor for future SQL queries
#python methods that execute SQL queries below:
from ordersmethods import getJobsInProgress, getJobsLate, getAssembliesLate, getJobsBehindSchedule, getAssembliesBehindSchedule, getJobsDueToday, getJobsDueTomorrow, getJobsDueThisWeek, getJobSteps #getJobStats
from shipmentmethods import getShipmentsToday, getShipmentsPastWeek, getShipmentsReadyToShip
from posmethods import getAllPOs, getAllPOs1Week, getAllPOs2Week, getAllPOs1Month, getLatePOs, getRejectedPOs, getJobsNeedPurchasing, getAllJobsPerVendorAllTime, getAllJobsPerVendorFromXMonthsAgo, getAllVendorOrdersNum, getAllVendorLateOrdersNum, getAllPOsNum, getLatePOsNum
from qualitymethods import getCustomerReturnStatus, getVendorReturnStatus, getNonConformance, getCAPA, getCustReturnCount, getVendorReturnCount, getNonConformanceCount, getCAPACount
from statsmethods import getPartsScrapped_PartsGoodQtrXAgo, getJobsInProg_Late_BehindSched_Count, getJobsDueToday_Tomorrow_ThisWeek_Count, getOnTimeDelivery, getAllDelivery, getQuotesWon, getQuotesLost, getQuotesExpired, getCustSurveyQtrXAgo, getQtrXAgoDateStart_End, getVendJobsLateQtrXAgo, getVendJobsTotalQtrXAgo, getVendPartsRejectedQtrXAgo, getCoZPartsRejectedQtrXAgo, getCoZTotalPartsQtrXAgo, getCoZJobsLateQtrXAgo, getCoZJobsTotalQtrXAgo

app = Flask(__name__)
#app.config['TESTING'] = False
#uncomment this when deploying - disables debugging when errors occur

@app.route('/')
def test1():
	return redirect('/orders')

#Page: Orders
@app.route('/orders')
def getJobsInProgress1(): #queryname1 to avoid naming conflicts, but still easy to recognize 
	cursor = connect() #pyodbcmethods.connect establishes cursor for future SQL queries
	result = getJobsInProgress(cursor) #ordersmethods.getJobsInProgress(cursor) uses pyodbc's execute('') method to execute SQL queries and fetchall() to return the results of the query as pyodbc.row objects, which can be treated like arrays
	return render_template('orders.html', table1=result, tabletype="In Progress") #Jinja passes the results of the queries into the HTML table

@app.route('/orders/late')
def getJobsLate1():
	cursor = connect()
	result = getJobsLate(cursor)
	return render_template('orders.html', table1=result, tabletype="Late")

@app.route('/orders/lateassemblies')
def getAssembliesLate1():
	cursor = connect()
	result = getAssembliesLate(cursor)
	return render_template('orders.html', table1=result, tabletype="Late Assemblies")

@app.route('/orders/behindschedule')
def getJobsBehindSchedule1():
	cursor = connect()
	result = getJobsBehindSchedule(cursor)
	return render_template('ordersbehindschedule.html', table1=result, tabletype='Behind Schedule')

@app.route('/orders/behindscheduleassemblies')
def getAssembliesBehindSchedule1():
	cursor = connect()
	result = getAssembliesBehindSchedule(cursor)
	return render_template('ordersbehindschedule.html', table1=result, tabletype='Behind Schedule Assemblies')

@app.route('/orders/duetoday')
def getJobsDueToday1():
	cursor = connect()
	result = getJobsDueToday(cursor)
	return render_template('orders.html', table1=result, tabletype="Due Today")

@app.route('/orders/duetomorrow')
def getJobsDueTomorrow1():
	cursor = connect()
	result = getJobsDueTomorrow(cursor)
	return render_template('orders.html', table1=result, tabletype="Due Tomorrow")

@app.route('/orders/duethisweek')
def getJobsDueThisWeek1():
	cursor = connect()
	result = getJobsDueThisWeek(cursor)
	return render_template('orders.html', table1=result, tabletype="Due This Week")

@app.route('/orders/jobs/<JobNo>')
def getJobSteps1(JobNo):
	cursor = connect()
	result = getJobSteps(cursor, JobNo)
	if not result: #if the query returns an empty list
		return render_template('error.html', message = 'Job ' + JobNo + ' could not be found in OrderRouting database!')
	#else show job steps from orderrouting for that user
	return render_template('ordersjobsteps.html', table1=result)

#Page: Vendors
@app.route('/vendors')
def getPOs1():
	cursor = connect()
	result = getAllPOs(cursor) #misnamed, actually gets active POs only
	return render_template('pos.html', table1=result, tabletype="All Active PO's")

@app.route('/vendors/1week')
def getPOs1Week1():
	cursor = connect()
	result = getAllPOs1Week(cursor)
	return render_template('pos.html', table1=result, tabletype="All Active PO's Due Within a Week")

@app.route('/vendors/2week')
def getPOs2Week1():
	cursor = connect()
	result = getAllPOs1Week(cursor)
	return render_template('pos.html', table1=result, tabletype="All Active PO's Due Within 2 Weeks")

@app.route('/vendors/1month')
def getPOs1Month1():
	cursor = connect()
	result = getAllPOs1Month(cursor)
	return render_template('pos.html', table1=result, tabletype="All Active PO's Due Within a Month")

@app.route('/vendors/late')
def getPOsLate():
	cursor = connect()
	result = getLatePOs(cursor)
	return render_template('pos.html', table1=result, tabletype="Late Active PO's")

@app.route('/vendors/rejected')
def getPOsRejected():
	cursor = connect()
	result = getRejectedPOs(cursor)
	return render_template('posrejected.html', table1=result, tabletype="Rejected PO's")

@app.route('/vendors/purchasing')
def getJobsNeedPurchasing1():
	cursor = connect()
	result = getJobsNeedPurchasing(cursor)
	return render_template('pospurchasing.html', table1=result, tabletype="Jobs that Need Purchasing")


#returns number of PO jobs on time, late, and rejected for each vendor within the specified time period
@app.route('/vendors/stats')
def getVendorStats():
	cursor = connect()
	result = getAllJobsPerVendorAllTime(cursor)
	return render_template('posvendors.html', table1=result, tabletype="Vendor Stats: All Time")

@app.route('/vendors/stats/3months')
def getVendorStats3Months():
	cursor=connect()
	result = getAllJobsPerVendorFromXMonthsAgo(cursor, 3)
	return render_template('posvendors.html', table1=result, tabletype="Vendor Stats: 3 Months")

@app.route('/vendors/stats/6months')
def getVendorStats6Months():
	cursor=connect()
	result = getAllJobsPerVendorFromXMonthsAgo(cursor, 6)
	return render_template('posvendors.html', table1=result, tabletype="Vendor Stats: 6 Months")

@app.route('/vendors/stats/12months')
def getVendorStats12Months():
	cursor=connect()
	result = getAllJobsPerVendorFromXMonthsAgo(cursor, 12)
	return render_template('posvendors.html', table1=result, tabletype="Vendor Stats: 12 Months")

#Page: Quality
@app.route('/quality/customerreturns')
def  getCustomerReturnStatus1():
	cursor = connect()
	result = getCustomerReturnStatus(cursor)
	return render_template('qualitycustreturns.html', table1=result, tabletype="Open Customer Returns")

@app.route('/quality/vendorreturns')
def getVendorReturnStatus1():
	cursor = connect()
	result = getVendorReturnStatus(cursor)
	return render_template('qualityvendorreturns.html', table1=result, tabletype="Open Vendor Returns")

@app.route('/quality/nonconformance')
def getNonConformance1():
	cursor = connect()
	result = getNonConformance(cursor)
	return render_template('qualitynonconformance.html', table1=result, tabletype='Non-Conformance Issues')

@app.route('/quality/capa')
def getCAPA1():
	cursor = connect()
	result = getCAPA(cursor)
	return render_template('qualitycapa.html', table1=result, tabletype='Corrective and Preventative Actions')

#Page: Shipments
@app.route('/shipments')
def getShipments1():
	cursor = connect()
	result = getShipmentsToday(cursor)
	return render_template('shipments.html', table1=result, tabletype='Today\'s Shipments')

@app.route('/shipments/week')
def getShipmentsPastWeek1():
	cursor = connect()
	result = getShipmentsPastWeek(cursor)
	return render_template('shipments.html', table1=result, tabletype='This Week\'s Shipments')

@app.route('/shipments/ready')
def getShipmentsReadyToShip1():
	cursor = connect()
	result = getShipmentsReadyToShip(cursor)
	return render_template('shipmentsready.html', table1=result, tabletype='Jobs Ready To Ship')

#Page: Stats
@app.route('/stats')
def getStats1():
	cursor = connect()
	return render_template('stats.html', 
		#Pie Chart: Job On Time Rate (All)
		onTimeDelivery = getOnTimeDelivery(cursor), 
		allDelivery = getAllDelivery(cursor), 

		#Pie Chart: Vendor On Time Deliveries
		vendorLateDelivery = getLatePOsNum(cursor), 
		vendorOnTimeDelivery = getAllPOsNum(cursor) - getLatePOsNum(cursor), 

		#Pie Chart: Quotes
		quotesWon = getQuotesWon(cursor), 
		quotesLost = getQuotesLost(cursor), 
		quotesExpired = getQuotesExpired(cursor), 

		#Pie Chart: Behind Schedule uses jobsinprog and jobsbehindsched from below

		#Order Stats Bar
		jobsinprog = getJobsInProg_Late_BehindSched_Count(cursor)[0], 
		jobslate = getJobsInProg_Late_BehindSched_Count(cursor)[1], 
		jobsbehindschedule = getJobsInProg_Late_BehindSched_Count(cursor)[2], 
		jobsduetoday = getJobsDueToday_Tomorrow_ThisWeek_Count(cursor)[0], 
		jobsduetomorrow = getJobsDueToday_Tomorrow_ThisWeek_Count(cursor)[1], 
		jobsduethisweek = getJobsDueToday_Tomorrow_ThisWeek_Count(cursor)[2], 
		
		#Customer Return Stats Bars
		openCustomerReturns = getCustReturnCount(cursor), 
		openVendorReturns = getVendorReturnCount(cursor), 
		openNonConformance = getNonConformanceCount(cursor), 
		openCorrectiveActions = getCAPACount(cursor), 

		#Vendor Stats Bar && Pie Chart: Vendor Late Rate (All)
		totalPO = getAllVendorOrdersNum(cursor), totalPOLate = getAllVendorLateOrdersNum(cursor), 

		#Bar Graph: Customer Survey Metric (quarterly), quarter dates actually used in all quarterly bar graphs
		thisQtrStartDate = getQtrXAgoDateStart_End(cursor, 0)[0], thisQtrEndDate = getQtrXAgoDateStart_End(cursor, 0)[1], 
		qtr1AgoStartDate = getQtrXAgoDateStart_End(cursor, 1)[0], qtr1AgoEndDate = getQtrXAgoDateStart_End(cursor, 1)[1], 
		qtr2AgoStartDate = getQtrXAgoDateStart_End(cursor, 2)[0], qtr2AgoEndDate = getQtrXAgoDateStart_End(cursor, 2)[1], 
		qtr3AgoStartDate = getQtrXAgoDateStart_End(cursor, 3)[0], qtr3AgoEndDate = getQtrXAgoDateStart_End(cursor, 3)[1], 
		
		#Bar Graph: Customer Survey Metric (quarterly)
		custSurveyThisQtr = getCustSurveyQtrXAgo(cursor, 0)[0], 
		custSurveyQtr1Ago = getCustSurveyQtrXAgo(cursor, 1)[0], 
		custSurveyQtr2Ago = getCustSurveyQtrXAgo(cursor, 2)[0], 
		custSurveyQtr3Ago = getCustSurveyQtrXAgo(cursor, 3)[0], 

		#Bar Graph: Vendor Job Late Rate (qtr)
		vendLateThisQtr = getVendJobsLateQtrXAgo(cursor, 0), 
		vendLateQtr1Ago = getVendJobsLateQtrXAgo(cursor, 1), 
		vendLateQtr2Ago = getVendJobsLateQtrXAgo(cursor, 2), 
		vendLateQtr3Ago = getVendJobsLateQtrXAgo(cursor, 3), 
		#vendor total jobs each qtr
		vendThisQtr = getVendJobsTotalQtrXAgo(cursor, 0), 
		vendQtr1Ago = getVendJobsTotalQtrXAgo(cursor, 1), 
		vendQtr2Ago = getVendJobsTotalQtrXAgo(cursor, 2), 
		vendQtr3Ago = getVendJobsTotalQtrXAgo(cursor, 3), 

		#Bar Graph: Vendor Parts Reject Rate (Qtr)
		#[0] is total parts rejected, [1] is total parts made in the qtr
		vendPartsRejectedThisQtr = getVendPartsRejectedQtrXAgo(cursor, 0), 
		vendPartsRejectedQtr1Ago = getVendPartsRejectedQtrXAgo(cursor, 1), 
		vendPartsRejectedQtr2Ago = getVendPartsRejectedQtrXAgo(cursor, 2), 
		vendPartsRejectedQtr3Ago = getVendPartsRejectedQtrXAgo(cursor, 3), 

		#Bar Graph: CoZ Part Reject Rate (Qtr)
		CoZPartsRejectedThisQtr = getCoZPartsRejectedQtrXAgo(cursor, 0), 
		CoZPartsRejectedQtr1Ago = getCoZPartsRejectedQtrXAgo(cursor, 1), 
		CoZPartsRejectedQtr2Ago = getCoZPartsRejectedQtrXAgo(cursor, 2), 
		CoZPartsRejectedQtr3Ago = getCoZPartsRejectedQtrXAgo(cursor, 3), 
		CoZTotalPartsThisQtr = getCoZTotalPartsQtrXAgo(cursor, 0), 
		CoZTotalPartsQtr1Ago = getCoZTotalPartsQtrXAgo(cursor, 1), 
		CoZTotalPartsQtr2Ago = getCoZTotalPartsQtrXAgo(cursor, 2), 
		CoZTotalPartsQtr3Ago = getCoZTotalPartsQtrXAgo(cursor, 3), 

		#Bar Graph: CoZ Job Late Rate (Qtr)
		CoZJobsLateThisQtr = getCoZJobsLateQtrXAgo(cursor, 0), 
		CoZJobsLateQtr1Ago = getCoZJobsLateQtrXAgo(cursor, 1), 
		CoZJobsLateQtr2Ago = getCoZJobsLateQtrXAgo(cursor, 2), 
		CoZJobsLateQtr3Ago = getCoZJobsLateQtrXAgo(cursor, 3), 
		CoZJobsTotalThisQtr = getCoZJobsTotalQtrXAgo(cursor, 0), 
		CoZJobsTotalQtr1Ago = getCoZJobsTotalQtrXAgo(cursor, 1), 
		CoZJobsTotalQtr2Ago = getCoZJobsTotalQtrXAgo(cursor, 2), 
		CoZJobsTotalQtr3Ago = getCoZJobsTotalQtrXAgo(cursor, 3), 

		#Bar Graph: % Parts Scrapped (Qtr)
		#[0] is parts scrapped, [1] is total parts made
		partsScrappedThisQtr = getPartsScrapped_PartsGoodQtrXAgo(cursor, 0)[0], 
		partsScrappedQtr1Ago = getPartsScrapped_PartsGoodQtrXAgo(cursor, 1)[0], 
		partsScrappedQtr2Ago = getPartsScrapped_PartsGoodQtrXAgo(cursor, 2)[0], 
		partsScrappedQtr3Ago = getPartsScrapped_PartsGoodQtrXAgo(cursor, 3)[0], 
		partsGoodThisQtr = getPartsScrapped_PartsGoodQtrXAgo(cursor, 0)[1], 
		partsGoodQtr1Ago = getPartsScrapped_PartsGoodQtrXAgo(cursor, 1)[1], 
		partsGoodQtr2Ago = getPartsScrapped_PartsGoodQtrXAgo(cursor, 2)[1], 
		partsGoodQtr3Ago = getPartsScrapped_PartsGoodQtrXAgo(cursor, 3)[1]

		)
		#end of render_template

#starts up webserver
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
