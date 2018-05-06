#loader.SetAttrs({"TOOLB_PassThrough" : False})
import os
import glob

for item in comp.GetToolList()[2].GetAttrs():
	print item

loaders = []
print "---------------------"


for i in comp.GetToolList():

	tool = comp.GetToolList()[i]
	# print i, comp.GetToolList()[i+1]
	attrs = tool.GetAttrs()
	if attrs["TOOLS_RegID"] == "Loader":
		print "LOADER !!!!!!! "
		loaders.append(comp.GetToolList()[i])

comp.Lock()
comp.StartUndo("gui2one Script")
for loader in loaders:
	
	# loader.SetAttrs({'TOOLB_NameSet' :True, 'TOOLS_Name' : "bbb"})
	#print loader.GetAttrs()["TOOLIT_Clip_TrimIn"]
	clipName =  loader.GetAttrs()["TOOLST_Clip_Name"][1]
	print clipName.replace('\\','/')
	# loader.SetAttrs({'TOOLST_Clip_Name' : clipName})
	# loader.SetAttrs({'TOOLIT_Clip_TrimIn' : 3.0})

	#loader.SetAttrs({"TOOLB_PassThrough" : False})
	#clipStart = loader.GetAttrs()["TOOLNT_Region_Start"][1] 


	loader.Clip = clipName
	# loader.SetAttrs({"Clip": clipName})

comp.EndUndo(True)
comp.Unlock()
