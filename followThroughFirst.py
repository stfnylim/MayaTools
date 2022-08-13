# followThroughFirst.py
import maya.cmds as cmds
selectionList = cmds.ls(orderedSelection=True )


class SL_Window:
    def __init__(self):
        self.window = "SL_Window"
        self.title = "Follow Through"
        self.size = (400,400)
        
        if cmds.window(self.window, exists= True):
            cmds.deleteUI(self.window, window=True)
            
        self.window = cmds.window(self.window, title= self.title, widthHeight = self.size)
        
        cmds.columnLayout(adjustableColumn=True)
        
        cmds.text(self.title)
        cmds.separator( height= 20) 
        self.type = cmds.optionMenuGrp( label='Type')
        cmds.menuItem( label='Spline' )
        cmds.menuItem( label='Batch' )
        
        self.range = cmds.intFieldGrp(numberOfFields=2, label='Keyframe Range', value1 = 0, value2 =26)
        self.delay = cmds.intFieldGrp(label='Delay', value1 = 5)
        
        self.createFollowThruBtn = cmds.button(label='Apply Follow Through', command=self.createFollowThrough)
            
        cmds.showWindow()
        
        
    def createFollowThrough(self, *args):
        
        
        if len(selectionList) >=2:
    

            parentObject = selectionList[0]
            
            selectionList.remove(parentObject)
            
            type = cmds.optionMenuGrp(self.type,query=True, value=True)
            startKey = cmds.intFieldGrp(self.range, query=True, value1=True)
            endKey = cmds.intFieldGrp(self.range, query=True, value2=True)
            timeAdded = cmds.intFieldGrp(self.delay, query=True, value1=True)
            
            temp = parentObject
            for object in selectionList:
                # select object, freeze transformation and paste keys
                
                
                cmds.select(object)
                cmds.makeIdentity(apply=True, t=1,r=1,s=1,n=0)
                
                cmds.copyKey(temp,time = (startKey,endKey))
                print(cmds.pasteKey())
                
                cmds.keyframe(edit=True, relative=True,timeChange=timeAdded, time=(startKey,endKey))
                
                
                if type == "Spline":
                    temp = object
                    startKey = startKey + timeAdded
                    endKey = endKey + timeAdded
              
        
        
        else:
            print("please select 2 or more objects")

        
# opens tool window                  
window1 = SL_Window()





