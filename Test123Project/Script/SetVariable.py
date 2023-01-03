def GetCurrentTestName():
  Project.Variables.tc_name = aqTestCase.CurrentTestCase.Name
  Log.Message("Test Case Name is " + Project.Variables.tc_name)