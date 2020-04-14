COMPANY Z DASHBOARD
8/17/18


==============================
-----------CONTENTS-----------
==============================
-Description
-Setup
-Running the App
-Using the App
-Content Organization
-Writing New Methods
-Changing Color Theme
-Changing Company Logo and Icon
-SQL Explanations
-Issues



===============================
----------DESCRIPTION----------
===============================

CoZDashboard is a web app that works alongside of E2 Shoptech system. It hosts a website that anyone on the local network can access. The site displays data on orders, shipments, PO's, quality issues, and overall company performance in a quick and convenient fashion. Users are able to select relevant queries (such as 'display late jobs only') and quickly search and sort table data. 

Benefits: 
+ much faster than E2
+ clear visual displays
+ no limit on number of users
+ can be accessed by any machine on the local network through a browser
+ users don't have to download any files or set up anything
+ search/sort is client sided, doesn't burden servers
+ very, very light hardware requirements.
	+ can be hosted on a computer running Windows XP with no performance issues





=========================
----------SETUP----------
=========================

Required components:
- Python 3.4.4+
	- pip should come with Python automatically
- ODBC Driver <ver> for SQL Server  or  SQL Server Native Client <ver>
- Flask 1.0.2+
- Microsoft .NET Framework 4+

NOTE1: Setup on a Windows computer is recommended due to potential issues with compatibility with MS SQL Server.

NOTE2: If the computer is super old, you may need to install Windows Installer version 4.5+ from the Microsoft website in order to proceed with installation.

NOTE3: Don't actually worry about version numbers, just install a recent version of everything and you'll be fine. The Toshiba laptop uses older versions of software that are compatible with Windows XP and it can still host the website perfectly.


Step by step:
- Install Python and add it to your system's PATH (found under Environment Variables)

- Open cmd as administrator and execute (type one line, then hit enter, then move onto the next) the following:

	> pip install virtualenv
	> virtualenv venv
	> venv\scripts\activate 
	(be careful not to use / for this step; it won't work)
	> pip install pyodbc

If this step fails since the computer's ODBC Driver for SQL Server version is too old, install a recent one from Microsoft's website. If the computer is also running XP, it cannot use any versions of ODBC on Microsoft's website, so instead install Microsoft SQL Server 2008 Native Client (a package that includes an older version of ODBC that works on XP) at https://www.microsoft.com/en-us/download/details.aspx?id=16978. 

- Still in cmd, execute 
	> pip install flask

After this step finishes, the cmd window can be closed.

- Using a text editor, open CoZDashboard/pyodbcmethods. It should read something like this:


def connect():
	import pyodbc
	server = '<SQL server name>' 
	database = '<Database name>' 
	username = '<user, using sa is recommended>' 
	password = '<password>' 
	driver = 'ODBC Driver 13 for SQL Server' 

	cnxn = pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor() 
	return cursor


Adjust server, database, username, and password as needed. Connecting to the database with the sa account is recommended to avoid potential issues with table viewing privileges. 

You will most likely need to change the driver variable to match the host computer's ODBC driver version. For example, on this laptop, it reads:

	driver = 'ODBC Driver 13 for SQL Server'

on the Toshiba laptop, that line reads:

	driver = SQL Server Native Client 10.0

To check the driver name to type in, go to 'ODBC Data Source Administrator', navigate to the 'Drivers' tab, and check the name of the driver the computer is using. Replace the name of the driver in the code with what the computer is using. Make sure you keep the quotation marks around the name.

After this, the site should be ready to run.





===================================
----------RUNNING THE APP----------
===================================

8/22/18 Update: run.bat written

NEW STEPS TO START UP THE SERVER:
On the host computer (preferably Windows; Mac not tested):
1. TO START HOSTING THE WEBSERVER: In the CoZDashboard folder, open 'run.bat'

2. run.bat will execute ipconfig and start up the app server for you. Keep the cmd window open!

3. Access the site through any internet browser on any device at: 
	<local IPv4 Address of host machine>:5000 
		- This IP address should be in the list printed by ipconfig.
		- Users do NOT need to download anything to access the site. Only the host computer needs to go through the setup process.

4. TO STOP HOSTING: In cmd, press 'ctrl' + 'c' at the same time. cmd will print: 
	(venv) C:/.../CoZDashboard>
This signifies that the Flask server has been stopped and that the cmd window can be closed safely.

To start up the server again, just open 'run.bat' again.

The rest of this section contains a more detailed explanation on manual setup. It can be skipped if run.bat works.


MANUAL SETUP:
On the host machine:
1. Run Command Prompt as an administrator.
2. Navigate to CoZDashboard using:
	> cd <name of next folder>
3. Execute:
	> venv\scripts\activate
4. Execute:
	> python __init__.py --host=0.0.0.0

	notes: --host=0.0.0.0 is needed to make the app discoverable on the local network. Without it, you will be able to access the app on your local machine but not the local network. 

5. Leave the cmd window open. Access the webpage through a web browser at:

	<this IP address>:5000/orders

Note1: URLs are case sensitive.
Note2: It's a good idea to set up a static IP address for the host machine for convenience.

To find the machine's current IP address: 
	Open cmd
	Execute:
		ipconfig
	Check the machine's current IPv4 address.

6. TO EXIT: Press 'ctrl' + 'c' in the cmd window to stop hosting (don't need to hit enter). After that, the cmd window can be closed safely.


Step by step: (in cmd)

What to Run
								Output
-----------
								------------
(start up cmd as administrator)	
								C:\Windows\system32
cd ..
								C:\Windows>
cd ..
								C:\
cd Users
								C:\Users
cd myName
								C:\Users\myName
cd CoZDashboard
								C:\Users\myName\CoZDashboard
venv\scripts\activate
								(venv) C:\Users\myName\CoZDashboard
python __init__.py --host=0.0.0.0
								* Serving Flask App "__init__" (lazy loading)... 
(website can be accessed now)





=================================
----------USING THE APP----------
=================================

Once the web app is being hosted successfully, users must be on the same local network to connect to the website on <host IP address>:5000/orders. Users can use any web browser to access the site. Note that older versions of Internet Explorer may not display the site correctly.

There are several general categories of information: Orders, Shipments, Quality, Vendors (Purchase Orders), and Stats. Stats displays a dashboard of many graphs that indicate general performance of the company. The rest display a table of data. To navigate between these categories, use the buttons on the navbar at the top.

Underneath each category, there are several possible queries that can be performed and displayed. You can select a specific query using the grey dropdown menu next to the page's heading. For example, on the Orders page, you can click on 'Orders: Late' and the table will then display only late orders (past their due date). Each of these queries has a specific URL and can be bookmarked.

Next to the grey dropdown, there is a help button that contains relevant information about the page. 

Tables:
Tables can be searched and sorted. To search a table, type anything into the searchbar and results will be filtered out in real time with each key press. (e.g. searching '123' will show jobs 12345-01, 12345-02, 12346-01, etc.) To perform an exact search for a phrase, type '!' and then your search query (e.g. searching '!1' will show all jobs with quantity 1 but not jobs with 1 somewhere in their order/job number since those aren't exact matches). To sort a table, click on a column header to sort by that column. Click on that header again to reverse sort by that column. If you wish to sort by multiple columns, shift click on secondary column headers to sort by those as well.

Graphs:
This app uses Google Charts to draw display data. Hovering over portions of the pie charts and bar graphs will display more detail about that data entry. Elements will automatically adjust positions if the page is zoomed in or out. The dashboard will also automatically adjust to any display size and aspect ratio.

Job Numbers:
Users can click on job numbers to access a dynamic webpage that displays a timeline of the entire job and a table containing details on each of its steps. Some job numbers will not be clickable since they do not exist in the JobRouting database, which means no details can be displayed for that job.

Part Numbers:
Users can access drawing files through part numbers. To do this, users must right click on a part number link, select 'Copy Link Address', and paste and go in a new browser window. Users may be able to access these files directly by left clicking on the part number, but Chrome and other more modern browsers disallow websites and their HTML from accessing your computer's files directly for security reasons. However, if the user initiates the action, the command is trusted and executed normally.

NOTE1: This features will only work if users had access to the server with the drawings folder beforehand.

NOTE2: Drawings are pulled from the Estim.DrawingFileName in the SQL server. The file path of each drawing must be available in the 'Image' tab of the part in E2 before it appears on the website. If it is not there, no link can be created. After users manually input the file path into the image tab (usually it can be found under the part's documents tab), refreshing the dashboard should show a blue, clickable link for that part number instead of plain black text.




========================================
----------CONTENT ORGANIZATION----------
========================================

Folders:
CoZ Dashboard/
	- __pycache__/
	- static/
		- __jquery.tablesorter
		- images/
		- themes/
		- orders.js
		- style.css
	- templates/
		-orders.html
		-ordersbehindschedule.html
		-pos.html
		-pospurchasing.html
		...
	- venv/
	- __init__.py
	- ordersmethods.py
	- posmethods.py
	- pyodbcmethods.py
	...
	- README.txt
	- run.bat
	...

Overview:
- run.bat will automatically start up the server for you.
- Don't touch the folders '__pycache__' and 'venv'

- There are four types of files used by the website: .py, .HTML, .css, .js
- __init__.py starts up the entire site and calls on everything else. For each URL, it renders an HTML template and passes in values to fill in the blanks of the template with.
- <category>methods.py files contain all methods used in __init__.py. They are python methods that execute SQL queries and return the results as pyodbc.row objects. Rows can be thought of as arrays, so the results set is like a 2D array.
- templates/ contains HTML files that use Jinja. Jinja lets you put logic and variables into HTML files inside curly brackets {{}}. 
- static/ contains the .css and .js files used by all HTML files. These make the site pretty and the tables searchable/sortable.

Summary: When a user accesses a URL on the local web server hosted by Flask, Flask renders the requested HTML page by inserting the results of SQL queries from <category>methods.py into the empty tables.

Detailed explanation:
------------------------------
__init__.py is the file that starts the site up up. It contains methods like this:

-1	import pyodbc
0	from ordersmethods import getJobsInProgress
...
1	@app.route('/orders')						
2	def getOrders():							
3		cursor = connect()						
4		result = getJobsInProgress(cursor)		
5		return render_template('orders.html', table1=result, tabletype="In Progress")

0: At the top of document, imports all methods used below 
1: Creates a new page URL. You can visit this page at <this machine's IP address>:5000/orders.
2. When the page is visited, Flask runs this method to create the page.
3. connect() defines a cursor, which tells later methods where to execute their SQL queries.
4. Calls on a Python method which executes a SQL query at the cursor and returns its results
5. the flask method return_template(<html file>, var1=<other var>, ...) creates the webpage displayed by passing in variable values to fill in the blanks of the template.
--------------------------------
- ordersmethods.py contains methods like this:

def getJobsInProgress(cursor):
	cursor.execute("SELECT Estim.DrawingFileName, Orders.CustCode, Orders.PONum, OrderDet.JobNo, OrderDet.PartNo...")
	return cursor.fetchall()

This python method uses pyodbc's execute method to execute an SQL query at the cursor. In __init__.py, we imported pyodbc and defined a cursor with connect() before calling on this method. This query gives a result in SQL. The cursor.fetchall() method converts the SQL results into Python by creating a array of pyodbc.row objects, where each column is an object attribute. The method returns that array. In this case, it will be:
[row0, row1, row2...]
where 
row0:[<filename>, <companyname>, <PONum>, <JobNo>, <PartNo>, ... ],
row1:[...]
and etc.

From the Python side of things, the values of these rows can be accessed in two ways. Let result=cursor.fetchall():
1. result[0][0] returns row0's filename by treating row objects like arrays
2. result[0].DrawingFileName returns row0's filename by calling on one of the row's attributes
This project uses the 2nd method since it is much more readable and allows adding/deleting queries without ruining every column that comes after it.
--------------------------------
-orders.html contains tables like this: 

<div class="orders_table_container">
  <table class="orders_table" class="tablesorter" id="searchtable" class="flex-container">
    <thead>
      <tr>
        <th>Customer</th>
        ...
        <th>Order Comments</th>
      </tr>
    </thead>
    <div>
      <tbody>
        {% for row in table1 %}
          <tr>
            <td>{{row.CustCode}}</td>
            ...
            <td class="Comments">{{row.OrderComments}}</td>
          </tr>
        {% endfor %}
      </tbody>
    </div>
  </table>
</div>

Note the curly brackets {{}} that signify Jinja inserting something into the template. Jinja logic statements (like {% for row in table1 %}) are surrounded by single brackets, while variable insertions are in double brackets (like {{row.CustCode}}).

In __init__.py, "render_template('orders.html', table1=results, tabletype='In Progress')" passes the SQL query results into the template as "table1", an array of pyodbc.row, which is essentially a 2D array. The template then creates an HTML table row (<tr>) for each pyodbc.row in 'table1'. Then for each HTML column (<td>), it inserts a specific column's value from the pyodbc.row.

Important note: while the HTML seems janky this specific structure allows other features to function. The div around <tbody> is what allows the table to be vertically scrollable while hiding the vertical scrollbar that ruins the alignment of all columns. The <thead> and <tbody> tags, which seem redundant with <th> and <td>, are needed for the TableSorter package to function.

Every single table on the website follows this structure.  





=======================================
----------WRITING NEW METHODS----------
=======================================

Summary: every change needs changes in 3 locations: '<sometype>methods.py', '__init__.py', and 'correspondingHTMLfile.html'

Adding onto an existing table:

1. Go to the corresponding methods file (e.g. 'ordersmethods.py') and write the new method. Follow the same structure as other methods:
	def methodName(cursor):
		cursor.execute("SELECT <new thing> AS newColumnNameFromSQLQuery...")
		return cursor.fetchall()

2. Go to __init__.py. Import the new method and create the new site:
	(at the top): 
	import getJobsInProgress, ... newMethodName FROM ordersmethods

	(below):
	@app.route('/orders/urlfornewmethod')
	def getOrders():
		cursor = connect()
		result = newMethodName(cursor)
		return render_template('orders.html', table1=result, tabletype="What You Want The Grey Button to Display") 

3. Update the HTML file if needed with more columns.

	e.g.
	<th>Customer</th>
	<th>Thing that New Method Returns</th>

	and below:

	<td>{{row.CustCode}}</td>
	<td>{{row.newColumNameFromSQLQuery}}</td>

	Follow the structure of existing HTML pages if writing a new page. Note the curly brackets {{}} that signify Jinja.

4. Update all other HTML files in that category (e.g. Orders) with a button in the dropdown menu that links to the new page
	<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
      <a class="dropdown-item" href="/orders/inprogress">In Progress</a>
      <a class="dropdown-item" href="/orders/newmethodname">New Method Name</a>

Note: If creating a completely new HTML file, it is highly recommended to copy paste another page's HTML and then altering the column names, what gets inserted, etc. without changing the existing HTML structure. Structure must be maintained strictly for table search and column sort to work.

----------------------------------------------


Creating a new Google Chart in the Stats page:

1. Write the new method in statsmethods.py 
	def sampleMethod(cursor):
		cursor.execute("SELECT COUNT <new thing> AS newColumnNameFromSQLQuery...")
		return cursor.fetchone()[0]

		(note: fetchone returns 1 row. [0] then accesses the first element of that row, which is the number of things the sample method counted)

2. In __init__.py: at the top of the page, import the new method

	from statsmethods import ..., sampleMethod

3. In __init__.py: under @app.route('/stats') pass the new statistic into the HTML page with render_template

	return render_template('stats.html', 
		#Pie Chart: Job On Time Rate (All)
		onTimeDelivery = getOnTimeDelivery(cursor), 
		allDelivery = getAllDelivery(cursor), 
		...

		#Pie Chart: Sample New Chart
		varSampleThatGetsPassedIn = sampleMethod(cursor)


	Note1: You may have to repeat steps 1-4 to pass if your new Google Chart needs multiple new variables
	Note2: You can directly pass in the variable here without varSample1 by doing render_template(...varSampleThatGetsPassedIn = sampleMethod(cursor)) but creating a variable in a previous line and then setting the variable that gets passed in equal to it is a lot more readable.

5. In stats.html: Create a new Google chart. To do this, check here as well as the instructions below: https://developers.google.com/chart/interactive/docs/gallery
	A. make sure that you load in the needed package at the top of the script

		google.charts.load('45', {packages: ['corechart', 'gauge', 'bar', '<samplepackage>']})

	B. Skip past the script for now and create a div where you want the graph to be:

		<div class="card border-primary">  
		  <div class="card-header border-primary">Sample Statistic</div>
		  <div id="<SampleNewChart>"</div>
		</div>

		Make sure that the ID is unique. 

	C. inside <script>, write the new function to draw the graph in the new div you just created. Items that you must input are highlighted with <>. Check the Google Charts documentation to see how this part should look. This example creates a pie chart.

		function <drawSampleChart()> {
																	//Name this function
		  var data = new google.visualization.DataTable();

		  data.addColumn('<string>', '<POs>');
		  															//Create two columns with data.addColumn('datatype', 'name')
		  data.addColumn('<number>', '<Quantity>');
		  data.addRows([
		  															//Create as many rows as needed in here with ['Data1', 'Data2']. 
		    ['<On Time>', {{vendorOnTimeDelivery}}],
		    														//Pass in the variable you added to render_template in step 4 inside {{}}
		    ['<Late>', {{varSampleThatGetsPassedIn}}],
		  ]);
		  var options={
		    ...
		    														//Customize the chart with options. Check Google's documentation for this.
		  };
		  // Instantiate and draw the chart.
		  var chart = new google.visualization.PieChart(document.getElementById('<SampleNewChart>'));
		  															//Draw the chart in the div you created in step B
		  chart.draw(data, options);
		}

	D. Tell Google to load the graph after everything else has been loaded with setOnLoadCallBack. Pass in the name of the function you created in Step C.

		google.charts.setOnLoadCallback(drawPieChartDelivery);
		google.charts.setOnLoadCallBack(<drawSampleChart>);


With this, your chart should be ready for viewing. Access the page and check how it looks.
NOTE: If something goes wrong in a single chart, all charts won't display. Don't worry if the entire page seems to break. 

Things to watch out for:
Puncutation! Check commas and semicolons.
Division for percentages: Do that in the <script> section of Google Charts to avoid rounding errors when passing numbers into the templates.






==========================================
----------CHANGING COLOR THEMES-----------
==========================================

Color themes are stored in CoZDashboard/static/themes/

Their contents are like this:

:root{
    --main-color:#001572; /*header1, tablehead*/
    --main-color-D:#000063; /*tablehead on hover*/
    --main-color-L:#e3f2fd; /*navbar*/
    --secondary-color:#bbdefb; /*buttons on hover*/
    --bg-color:#f2f9ff;
    --table-light-cell:#ffffff;
    --table-dark-cell:#f2f2f2;
    --table-highlight-cell:#fff4bf;
}

They define several variables to be certain colors.
These variables are used in the main stylesheet to color the navbar and tables.

To create a new color theme, just change the hex colors in the file and save as a new name. Then, in navbar.html, change  

<link rel="stylesheet" type = "text/css" href="/static/themes/lightblue.css">

to load in your new color theme. 





===================================================
----------CHANGING COMPANY LOGO AND ICON-----------
===================================================

These assets are loaded in to every page by the navbar template, found at /templates/navbar.html. Every page extends the navbar file.

Place the new images into /static/images and then change the following lines of code:

<link rel="icon" type="image/x-icon" href="/static/images/CoZfavicon.ico">

and

<a class="navbar-brand" href="/orders"><img src="/static/images/CoZlogo.png" alt="CoZ"></img></a>

to reflect the new file names.





====================================
----------SQL EXPLANATIONS----------
====================================

Some commonly reoccurring expressions in SQL statements executed aren't even explained in comments since it would be redundant and messy. Instead, they will be explained here.

1. "GETDATE()":
Gets the current date and time, e.g. 8/23/2018 15:09:24.5243


2. "CONVERT(DATE, <today's date or due date>)":
Used to convert datetime objects into date alone. Reasoning: Suppose a job is due on 8/23/2018 and today is 8/23/2018, 2:46 PM, and we want to check whether jobs are late. Using the expression (DueDate < GETDATE()) would evaluate to false since the due date 8/23 is evaluated as 8/23/2018 00:00:00 while GETDATE() would return 8/23/2018 14:46:00. This method would return everything due today as 'Late', which is not desired.

However, CONVERT(DATE, GETDATE()) would get rid of today's time and return 8/23/2018 alone. 8/23/2018 behaves like 8/23/2018 00:00:00. The expression (CONVERT(DATE, DueDate) < CONVERT(DATE, GETDATE())) would correctly evaluate to 'False' and the job would not be counted as late.

Note: DueDates are actually stored as datetime objects with time 0 in a lot of cases. So a job due 8/23/2018 would have a DueDate of 8/23/2018 00:00:00 in the database, and you would only need to do (DueDate < CONVERT(DATE, GETDATE())) to obtain the same results as above.


3. cursor.execute("SELECT ... WHERE DueDate > ? AND DueDate < ?", (startdate), (enddate))
Python methods can substitute variables into the place of the question marks. By passing in variables when calling on the function, you can use one method to find statistics for any period of time.



4. "WHERE DueDate >= DATEADD(qq, DATEDIFF(qq, 0, DATEADD(qq, ?, GETDATE()-1))...", (-qtrsago), (-qtrsago+1)
qq is a quarter. This method takes advantage of rounding errors in SQL's inbuilt DATEDIFF method (which truncates down) to determine the start date of a quarter. It honestly isn't important to know how this works, so you can skip the rest of this paragraph. But if you want to, the explanation is below.

Let's suppose we're trying to find this quarter's dates. The inner DATEADD() subtracts a variable number of quarters from today. We would set this variable to be 0 since we want this quarter. DATEDIFF(qq, GETDATE()-1), 0) would then find the number of quarters, rounded down, between the start of SQL time and yesterday (the reason we use yesterday is because there's no point in displaying the qtr data on the day of a new qtr when there is no data yet). By adding that difference to the beginning of SQL time, we will get the date of the beginning of this quarter.

So to find this quarter's start and end date, we pass in (-qtrsago) = 0 and then (-qtrsago+1) = 1 to the method. This returns this quarter's start, and then next quarter's start (or this quarter's end).


5. ISNULL(ActualStartDate, '')
Trying to insert null objects into the table is bad. It either displays a blank box, the string 'None', or breaks something so the website can't render the table. This expression here replaces the query output with a blank string instead of a null object if there is no ActualStartDate. This is used on all columns where a null output is a possibility to keep those columns on the table empty without breaking anything. 


5. CASE WHEN... THEN ____ ELSE ____ END
essentially an if else statement in SQL. For example to fill the PO comments column in case there are no comments in PODet, WHEN (POJobComments IS NOT NULL) THEN POJobComments ELSE POComments END. 

NOTE: Smaller queries (less columns) are faster. This is preferable to returning both POJobComments and POComments from the query and then using python/Jinja to select one or the other later on.  





==========================
----------ISSUES----------
==========================

- Mobile display is cramped, difficult to read
	- Tables automatically adjust to size of screen. However, with mobile displays, table divisons shrink smaller than individual words in their labels, so entries overflow from their column
		-Fixed 8/20; screens with width < 800px default to a fixed 800px wide table that users can scroll across.
		