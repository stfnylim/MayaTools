# goldenRatio.py

import maya.cmds as cmds
import math


selectionList = cmds.ls(orderedSelection=True)

class GR_Window:
    def __init__(self):
        self.window = "GR_Window"
        self.title = "add Golden Ratio"
        self.size = (400,400)
        
        if cmds.window(self.window, exists= True):
            cmds.deleteUI(self.window, window=True)
            
        self.window = cmds.window(self.window, title= self.title, widthHeight = self.size)
        
        cmds.columnLayout(adjustableColumn=True)
        
        cmds.text(self.title)
        cmds.separator( height= 20) 
        
        self.numInstances = cmds.intFieldGrp(numberOfFields=1, label='Number of Instances', value1= 10)
        self.spacing = cmds.intSliderGrp(label='Spacing', minValue=0, maxValue=100)
        self.axis = cmds.checkBoxGrp(numberOfCheckBoxes=3, label='Axis of creation', labelArray3=['XZ','YZ','XY'])
        print("hello")
        self.createGoldenRatioBtn = cmds.button(label='Apply Golden Ratio', command = self.createGoldenRatio)
        
        cmds.showWindow()
        

        
    def createGoldenRatio(self, *args):
        # later create as parameter
        numInstances = cmds.intFieldGrp(self.numInstances, query=True, value1=True)
        spacing = cmds.intSliderGrp(self.spacing, query=True, value=True)
        ratio = (1 + math.sqrt(5))/2
        angleRotation = 360/ratio
        XZ = cmds.checkBoxGrp(self.axis, query=True, value1=True)
        YZ = cmds.checkBoxGrp(self.axis, query=True, value2=True)
        XY = cmds.checkBoxGrp(self.axis, query=True, value3=True)
        
        
        
        if len(selectionList) >= 1:
    
            objectName = selectionList[0]
            # create locator to rotate the instances around
            coords = cmds.getAttr('%s.translate' %(objectName))[0]
            locatorName = cmds.spaceLocator(position=coords, name='%s_loc#' %(objectName))[0]
            instanceGroupName = cmds.group( empty=True, name= objectName +'_instance_grp#')
            
            print(coords)
            angle = 0.0
            
            cmds.select(instanceGroupName)
            cmds.addAttr(longName='Angle', shortName= 'agl',
                       attributeType= 'double', min=0, max= 360,
                       defaultValue=0, keyable=True)
            
            
            # parse through instances
            for i in range(numInstances):
                radius = math.sqrt(i+1+spacing) 
                angle += angleRotation
                instanceResult = cmds.instance(objectName, name = objectName +"_instance#")
                cmds.parent(instanceResult, instanceGroupName)
                # move instance along selected axis
                # if axis= "XZ"
                if XZ:
                
                    cmds.move(radius, 0, 0, instanceResult)
                elif YZ:
                
                    cmds.move(0,0,radius, instanceResult)
                elif XY:
                
                    cmds.move(0,radius, 0, instanceResult)
                
                
                # set its scalepivot and rotate pivot to center of rotation
                x = coords[0]
                y = coords[1]
                z = coords[2]
                cmds.move(x,y,z, instanceResult[0]+".scalePivot", instanceResult[0] + ".rotatePivot", absolute=True)
                
                # rotate instance at golden ratio angle increments
                
                if XZ:
                    cmds.rotate(0,angle,0, instanceResult)
                elif YZ:
                    cmds.rotate(angle,0,0, instanceResult)
                elif XY:
                    cmds.rotate(0,0,angle, instanceResult)
                
                cmds.xform(instanceResult, centerPivots=True)
                
                # create attributes to instance grp to control angle and spacing 
                '''
                ang = ''
                if XZ:
                    ang = 'rz'
                    rx= cmds.getAttr(instanceGroupName + ".Angle")
                elif YZ:
                    ang = 'rx'
                    ry= cmds.getAttr(instanceGroupName + ".Angle")
                elif XY:
                    ang = 'ry'
                    rz= cmds.getAttr(instanceGroupName + ".Angle")
                print('1')
                cmds.expression(alwaysEvaluate=True,object=instanceResult[0],
                                string = 'rotate -r -os -fo 0 0 %s.Angle' % (instanceGroupName))
                cmds.connectAttr( '%s.%s' %(instanceGroupName,'Angle') ,'%s.%s' % (instanceResult[0], ang))
                
                                
                print('2')
                '''
             
            
            
        else:
            print("Please select enough objects in the scene")
        
GR_Window()        
        
        
        




