from flask import Flask, request, render_template, redirect, url_for, session, g, flash
from flaskext.mysql import MySQL
from forms import AddIncidentForm
import time 
from Queries import Queries
from flask_table import Table, Col
from tables import ResourcesInUse, ResourcesInUse_Item, ResourcesInUseWithDistance, ResourcesInUseWithDistance_Item, GenerateReport_Table, GenerateReport_Item, ResourceStatus_ResourcesInUse, GeneResourceStatus_ResourcesInUse_Item, ResourceStatus_ResourcesRequestedByMe, GeneResourceStatus_ResourcesRequestedByMe_Item, ResourceStatus_ResourceRequestsReceivedByMe, ResourceStatus_ResourceRequestsReceivedByMe_Item, ResourceStatus_RepairsScheduledAndInProgress, ResourceStatus_RepairsScheduledAndInProgress_Item, ResourcesInUseStatus_Item, ResourcesInUseStatus

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'team49'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Letmein123!'
app.config['MYSQL_DATABASE_DB'] = 'team49'
app.config['MYSQL_DATABASE_HOST'] = 'team49.db.9939976.hostedresource.com'

mysql.init_app(app)
cursor = mysql.connect().cursor()

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
 
@app.route("/")
def root():
    return redirect(url_for('login'))

@app.route("/action", methods=['GET', 'POST'])
def parseAction():
	if request.method=="POST":
		print "**************************swwsaw"
		_type = request.args.get('type')

		print "TYPE IS", _type

		if _type == "cancel":
			_resourceid = request.args.get('id')
			query = Queries.deleteRepairRequest(_resourceid)
			cursor.execute(query)
			flash("Successfully Cancelled Repair Request!", "success")
			return redirect(url_for('mainMenu'));

		if _type == "repair":
			_resourceid = request.args.get('id')
			query = Queries.submitRepairRequest(_resourceid)
			cursor.execute(query)
			flash("Successfully Requested Resource Repair!", "success")
			return redirect(url_for('mainMenu'));
			#return query

		if _type == "return":

			#1 check for repair requests
			_resourceid = request.args.get('id')
			query = Queries.checkForRepairRequests(_resourceid)
			cursor.execute(query)
			rowcount = cursor.rowcount

			#if its in there, set status to in repair and delete it from rep req
			if rowcount > 0:
				results = cursor.fetchone()
				query = Queries.setStatusToInRepair(results[1], _resourceid)
				cursor.execute(query)

				#delete from rep requests
				query = Queries.deteFromRepairRequests(_resourceid)
				cursor.execute(query)

			#if its not, set status to available	
			else:
				print "SETTING STATUS TO AVAILABLE"
				_incidentID = request.args.get('incidentID')
				query = Queries.setStatusToAvailable(_resourceid)
				cursor.execute(query)

				#delete from requests
				query = Queries.deleteResourceFromRequestsTable(_resourceid, _incidentID)
				cursor.execute(query)

			flash("Successfully Returned Resource!", "success")
			return redirect(url_for('mainMenu'));

		if _type == "deleteResourceRequest":
			_incidentID = request.args.get('resourceID')
			_resourceid = request.args.get('incidentID')
			#_id = request.args.get('id')
			#_incidentID = request.args.get('incidentID')
			query = Queries.deletePendingResourceRequests(_resourceid, _incidentID);
			#return query
			cursor.execute(query)
			flash("Successfully Deleted Resource Request!", "success")
			print "eee"
			return redirect(url_for('mainMenu'));

		if _type == "request":

			print "its a request"

			_id = request.args.get('id')
			_incidentID = request.args.get('incidentID')

			#DO IT
			try:
				query = Queries.requestResource(_id, _incidentID);
				cursor.execute(Queries.requestResource(_id, _incidentID))
			except:
				print "error"
				pass	
			print "hiiii"	
			flash("Successfully Requested Resource!", "success")
			return redirect(url_for('mainMenu'));

		if _type == "deploy":
			_resourceid = request.args.get('resourceID')
			_incidentID = request.args.get('incidentID')
			_returnBy = request.args.get('returnBy')

			#updates status
			query = Queries.deployResource(_resourceid, _incidentID);
			cursor.execute(query)
			#deploys
			query2 = Queries.deployingResourceStatus(_returnBy, _resourceid)
			#return query2
			cursor.execute(query2)


			flash("Successfully Deployed Resource Request!", "success")
			return redirect(url_for('mainMenu'));

@app.route("/SearchResources",methods=['GET','POST'])
def search():
	currentuser = session['username'];
	cursor= mysql.connect().cursor()
	tableList = []

	if request.method=="POST":
		keyword = request.form["keyword"]
		esf = request.form["primary-esf-form"]
		loc = request.form["location"]
		incident = request.form["incident"] #fix this...might not always be there...

		
		incident_lat = None
		incident_long = None

		useIntersection = False

		#checks to see if they are not blank
		if incident != "":

			cursor.execute(Queries.getIncidentNameFromID(incident))
			incidentName = cursor.fetchone()

			g.tableTitle = "Search Results for Incident: %s" % incidentName
			cursor.execute(Queries.getLatLongOfIncident(incident))
			result = cursor.fetchone()
			incident_lat = result[0]
			incident_long = result[1]

		#Option 1 - if NO field is selected
		if keyword == "" and esf == "" and loc == "" and incident == "":
			cursor.execute(Queries.searchResourcesNothingSelected())
			results = cursor.fetchall()
			#print "RESULT:", results[1]
			rlist = []
			for r in results:

				#DRY THIS UP -- BUTTON PART
				button = None
				#if r[5] == "Available": #or IN USE
				#	button = "request"

				obj = ResourcesInUse_Item(r[0], r[1], r[2], r[3], r[4], r[5], r[6])#, button)
				rlist.append(obj)
			tableList = rlist

			removeDupesFromList(tableList)
			g.table = ResourcesInUse(tableList)
				#print g.table.distance
			useIntersection = True	

		#Option2 - search by Keyword 
		if keyword != "":
			cursor.execute(Queries.searchResourcesbyKeyword(keyword))
			results = cursor.fetchall()
			rlist = []
			for r in results:
				obj = ResourcesInUse_Item(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
				rlist.append(obj)
			if useIntersection:
				intersection = []
				for o in tableList:
					for p in rlist:
						if o == p:
							intersection.append(o)
				tableList = intersection
			else:
				tableList = rlist	

			removeDupesFromList(tableList)		
			g.table = ResourcesInUse(tableList)
			useIntersection = True	

		#Option 3 - search by ESF
		if esf != "":
			cursor.execute(Queries.searchResourcesbyESF(esf))
			results = cursor.fetchall()
			rlist = []
			for r in results:
				obj = ResourcesInUse_Item(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
				rlist.append(obj)
			if useIntersection:
				intersection = []
				for o in tableList:
					for p in rlist:
						if o == p:
							print "ADDED!"
							intersection.append(o)
				tableList = intersection
			else:
				tableList = rlist	
	
			removeDupesFromList(tableList)
			g.table = ResourcesInUse(tableList)	
			useIntersection = True	

		#Option 4 - search by Location (include condition for table) -- make sure form knows both field have to be populated (distance AND incident)
		if incident != "":
			cursor.execute(Queries.searchResourcesbyIncidentAndDistance(incident_lat, incident_long))
			results = cursor.fetchall()
			#print "results are:", results
			rlist = []
			for r in results:

				owner = r[7]
				button = None
				repairButton = None
				if r[4] == "Available" or r[4] == "In Use": #or IN USE
					button = "request"

				if owner == currentuser:
					button = "deploy"
					repairButton = "repair"
				
				#cursor.execute(Queries.getIncidentNameFromID(incident))
				#incidentName = cursor.fetchone()	

				obj = ResourcesInUseWithDistance_Item(r[0], r[1], r[2], r[3], r[4], r[5], r[6], incident, r[7], button, repairButton)
				rlist.append(obj)

			if useIntersection:
				intersection = []
				for o in tableList:
					for p in rlist:
						if o == p:
							print "ADDED!"
							intersection.append(o)
				tableList = intersection
			else:
				tableList = rlist	

			#filter out things > than loc
			if loc != "":
				filteredList = []
				for q in tableList:
					if q.distance <= float(loc):
						print "added!", q
						filteredList.append(q)
				print "got some stuff:", filteredList		
				tableList = filteredList


			#g.table = tableList				


			removeDupesFromList(tableList)
			g.table = ResourcesInUseWithDistance(tableList)
			useIntersection = True	

		print "*****"
		print "keyword: ", keyword
		print "esf: ", esf	
		print "loc: ", loc
		print "incident: ", incident

		print "incidents", incident_lat, incident_long	

		#test = request.form["test"]
		print "Proccess postes"
		print "The keyword is:", request.form["keyword"]
	
	cursor.execute("SELECT ESF_ID, DESCRIPTION from ESF")
	esf=cursor.fetchall()
	g.esf=esf

	#get incidents
	cursor.execute(Queries.getUserIncidents(currentuser))
	g.incidents = cursor.fetchall()


	return render_template("searchresource.html")


def removeDupesFromList(list):
	for i in range(len(list)):
		removed = False
		if i+1 <= len(list):
			for x in range(i+1, len(list)):
				if list[i].id == list[x].id:
					list.remove(list[x])
					removed = True
					break
					#break everything and redo
		if removed:
			removeDupesFromList(list)
			break			
    	
	return list

@app.route("/addIncident", methods=['GET','POST'])
def addIncident():
    form = AddIncidentForm()
    if form.validate_on_submit():
        #add this to DB
        
        currentuser = session['username'];
        cursor.execute(Queries.addIncident(currentuser, form.description.data, form.latitude.data, form.longitude.data))
        flash("Successfully Added Incident!", "success")
        return redirect(url_for('mainMenu'));

    flash_errors(form)
    return render_template("addIncident.html", form=form)


@app.route("/addResource")
def addResource():

    #grab ESFs
    cursor.execute(Queries.getESFs())
    esfs = cursor.fetchall()
    g.esf = esfs

    #grab COST_PER
    cursor.execute("SELECT COSTPER from COST_PER") #T49 - Use above example to put this into Queries
    g.costper = cursor.fetchall()

    #grab no of resources to generate ID:
    cursor.execute(Queries.getNextResourceID())
    try:    	
    	autoInc = cursor.fetchone()[10]
    except:
    	autoInc = 1	
    #cursor.execute("SELECT 'auto_increment' FROM INFORMATION_SCHEMA.TABLES WHERE table_name = 'RESOURCE'") #T49 - Use above example to put this into Queries
    g.resourceID = autoInc

    return render_template('addResource.html')

@app.route("/submitResource", methods=['POST'])
def submitResource():
    currentuser = session['username'];
    Name1 = session['name']
    ResourceName = request.form['resourceName-form']
    P_ESF1 = request.form['primary-esf-form'] #This is the ID of the ESF
    M_NAME = request.form['modelName-form']
    AMOUNT = request.form['cost-form']
    COST_PER = request.form['costper-form']
    #DATE_AV = time.strftime('%Y-%m-%d %H:%M:%S')
    LATITUDE = request.form['lat-form']
    LONGITUDE = request.form['long-form']

    #add this to DB
    cursor = mysql.connect().cursor()
    queryString = "INSERT INTO RESOURCE (USERNAME,NAME,P_ESF,M_NAME,AMOUNT,COST_PER,STATUS,DATE_AV,LATITUDE,LONGITUDE) values('"+currentuser+"', '"+ResourceName+"', '"+P_ESF1+"', '"+M_NAME+"', '"+AMOUNT+"', '"+COST_PER+"', 'Available',CURDATE(),'"+LATITUDE+"', '"+LONGITUDE+"');"
    cursor.execute(queryString)

    resourceID = cursor.lastrowid
    for c in request.form.getlist('capabilities-form'):
        queryString = "INSERT into RESOURCE_CAPABILTY(RES_ID,CAPABILITY) values("+str(resourceID)+",'"+str(c)+"');"
        print "Querystring for Capabilities is:", queryString
        cursor.execute(queryString)
         

    #ADD ADDITIONAL ESFS
    for esfid in request.form.getlist('additional-esfs-form'):
        queryString = "INSERT into ADDITIONAL_ESF VALUES ("+str(resourceID)+","+str(esfid)+")"
        cursor.execute(queryString)

    flash("Successfully Added Resource - %s" % (ResourceName), "success")
    #flash("Testing ERROR message Resource - %s" % (ResourceName), "danger")
    return redirect(url_for('mainMenu'));


@app.route("/login", methods=['GET', 'POST'])
def login():

    #if this is a post, authenticate the user
    error = None
    if request.method == 'POST':
        username = request.form['username'];
        password = request.form['password'];
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from USERS where Username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()

        if data is None:
            error = "Invalid Credentials. Try again."

        else:
            session['username'] = username
            session['name'] = data[2]
            return redirect(url_for('mainMenu'));     

    return render_template('login.html', error=error)

@app.route("/resourcestatus")    
def resourceStatus():
	currentuser = session['username'];
	cursor = mysql.connect().cursor()


	#FIRST ONE
	#return Queries.resourceStatus_getResourcesInUse(currentuser)

	query = Queries.resourceStatus_getResourcesInUse(currentuser)
	#return query
	cursor.execute(query)
	results = cursor.fetchall()
	resourceInUseList = []

	for r in results:
		print r
		obj = ResourcesInUseStatus_Item(r[0], r[1], r[2], r[3], r[4], r[5], r[6])#, r[6], r[7])
		resourceInUseList.append(obj)

	g.resourceInUsetable = ResourcesInUseStatus(resourceInUseList)
	'''
	try:
		cursor.execute(Queries.resourceStatus_getResourcesInUse(currentuser))
		results = cursor.fetchall()
		resourceInUseList = []
	
		for r in results:
			obj = ResourcesInUseWithDistance_Item(r[0], r[1], r[2], r[3], r[4], r[5])
			resourceInUseList.append(obj)

		g.resourceInUsetable = ResourceStatus_ResourcesInUse(resourceInUseList)
	except TypeError:
		print "No data to display..."	
		g.resourceInUsetable = None
	'''		

	#SECOND ONE
	#return Queries.resourceStatus_getResourcesRequestedByMe(currentuser)

	cursor.execute(Queries.resourceStatus_getResourcesRequestedByMe(currentuser))
	results = cursor.fetchall()
	resourcesRequestedByMe = []

	for r in results:
		obj = GeneResourceStatus_ResourcesRequestedByMe_Item(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
		resourcesRequestedByMe.append(obj)

	g.resourcesRequestedByMeTable = ResourceStatus_ResourcesRequestedByMe(resourcesRequestedByMe)





	#THIRD
	query = Queries.resourceStatus_getResourcesReceivedByMe(currentuser)
	cursor.execute(query)
	#return query

	results = cursor.fetchall()
	resourcesReceivedByMe = []

	for r in results:
		print r
		obj = ResourceStatus_ResourceRequestsReceivedByMe_Item(r[0], r[1], r[2], r[3], r[4], r[5])
		resourcesReceivedByMe.append(obj)

	g.resourcesReceivedByMeTable = ResourceStatus_ResourceRequestsReceivedByMe(resourcesReceivedByMe)


	#FOURTH
	cursor.execute(Queries.resoureceStatus_getRepairsScheduledAndInProgress(currentuser))
	results = cursor.fetchall()
	resourcesInUse = []

	for r in results:
		obj = ResourceStatus_RepairsScheduledAndInProgress_Item(r[0], r[1], r[2], r[3], "cancel")
		resourcesInUse.append(obj)

	g.resourcesReceivedByMe = ResourceStatus_RepairsScheduledAndInProgress(resourcesInUse)

    
	return render_template('resourceStatus.html')

@app.route("/reportGenerator")    
def reportGenerator():
	currentuser = session['username'];
	cursor.execute(Queries.generateReport(currentuser))
	data = cursor.fetchall()

	newList = []
	for r in data:
		obj = GenerateReport_Item(r[0], r[1], r[2], r[3])
		newList.append(obj)

	g.table = GenerateReport_Table(newList)
	
	return render_template('reportGenerator.html')

@app.route("/menu")
def mainMenu():
    currentuser = session['username'];

    cursor.execute(Queries.getPopulation(currentuser))
    g.population = cursor.fetchone()
    if g.population > 0:
		g.population = g.population[0]
    
    cursor.execute(Queries.getJurisdiction(currentuser))
    g.jurisdiction = cursor.fetchone() 
    if g.jurisdiction > 0:
		g.jurisdiction = g.jurisdiction[0]   

    cursor.execute(Queries.getHQLocation(currentuser))
    g.hqlocation = cursor.fetchone()
    if g.hqlocation > 0:
		g.hqlocation = g.hqlocation[0]

    return render_template('menu.html')

#THIS FLASHES ERRORS ON FORM SUBMISSION -- NEED TO TEST
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:

            print("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))  


            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))    
    

if __name__ == "__main__":
    app.run()