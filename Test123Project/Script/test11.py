import json
import base64

#the following is for Zephyr Scale Cloud deployements
def EventControl1_OnStopTestCase(Sender, StopTestCaseParams):
    import utilities #to use the utility functions
    testrunKey = Project.Variables.testRunKey #grab testrun key from createstRun script
    #tc_name = aqTestCase.CurrentTestCase.Name #grab current testcase name to provide to getTestCaseID function below
    tcKey =  utilities.getTestCaseID(Project.Variables.tc_name) #return testcase Key for required resource path below
    address = "https://api.zephyrscale.smartbear.com/v2/testexecutions"

    request = aqHttp.CreatePostRequest(address)
    request.SetHeader("Authorization", "Bearer " + Project.Variables.cloud_token)
    request.SetHeader("Content-Type", "application/json")
    
    #building requirest body; limited to pass,warning, and fail from within TestComplete. mapping to their corresponding execution statuses in ZS 
    
    exec_time = StopTestCaseParams.Duration
    comment = "posting from TestComplete" #default comment to test executions
    if StopTestCaseParams.Status == 0: 
        statusId = "Pass"
    elif StopTestCaseParams.Status == 1: 
        statusId = "In Progress" 
        comment = StopTestCaseParams.FirstWarningMessage
    elif StopTestCaseParams.Status == 2: 
        statusId = "Fail"
        comment = StopTestCaseParams.FirstErrorMessage
                   
    #YOU NEED TO EDIT THE BELOW KEY VALUE PAIRS FOR THE "requestBody"
    #request body for each pertinent statuses
    requestBody = {"projectKey": "ZSC", 
                   "testCaseKey": tcKey, 
                   "testCycleKey": testrunKey, 
                   "statusName": statusId,
                   "executionTime": exec_time,
                   #"executedById": "5d80fa1f30926d0c33b2467f", #jira user id (can find via url resource path in profiles)
                   #"assignedToId": "5d80fa1f30926d0c33b2467f", #same as above
                   "comment":comment}
    response = request.Send(json.dumps(requestBody))

    #in case the post request fails, let us know via logs
    if response.StatusCode != 201:
      Log.Warning("Failed to send results to Zephyr Scale. See the Details in the previous message.")
      


#the following is for Zephyr Scale Server deployment
def EventControl2_OnStopTestCase(Sender, StopTestCaseParams):
    import utilities #to use the utility functions
    testrunKey = Project.Variables.testRunKey #grab testrun key from createstRun script
    tc_name = aqTestCase.CurrentTestCase.Name #grab current testcase name to provide to getTestCaseID function below
    tcKey = utilities.getTestCaseID(tc_name) #return testcase Key for required resource path below
    address = "https://jira-se.tm4j-server.smartbear.io/rest/atm/1.0/testrun/" + str(testrunKey) + "/testcase/" + str(tcKey) + "/testresult" #endpoint to create testrun w test cases
    username = "username" #zephyr scale username
    password = "password" #zephyr scale passowrd
    # Convert the user credentials to base64 for preemptive authentication
    credentials = base64.b64encode((username + ":" + password).encode("ascii")).decode("ascii")

    request = aqHttp.CreatePostRequest(address)
    request.SetHeader("Authorization", "Basic " + credentials)
    request.SetHeader("Content-Type", "application/json")
    
    #building requirest body; limited to pass,warning, and fail from within TestComplete. mapping to their corresponding execution statuses in tm4j 
    
    comment = "posting from TestComplete" #default comment to test executions
    if StopTestCaseParams.Status == 0: # lsOk
        statusId = "Pass" # Passed
    elif StopTestCaseParams.Status == 1: # lsWarning
        statusId = "In Progress" # Passed with a warning
        comment = StopTestCaseParams.FirstWarningMessage
    elif StopTestCaseParams.Status == 2: # lsError
        statusId = "Fail" # Failed
        comment = StopTestCaseParams.FirstErrorMessage
  
    #request body for each pertinent statuses
    requestBody = {"status": statusId,"comment":comment}
    response = request.Send(json.dumps(requestBody))

    #in case the post request fails, let us know via logs
    if response.StatusCode != 201:
      Log.Warning("Failed to send results to TM4J. See the Details in the previous message.")
      
    df1 = json.loads(response.Text)
    testResultID = df1['id']
    Log.Message("Test Result ID for this execution is: " + str(testResultID))
    
    


def EventControl1_OnStartTestCase(Sender, StartTestCaseParams):
     
  tc_name = aqTestCase.CurrentTestCase.Name
  Log.Message("The name of this test case is " + tc_name) 
  
  if Project.TestItems.Current.Name == Project.TestItems.TestItem[0].Name:    
    cycleName = "Automated_TestComplete_Run " + str(aqDateTime.Now()) #timestamped test cycle name 
    address =  "https://api.zephyrscale.smartbear.com/v2/testcycles" #Zephyr Scale cloud endpoint to create test run
  
    request = aqHttp.CreatePostRequest(address)
    request.SetHeader("Authorization", "Bearer " + Project.Variables.cloud_token) #replace proj. lvl var. with your bearer token from ZS
    request.SetHeader("Content-Type", "application/json")
    
    #YOU NEED TO EDIT THE BELOW KEY VALUE PAIRS FOR THE "requestBody"  
    #building request body
    requestBody = {
      "name" : cycleName,
      "projectKey" : "ZSC", #jira project key for the Zephyr Scale/JIRA project
      #"folderId" : 1058696
      }
    response = request.Send(json.dumps(requestBody))
    df =  json.loads(response.Text)
    key = str(df["key"])
    #set the new test cycle key as a project level variable for later use
    Project.Variables.testRunKey = key
    Log.Message(key) #output new test cycle key  
    Log.Message("Creating a new test run wtih Test Run Key : " + key)  
  
  else:
    Log.Message("Not the first test item, so not creating a new test run")
    pass

