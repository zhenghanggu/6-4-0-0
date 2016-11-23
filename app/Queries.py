import datetime
from datetime import timedelta
from datetime import date
import time

class Queries(object):
	
	@classmethod
	def addIncident(cls, username, description, long, lat):
		queryString = "INSERT INTO INCIDENTS (USERNAME,DESCRIPTION,LATITUDE,LONGITUDE) values('%s','%s','%s','%s');" % (username, description, long, lat)
		return queryString

	@classmethod
	def getESFs(cls):
		queryString = "SELECT ESF_ID, DESCRIPTION from ESF"
		return queryString	
	@classmethod
	def getNextResourceID(cls):
		queryString = "SHOW TABLE STATUS LIKE 'RESOURCE'"
		return queryString

	@classmethod
	def getReports(cls, username):
		queryString = "SELECT a.ESF_ID,a.DESCRIPTION, COUNT(b.ID) as 'Total Resources', COUNT(c.ID) as 'Resources in use' FROM ESF a LEFT OUTER JOIN RESOURCE b ON a.ESF_ID=b.P_ESF AND b.USERNAME=%s LEFT OTUER JOIN RESOURCE c ON a.ESF_ID=c.P_ESF AND c.status='INUSE' AND c.USERNAME=%s GROUP BY a.ESF_ID,a.DESCRIPTION;" % (username, username)
		return queryString

	
	@classmethod
	def getResourcesInUse(cls):
		queryString = "SELECT a.RES_ID as 'ID', b.NAME as 'Resource Name', c.DESCRIPTION as 'Incident', d.NAME as 'Owner', a.APP_DATE as 'Start Date', a.RET_DATE as 'Return By' FROM REQUESTS a JOIN RESOURCE b ON a.RES_ID=b.ID JOIN INCIDENTS c on a.INC_ID=c.INC_ID JOIN USERS d on b.USERNAME=d.USERNAME WHERE c.USERNAME=@currentuser and a.status='Approved';"
		return queryString

	@classmethod
	def getPopulation(cls, username):
		queryString = "SELECT POPULATION FROM MUNICIPALITY_USERS WHERE USERNAME='%s'" % (username)
		return queryString	

	@classmethod
	def getJurisdiction(cls, username):
		queryString = "SELECT JURISDICTION FROM GOVAGENCY_USERS WHERE USERNAME='%s';" % (username) 
		return queryString

	@classmethod
	def getHQLocation(cls, username):
		queryString = "SELECT LOC_OF_HQ FROM COMPANY_USERS WHERE USERNAME='%s';" % (username)
		return queryString	

	@classmethod
	def getUserIncidents(cls, username):
		queryString = "SELECT INC_ID, DESCRIPTION FROM INCIDENTS WHERE username='%s';" % (username)
		return queryString

	@classmethod
	def getIncidentNameFromID(cls, id):
		queryString = "SELECT DESCRIPTION FROM INCIDENTS WHERE INC_ID='%s';" % (id)
		return queryString

	@classmethod
	def getLatLongOfIncident(cls, incidentID):
		queryString = "SELECT LATITUDE, LONGITUDE FROM INCIDENTS WHERE INC_ID='%s'" % (incidentID)
		return queryString	

	@classmethod
	def searchResourcesNothingSelected(cls):
		queryString = "SELECT a.ID,a.NAME,b.NAME,a.AMOUNT,a.COST_PER,a.STATUS,a.DATE_AV FROM RESOURCE a INNER JOIN USERS b ON a.USERNAME=b.USERNAME"
		return queryString

	@classmethod
	def searchResourcesbyKeyword(cls, keyword):
		queryString = "SELECT a.ID,a.NAME,b.NAME,a.AMOUNT,a.COST_PER,a.STATUS,a.DATE_AV FROM RESOURCE a INNER JOIN USERS b ON a.USERNAME=b.USERNAME LEFT OUTER JOIN RESOURCE_CAPABILTY c ON a.ID=c.RES_ID WHERE a.name LIKE '%%%s%%' OR a.M_NAME LIKE '%s' OR c.CAPABILITY like '%s'" % (keyword, keyword, keyword)
		return queryString	

	@classmethod
	def searchResourcesbyESF(cls, esfid):
		queryString = "SELECT a.ID,a.NAME,b.NAME,a.AMOUNT,a.COST_PER,a.STATUS,a.DATE_AV FROM RESOURCE a INNER JOIN USERS b on a.USERNAME=b.USERNAME LEFT OUTER JOIN ADDITIONAL_ESF c on a.ID=c.RES_ID WHERE a.P_ESF = '%s' OR c.ESF_ID='%s';" % (esfid, esfid)
		return queryString


	@classmethod
	def searchResourcesbyIncidentAndDistance(cls, lat, long):
		queryString = "SELECT ID, NAME,AMOUNT,COST_PER,STATUS,DATE_AV, 6371*2 * atan2(sqrt(sin( radians( LatIncident-latitude)/2)* sin(radians( LatIncident-latitude)/2)+cos(radians(LatIncident))*cos(radians(latitude))*sin(radians(LongIncident-longitude)/2)*sin(radians(LongIncident-longitude)/2)), sqrt(1-sin( radians( LatIncident-latitude)/2)* sin(radians( LatIncident-latitude)/2)+cos(radians(LatIncident))*cos(radians(latitude))*sin(radians(LongIncident-longitude)/2)*sin(radians(LongIncident-longitude)/2))) AS Distance, USERNAME AS OWNER FROM RESOURCE JOIN (SELECT %s AS LatIncident,  %s AS LongIncident) AS p ON 1=1 ORDER BY Distance" % (lat, long)
		return queryString	
	
	@classmethod
	def generateReport(cls, username):
		queryString = "SELECT a.ESF_ID,a.DESCRIPTION, COUNT(b.ID) as 'Total Resources', COUNT(c.ID) as 'Resources in use' FROM ESF a LEFT OUTER JOIN RESOURCE b ON a.ESF_ID=b.P_ESF AND b.USERNAME='%s' LEFT OUTER JOIN RESOURCE c ON a.ESF_ID=c.P_ESF AND c.status='INUSE' AND c.USERNAME='%s' GROUP BY a.ESF_ID,a.DESCRIPTION;" % (username, username)
		return queryString	

	@classmethod
	def resourceStatus_getResourcesInUse(cls, username):
		queryString = "SELECT a.RES_ID AS 'ID',b.NAME AS 'Resource Name',c.DESCRIPTION AS 'Incident',d.NAME AS 'Owner', a.REQ_DATE AS 'Start Date', a.RET_DATE AS 'Return By' ,c.INC_ID, a.RES_ID FROM REQUESTS a JOIN RESOURCE b on a.RES_ID=b.ID JOIN INCIDENTS c ON a.INC_ID=c.INC_ID JOIN USERS d ON b.USERNAME=d.USERNAME WHERE c.USERNAME='%s' AND a.status='Approved';" % (username)			
		return queryString

	@classmethod
	def resourceStatus_getResourcesRequestedByMe(cls, username):
		queryString = "SELECT a.RES_ID AS 'ID', b.NAME AS 'Resource Name', c.DESCRIPTION AS 'Incident', d.NAME AS 'Owner', a.RET_DATE AS 'Return By' , c.INC_ID AS 'Incident ID', a.RES_ID AS 'Resource ID'  " \
			"FROM REQUESTS a " \
			"JOIN RESOURCE b " \
			"ON a.RES_ID=b.ID " \
			"JOIN INCIDENTS c " \
			"ON a.INC_ID=c.INC_ID " \
			"JOIN USERS d " \
			"ON b.USERNAME=d.USERNAME " \
			"WHERE c.USERNAME='%s' AND a.status='Pending';" % (username)
		return queryString

	@classmethod
	def resourceStatus_getResourcesReceivedByMe(cls, username):
		queryString = "SELECT a.RES_ID as 'ID',b.NAME as 'Resource Name',c.DESCRIPTION as 'Incident',d.NAME as 'Requested By', a.RET_DATE as 'Return By', a.INC_ID from REQUESTS a " \
			"JOIN RESOURCE b " \
			"ON a.RES_ID=b.ID " \
			"JOIN INCIDENTS c " \
			"ON a.INC_ID=c.INC_ID "\
			"JOIN USERS d " \
			"ON c.USERNAME=d.USERNAME " \
			"where b.USERNAME='%s' and a.status='Pending';" % (username)
		return queryString	

	@classmethod
	def resoureceStatus_getRepairsScheduledAndInProgress(cls, username):
		queryString = "SELECT ID as 'ID', NULL as 'START_DATE', DATE_AV as 'Ready by', STATUS from RESOURCE where STATUS='In-Repair' and USERNAME='%s' " \
			"UNION " \
			"SELECT RES_ID as 'ID', START_DATE, READY_DATE as'Ready by', 'REPAIR_SCHEDULED' as 'STATUS' from REP_REQUESTS;"		
		return queryString	

	@classmethod
	def requestResource(cls, resourceID, incidentID):
		today = date.today()
		returnDate = today + timedelta(days=10)
		queryString = "INSERT INTO REQUESTS VALUES (%s, %s, '%s', '%s', 'Pending', NULL)" % (resourceID, incidentID, today, returnDate)		
		return queryString

	@classmethod
	def deletePendingResourceRequests(cls, resourceID, incidentID):
		queryString = "DELETE FROM REQUESTS WHERE RES_ID='%s' and INC_ID='%s';" % (resourceID, incidentID)	
		return queryString

	@classmethod
	def deployResource(cls, resourceID, incidentID):
		queryString = "UPDATE REQUESTS SET STATUS='Approved' WHERE RES_ID=%s and INC_ID=%s;" % (resourceID, incidentID)
		return queryString
	
	@classmethod
	def deployingResourceStatus(cls, _date, resourceID):
		_today = date.today()
		print "TODAY IS", _today
		returnDate = _today + timedelta(days=10)
		queryString = "UPDATE RESOURCE SET STATUS='INUSE', DATE_AV='%s' WHERE ID=%s;" % (returnDate, resourceID)
		return queryString

	@classmethod
	def checkForRepairRequests(cls, resourceID):
		queryString = "SELECT START_DATE, READY_DATE FROM REP_REQUESTS WHERE RES_ID='%s';" % (resourceID)
		return queryString

	@classmethod
	def setStatusToInRepair(cls, resourceID, readyDate):
		queryString = "UPDATE RESOURCE SET STATUS='INREPAIR', DATE_AV='%s' WHERE ID='%s';"	% (readyDate, resourceID)
		return queryString

	@classmethod
	def deteFromRepairRequests(cls, resourceID):
		queryString = "DELETE FROM REP_REQUESTS WHERE RES_ID=%s" % resourceID
		return queryString	

	@classmethod
	def setStatusToAvailable(cls, resourceID):
		today = date.today()
		queryString = "UPDATE RESOURCE SET STATUS='Available', DATE_AV='%s' WHERE ID='%s';" % (today, resourceID)
		return queryString

	@classmethod
	def deleteResourceFromRequestsTable(cls, resourceID, incidentID):
		queryString = "DELETE FROM REQUESTS WHERE RES_ID=%s AND INC_ID=%s" % (resourceID, incidentID)
		return queryString

	@classmethod
	def submitRepairRequest(cls, resourceID):
		today = date.today()
		returnDate = today + timedelta(days=10)
		queryString = "INSERT INTO REP_REQUESTS VALUES ('%s', '%s', '%s');" % (resourceID, today, returnDate)
		return queryString

	@classmethod
	def deleteRepairRequest(cls, resourceID):
		queryString = "DELETE FROM REP_REQUESTS WHERE RES_ID='%s';"	% (resourceID)
		return queryString


	

		
	