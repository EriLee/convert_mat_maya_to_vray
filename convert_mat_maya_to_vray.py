import pymel.core as pm
import pprint

import pymel.core as pm

def createVrayMat(mat_dict):
    
    for mat_name, info_dict in mat_dict.iteritems():
        
        color_file = info_dict.get('color')
        spec_file = info_dict.get('spec')
        bump_file = info_dict.get('bump')
        mesh = info_dict.get('mesh')
        
        print(mat_name, color_file, spec_file, bump_file)
    

    #reflectionColor = (0.5, 0.5, 0.5)
    #reflectionAmount = 0.7
    #reflectionGloss = 0.8
    
    # create the vray mat
    vrayMat = pm.shadingNode('VRayMtl',asShader=True, name='vray_{0}'.format(mat_name))
    
    # set properties
    #vrayMat.useFresnel.set(True)
    #vrayMat.reflectionGlossiness.set(reflectionGloss)
    #vrayMat.reflectionColorAmount.set(reflectionAmount)
    
    if color_file:
        pm.connectAttr('{0}.outColor'.format(color_file), '{0}.color'.format(vrayMat))
        
    if color_file:
        pm.connectAttr('{0}.outColor'.format(spec_file), '{0}.reflectionColor'.format(vrayMat))
        
    if color_file:
        pm.connectAttr('{0}.outColor'.format(bump_file), '{0}.bumpMap'.format(vrayMat))
        
    
    
    # create the shading grp
    vraySG = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name='vray_{0}SG'.format(mat_name))
    # connect the mat and SG
    pm.connectAttr('{0}.outColor'.format(vrayMat), '{0}.surfaceShader'.format(vraySG), force=True)
    
    if mesh:
        pm.sets(vraySG, forceElement=mesh)
    
    
    
# select materials
selMat = pm.ls(materials=True, sl=True)

for mat in selMat:
    
    maps = {}
    sg = mat.listConnections(type='shadingEngine')[0]
    mesh = sg.listConnections(type='mesh')
    
    specFile = mat.specularRollOff.inputs()
    #print("spec roll off", specFile)
    
    if(specFile):
        maps.update({'specular': specFile})

   
    colorFile = mat.color.inputs()
    #print("color", colorFile)
    if(colorFile):
        maps.update({'color': colorFile})
        # the file path
        print(pm.getAttr(colorFile[0].fileTextureName))
    
    
    # hacky way to get to the file node ?
    bumpNode = mat.normalCamera.inputs()
    #print("bump", bumpFile)
    if(bumpNode):
        bumpFile = bumpNode[0].listConnections(type="file")
        if(bumpFile):
            maps.update({'bump': bumpFile})
        
    
     
    # create the vray material and assign it
    vraySG = createVrayMat(mat, maps)
    pm.sets(vraySG, forceElement=mesh)
    
    print(maps)

def convert_maya_to_vray_material(mat_list):
    
    mat_dict = {}
    
    for mat in mat_list:
        
        if (mat == 'lambert1' or mat == 'particleCloud1'): continue
        
        sg = mat.listConnections(type='shadingEngine')[0]
        mesh = sg.listConnections(type='mesh')
        
        spec_file = None
        color_file = None
        bump_file = None
        
        spec_file = mat.specularRollOff.inputs()
        color_file = mat.color.inputs()
        
        bump_node = mat.normalCamera.inputs()
    
        if(bump_node):
            bump_file = bump_node[0].listConnections(type="file")
            
        mat_dict.update({mat:{'mesh':mesh, 'color':color_file[0], 'spec':spec_file[0], 'bump':bump_file[0]}})
  
            
    #pprint.pprint(dir(mat))
    
    print(mat.getDiffuseCoeff())
    print(mat.getEccentricity())
    print(mat.getColor())
    print(mat.getSpecularRollOff())
    print(mat.getSpecularColor())
    
    
    
    #print(spec_file, color_file, bump_file)
    return mat_dict
    
    
    


pm.openFile('/Users/johan/Developement/maya/convert_mat_maya_to_vray/convert_scene.mb', force=True)

all_mat = pm.ls(materials=True)
md = convert_maya_to_vray_material(all_mat)
#pprint.pprint(md)

#createVrayMat(md)