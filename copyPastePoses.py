import json
import maya.cmds as mc
import os

# ------------------------------------- Part 1 ------------------------------------------
# This tool stores all poses from a scene and inputs them into json format.
# It will first store the root joint and recursively stores its children as follows:
# hierarchy = { parentNode : [ [scale , rotate ,translate , jointOrient] , [ allchildNodeslist ] ] }
# writes to json file with all of the joint heirarchies from the scene in a list.
# [ hierarchy1, hierarchy2, .... , hierarchyN ]
# To store all joint hierarchies:
#    1. parse through scene for root joints and store in list
#    2. go through list to store all child nodes for each root joint
# NOTE: All joints must have different names in the scene.

# ------------------------------------- Part 2 ------------------------------------------
# reads from json file to input poses to new joint heirarchy from scene
# looks for any missing bones in the new joint heirarchy to match the original pose:
#    1. Parse through new joint heirarchy and store in dictionary/list
#    2. TODO: Compare structures by name, if the joint names are missing, add new bones
#    3. Parse through joint hierarchies to update based on source data
# NOTE: All joints must have the same names as original scene (as of now)

# directory management
_data_dir_ = 'data.json'
_current_dir_ = '/Users/stfnylim/Documents/maya/projects/Tutorial/scripts'
_write_dir_ = os.path.join(_current_dir_,_data_dir_)
_read_dir_ = os.path.join(_current_dir_,_data_dir_)

# class for Part 1
class SkeletonStorage():
    def getAllRootJoints():
        jnts = mc.ls(type="joint", l=True)  # Collect all joints in scene by their long names.
        output = []
        for jnt in jnts:
            prnt = mc.listRelatives(jnt,parent=True)
            if not prnt or mc.objectType(prnt[0]) != 'joint':
                output.append(jnt)
        return output
    
    # for getting the scale, rotate, translate, joint orient attributes of object
    def getAttributes(object):
        attributes = ['scale','rotate','translate','jointOrient']
        attList = []
        for attribute in attributes:
            try:
                attList.append(mc.getAttr(object + '.' + attribute))
            except:
                pass
        return attList
    
    # to store information of single joint heirarchy as a tree.
    # preserves index order of joints
    def inputJointHierarchy(parent, tree):
        children = mc.listRelatives(parent, c=True, type='joint')
        dict1 = {parent: [getAttributes(parent),[]]}
        tree.append(dict1)
        if children:
            for child in children:
                inputJointHierarchy(child, tree[-1][parent][1]) 
        else:
            return

    def getSceneSkeletons():
        allJointHier = []
        allRootJoints = getAllRootJoints()
        # iterates through all root joints to store attributes and child joint data
        for rootJoint in allRootJoints:
            hier_tree = []
            inputJointHierarchy(rootJoint, hier_tree)
            allJointHier.append(hier_tree)
        return allJointHier
# class for part 2       
class SkeletonsLoad():
    # TODO: compare new skeletons in scene with old
    def compareSkeletons():
        # Use getAllRootJoints, and inputJointHierarchy to retrieve new scene data
        # or parseChildJoints after getAllRootJoints
        # Then compare names and structure.
        # if name does not exist in children nodes, call addJoints.
        Pass
    
    
    # TODO: unparent if needed, add new joints to structure, then parent.
    def addJoints(parent_joint, new_child_joint):
        # retrieve parent joint, if it has children, unparent those children
        
        # create new child joint with transform info from param.
        # parent it to parent_joint
        # reparent children to new_child_joint
        Pass
    
    # parses through skeletons to update transforms
    def parseChildJoints(joint_list, f):
        for skeleton in joint_list:
            if type(skeleton) == list:
                skeleton = skeleton[0]               
            prnt = next(iter(skeleton))
            
            f(skeleton)
                 
            children = skeleton[prnt][-1]
            
            if len(children) == 0:
                return
            #print(children)
            parseChildJoints(children,f)
            
    
    def changeTransform(dst_transform):
        name = next(iter(dst_transform))
        transform = getSourceTransform(name)  # source transform from json file
        # updating scale, rotate, translate, joint orient attributes 
        mc.setAttr(name+".scale", transform[0][0][0], transform[0][0][1], transform[0][0][2])
        mc.setAttr(name+".rotate", transform[1][0][0],transform[1][0][1],transform[1][0][2])
        mc.setAttr(name+".translate", transform[2][0][0], transform[2][0][1], transform[2][0][2])
        mc.setAttr(name+".jointOrient", transform[3][0][0],transform[3][0][1],transform[3][0][2])
    
    
    def getSourceTransform(name):
        f = open(_read_dir_)
        data = json.load(f)
        return getTransformByName(data, name)
        
        
    def getTransformByName(transform, name): # would find more efficient way to search
        for skeleton in transform:
            # some data is stored in a list so retrieve data
            if type(skeleton) == list:
                skeleton = skeleton[0]  
           
            prnt = next(iter(skeleton))
            if prnt == name:
                return skeleton[name][0]
            
            children = skeleton[prnt][-1]
            if len(children) == 0:
                continue
            else: # If children node returns none, then continue loop
                child = getTransformByName(children, name)            
                if not child:
                    continue
                else:
                     return child


# main

# ------------------- Store original poses in json file ------------------------ #
# clear all data and input all joint hierarchies from current scene.
if not os.path.exists(_current_dir_):
    print('The directory does not exist')
else:
    if os.path.exists(_write_dir_):
        os.remove(_write_dir_)
    with open(_write_dir_, 'w') as f:
        json.dump(SkeletonStorage.getSceneSkeletons(), f)
    print('Successfully stored skeletons in json file')


# ------------------- Update new scene with json file -------------------------- #
allJointHier = SkeletonStorage.getSceneSkeletons()
if not os.path.exists(_read_dir_):
    print('The read file does not exist')
else:
    # TODO: Must compare skeletons in current scene to add any missing bones
    # SkeletonsLoad.compareSkeletons()
    SkeletonsLoad.parseChildJoints(allJointHier, SkeletonsLoad.changeTransform)
    print('finished copying poses to current scene')
