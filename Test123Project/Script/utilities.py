import json
import base64
import sys
import inspect

#init empty id dictionary
id_dict = {}
      

def createTestRun_cloud():
      cycleName = "Automated_TestComplete_Run " + str(aqDateTime.Now()) #timestamped test cycle name (new one is created every time the project is run)
      address =  "https://api.zephyrscale.smartbear.com/v2/testcycles" #Zephyr Scale cloud endpoint to create test run
  
      request = aqHttp.CreatePostRequest(address)
      request.SetHeader("Authorization", "Bearer " + Project.Variables.cloud_token) #replace proj. lvl var. with your bearer token from ZS
      request.SetHeader("Content-Type", "application/json")
      
      #building request body
      #YOU NEED TO EDIT THIS "requestBody"
      requestBody = {
        "name" : cycleName,
        "projectKey" : "ZSC", #jira project key for the Zephyr Scale/JIRA project
        #"folderId" : 1058696 #the folderID of the testcase folder you'd like to deposit these testcases into (optional)
        }
      response = request.Send(json.dumps(requestBody))
      df =  json.loads(response.Text)
      key = str(df["key"])
      #set the new test cycle key as a project level variable for later use
      Project.Variables.testRunKey = key
      Log.Message(key) #output new test cycle key
      
'''      
def createTestRun_server():
      projName = "Automated_TestComplete_Run " + str(aqDateTime.Now()) #timestamped test cycle name 
      address =  "https://jira-se.tm4j-server.smartbear.io/rest/atm/1.0/testrun" #zephyr scale server endpoint to create test run
      username = "ZephyrScale_Server_Username" #jira username
      password = "ZephyrScale_Server_Password" #jira password
      # Convert the user credentials to base64 for preemptive authentication
      credentials = base64.b64encode((username + ":" + password).encode("ascii")).decode("ascii")
  
      request = aqHttp.CreatePostRequest(address)
      request.SetHeader("Authorization", "Basic " + credentials)
      request.SetHeader("Content-Type", "application/json")
      
      #intialize empty item list
      items= []
      for i in range(Project.TestItems.ItemCount): #for all test items listed at the project level
        entry = {"testCaseKey":getTestCaseID(Project.TestItems.TestItem[i].Name)} #grab each tc key as value pair according to name found in id_dict
        items.append(entry) #append as a test item
      
      #building request body
      requestBody = {
        "name" : projName,
        "projectKey" : "KIM", #jira project key for the tm4j project
        "folder": "/TestComplete", #cycle folder for test run 
        "items" : items #the items list will hold the key value pairs of the test case keys to be added to this test cycle
      }
      response = request.Send(json.dumps(requestBody))
      df =  json.loads(response.Text)
      key = str(df["key"])
      #set the new test cycle key as a project level variable for later use
      Project.Variables.testRunKey = key
      Log.Message(key) #output new test cycle key      
'''
        
def getTestCaseID(tc_name):
    #list out testcaseID's in dict format - this is where you will map your internal testcases (by name) to their corresponding zephyr scale testcases
    '''the following dictionary is for server deployment
    id_dict = {
        "login": "ZSC-T1",
        "logout": "ZSC-T3",  
        "UI_Error": "ZSC-T2",
        "UI_Warning": "ZSC-T4"
        }
    '''
    
    #YOU NEED TO EDIT THE BELOW "id_dict" WITH YOUR KEY VALUE PAIRS
    
    #the below is the zephyr scale cloud
    #so, in TestComplete, my Keyword Tests are called "login","logout", "UI_Error" and "UI_warning", and these are the keys in the dictionary below
    #the correspondeing TestCases in Zephyr Scale (they don't have to have the same name, but that would be preferable for clarity's sake)
    #these Zehyr Scale test cases have issue keys, in the format of PROJECT-T<number>, and these are the value pairs to the keys in the dictionary below
    id_dict = {
            "login": "ZSC-T1",
            "logout": "ZSC-T3",  
            "UI_Error": "ZSC-T2",
            "UI_Warning": "ZSC-T4"
            }
    tc_ID = id_dict.get(tc_name, "Invalid testCase") #get testcase keys by name from dictionary above
    return tc_ID  #output tm4j testcase ID
    
    
def getTCFolders(): #in case you want to get the folder id to deposit the newly created test cycle
      address =  "https://api.zephyrscale.smartbear.com/v2/folders?folderType=TEST_CYCLE" #Zephyr Scale Cloud endpoint to create test run
      request = aqHttp.CreateGetRequest(address)
      request.SetHeader("Authorization", "Bearer " + Project.Variables.cloud_token)
      request.SetHeader("Content-Type", "application/json")
      response = request.Send()
      df11= json.loads(response.Text)
      Log.Message(response.Text)


def current_script_routine_name():
  #print current script routine name
    Log.Message(inspect.currentframe().f_code.co_name)
    Log.Message(sys._getframe().f_code.co_name)    