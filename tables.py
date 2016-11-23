from flask_table import Table, Col, ButtonCol, LinkCol
from flask import Markup



class ButtonColCustom(LinkCol):
    """Just the same a LinkCol, but creates an empty form which gets
    posted to the specified url.
    Eg:
    delete = ButtonCol('Delete', 'delete_fn', url_kwargs=dict(id='id'))
    When clicked, this will post to url_for('delete_fn', id=item.id).
    """

    def td_contents(self, item, attr_list):
        text = self.text(item, attr_list)
        if text == "":
            return ""

        return '<form method="post" action="{url}">'\
            '<button type="submit">{text}</button>'\
            '</form>'.format(
                url=self.url(item),
                text=Markup.escape(self.text(item, attr_list)))


class ResourcesInUse(Table):
    classes = ['table', 'table-striped']
    id = Col('Id')
    resourcName = Col('Resource Name')
    owner = Col('Owner')
    cost = Col('Cost')
    status = Col('Status')
    nextAvailable = Col('Next Available')
    #action = ButtonColCustom("Action", "root", url_kwargs=dict(id='id'), attr='action')
    #action = ButtonCol("Action", "parseAction", url_kwargs=dict(id='id', type="action"), attr='action', attr_list=["taod"])


    #action = CustomButtonCol('Action', 'root', url_kwargs=dict(id='id'), attr="action")
    #distance = Col('Distance', show=False)
    #action = Col('Action') 

class ResourcesInUse_Item(object):
    def __init__(self, id, resourcName, owner, cost, per, status, nextAvailable):#, action=""):
        self.id = id
        self.resourcName = resourcName    
        self.owner = owner
        self.cost = "$"+str(cost)+"/"+str(per)
        self.status = status
        self.nextAvailable = nextAvailable
        #self.action = action
        #self.distance = distance
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__  


class ResourcesInUseStatus(Table):
    classes = ['table', 'table-striped']
    id = Col('Id')
    resourceName = Col('Resource Name')
    incident = Col('Incident')
    owner = Col('Owner')
    startDate = Col('Start Date')
    returnBy = Col('Return By')
    action = ButtonColCustom("Action", "parseAction", url_kwargs=dict(id='id', type="action", incidentID="incidentID"), attr='action')

class ResourcesInUseStatus_Item(object):
    def __init__(self, id, resourceName, incidentName, ownerName, startDate, returnBy, incidentID, action="return"):
        self.id = id
        self.resourceName = resourceName
        self.incident = incidentName   
        self.owner = ownerName 
        self.startDate = startDate
        self.returnBy = returnBy
        self.action = action
        self.incidentID = incidentID
        #self.owner = owner

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__                   


class ResourcesInUseWithDistance(Table):
    classes = ['table', 'table-striped']
    id = Col('Id')
    resourcName = Col('Resource Name')
    owner = Col('Owner')
    cost = Col('Cost')
    status = Col('Status')
    nextAvailable = Col('Next Available')
    distance = Col('Distance')
    action = ButtonColCustom("Action", "parseAction", url_kwargs=dict(id='id', type="action", incidentID="incidentID", resourceID="id"), attr='action')
    repair = ButtonColCustom("Repair", "parseAction", url_kwargs=dict(id='id', type="repair", incidentID="incidentID", resourceID="id"), attr='repair')

class ResourcesInUseWithDistance_Item(object):
    def __init__(self, id, resourcName, cost, per, status, nextAvailable, distance, incidentID, owner, action="", repair=""):
        self.id = id
        self.resourcName = resourcName    
        #self.owner = owner
        self.cost = "$"+str(cost)+"/"+str(per)
        self.status = status
        self.nextAvailable = nextAvailable
        self.distance = "{0:.2f}".format(distance)
        self.action = action
        self.incidentID = incidentID
        self.incident = "HELLO"
        self.owner = owner
        self.repair = repair

    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__  

class GenerateReport_Item(object):
    def __init__(self, id, primary_esf, total_resources, resources_inuse):
        self.id = id
        self.primary_esf = primary_esf    
        self.total_resources = total_resources
        self.resources_inuse = resources_inuse
        
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__  

class GenerateReport_Table(Table):
    classes = ['table', 'table-striped']
    id = Col('Id')
    primary_esf = Col('Primary Esf')
    total_resources = Col('Total Resources')
    resources_inuse = Col('Resources In Use') 


# RESOURCE STATUS PAGE CLASSES    
class ResourceStatus_ResourcesInUse(Table):
    classes = ['table', 'table-striped']
    id = Col('Id')
    resourcName = Col('Resource Name')
    incident = Col('Incident')
    owner = Col('Owner')
    startDate = Col('Start Date')
    returnBy = Col('Return By')
    action = Col("Action")

class GeneResourceStatus_ResourcesInUse_Item(object):
    def __init__(self, id, resourceName, incident, owner, startDate, returnBy, action=""):
        self.id = id
        self.resourceName = resourceName    
        self.incident = incident
        self.owner = owner
        self.startDate = startDate
        self.returnBy = returnBy
        self.action = action
        
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__ 

class ResourceStatus_ResourcesRequestedByMe(Table):
    classes = ['table', 'table-striped']
    id = Col('Id')
    resourcName = Col('Resource Name')
    incident = Col('Incident')
    owner = Col('Owner')
    returnBy = Col('Return By')
    #action = Col("Action")
    action = ButtonColCustom("Action", "parseAction", url_kwargs=dict(id='id', type="type", incident="incident", resourceID="resourceID", incidentID="incidentID"), attr='action')

class GeneResourceStatus_ResourcesRequestedByMe_Item(object):
    def __init__(self, id, resourceName, incident, owner,  returnBy, resourceID, incidentID, action="cancel"):
        self.id = id
        self.resourcName = resourceName    
        self.incident = incident
        self.owner = owner
        self.returnBy = returnBy
        self.action = action
        self.type = "deleteResourceRequest"
        self.resourceID = resourceID
        self.incidentID = incidentID
        
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

class ResourceStatus_ResourceRequestsReceivedByMe(Table):
    classes = ['table', 'table-striped']
    id = Col('Id')
    resourceName = Col('Resource Name')
    incident = Col('Incident')
    requestedBy = Col('Requested By')
    returnBy = Col('Return By')
    #action = Col("Action")
    action = ButtonColCustom("Action", "parseAction", url_kwargs=dict(id='id', type="type", incident="incident", returnBy="returnBy", resourceID="resourceID", incidentID="incidentID"), attr='action')
    

class ResourceStatus_ResourceRequestsReceivedByMe_Item(object):
    def __init__(self, id, resourceName, incident, requestedBy,  returnBy, incidentID, action="deploy"):
        self.id = id
        self.resourceName = resourceName    
        self.incident = incident
        self.requestedBy = requestedBy
        self.returnBy = returnBy
        self.action = action

        self.type = "deploy"
        self.resourceID = id
        self.incidentID = incidentID
        
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__             

class ResourceStatus_RepairsScheduledAndInProgress(Table):
    classes = ['table', 'table-striped']
    id = Col('Id')
    resourceName = Col('Resource Name')
    startOn = Col('Start On')
    readyBy = Col('Ready By')
    action = ButtonColCustom("Action", "parseAction", url_kwargs=dict(id='id', resourceID="id", type="action", action="action"), attr='action')
    

class ResourceStatus_RepairsScheduledAndInProgress_Item(object):
    def __init__(self, id, resourceName, startOn, readyBy,  action=""):
        self.id = id
        self.resourceName = resourceName    
        self.startOn = startOn
        self.readyBy = readyBy
        self.action = action
        self.incident = "whhhhat"
        
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__         

           