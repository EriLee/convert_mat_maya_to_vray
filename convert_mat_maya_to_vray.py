import pymel.core as pm
import pprint

import pymel.core as pm

def createVrayMat(mat_dict):
 
    for mat_name, info_dict in mat_dict.iteritems():
        
        # get the maps
        color_file = info_dict.get('color_file')
        spec_file = info_dict.get('spec_file')
        bump_file = info_dict.get('bump_file')
        diffuse_amount_file = info_dict.get('diffuse_amount_file')
        reflect_gloss_file = info_dict.get('reflect_gloss_file')
        spec_rolloff_color_file = info_dict.get('spec_rolloff_color_file')
        mesh = info_dict.get('mesh')

    # create the vray mat
    vrayMat = pm.shadingNode('VRayMtl',asShader=True, name='vray_{0}'.format(mat_name))
    
    vrayMat.useFresnel.set(True)

    
    if color_file:
        pm.connectAttr('{0}.outColor'.format(color_file), '{0}.color'.format(vrayMat))
    else:
        color = info_dict.get('color')
        print('found no color_file', color)
        vrayMat.color.set(color)

   
    if spec_file:
        pm.connectAttr('{0}.outColor'.format(spec_file), '{0}.reflectionColor'.format(vrayMat))
    else:
        spec = info_dict.get('spec')
        print('found no spec_file', spec)
        vrayMat.reflectionColor.set(spec)
             
        
    if bump_file:
        pm.connectAttr('{0}.outColor'.format(bump_file), '{0}.bumpMap'.format(vrayMat))
    else:
        print('found no bump_file')
            
    
    if diffuse_amount_file:
        pm.connectAttr('{0}.outColor'.format(diffuse_amount_file), '{0}.diffuseColorAmount'.format(vrayMat))
    else:
        diffuse_amount = info_dict.get('diffuse_amount')
        print('found no diffuse_amount_file', diffuse_amount)
        vrayMat.diffuseColorAmount.set(diffuse_amount)
   
    
    if reflect_gloss_file:
        pm.connectAttr('{0}.outColor'.format(reflect_gloss_file), '{0}.reflectionGlossiness'.format(vrayMat))
    else:
        reflect_gloss = info_dict.get('reflect_gloss')
        print('found no reflect_gloss_file', reflect_gloss)
        vrayMat.reflectionGlossiness.set(reflect_gloss)
        
        
        
    if spec_rolloff_color_file:
        pm.connectAttr('{0}.outColor'.format(spec_rolloff_color_file), '{0}.reflectionColorAmount'.format(vrayMat))
    else:
        spec_rolloff_color = info_dict.get('spec_rolloff_color')
        print('found no spec_rolloff_color_file', spec_rolloff_color)
        vrayMat.reflectionColorAmount.set(spec_rolloff_color)
        #vrayMat.reflectionColorAmount.set(.5)
        

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
    
    ret_dict = {}
    
    for mat in mat_list:
        
        mat_dict = {}
        ret_dict[mat] = mat_dict
        
        if (mat == 'lambert1' or mat == 'particleCloud1'): continue
        
        sg = mat.listConnections(type='shadingEngine')[0]
        mesh = sg.listConnections(type='mesh')
        
        
        mat_dict['mesh'] = mesh
        
        
        # get the file textures
        spec_file = mat.specularRollOff.inputs()
        
        color_file = mat.color.inputs()
   
        bump_node = mat.normalCamera.inputs()
        if(bump_node):
            bump_file = bump_node[0].listConnections(type="file")
         
           
        diffuse_amount_file = mat.diffuse.inputs()
        
        reflect_gloss_file = mat.eccentricity.inputs()
        
        spec_rolloff_color_file = mat.eccentricity.inputs()
           
        
        # if we did not get a file, check for a value
        if len(spec_file) > 0:
            mat_dict['spec_file'] = spec_file[0]
            
        else:
             spec = mat.getSpecularRollOff()
             mat_dict['spec'] = spec
            
        
        if len(color_file) > 0:
            mat_dict['color_file'] = color_file[0]
        
        else:
            color = mat.getColor()
            mat_dict['color'] = color
        
        
        if len(bump_file) > 0:
            mat_dict['bump_file'] = bump_file[0]
        else:
            pass
        
        if len(diffuse_amount_file) > 0:
            mat_dict['diffuse_amount_file'] = diffuse_amount_file[0]
            
        else:
            diffuse_amount = mat.getDiffuseCoeff()
            mat_dict['diffuse_amount'] = diffuse_amount

        if len(reflect_gloss_file) > 0:
            mat_dict['reflect_gloss_file'] = reflect_gloss_file[0]
            
        else:
            eccentricity = mat.getEccentricity()
            reflect_gloss = 1 - eccentricity
            mat_dict['reflect_gloss'] = reflect_gloss

        if len(spec_rolloff_color_file) > 0:
            mat_dict['spec_rolloff_color_file'] = spec_rolloff_color_file[0]
            
        else:
            spec_rollof = mat.getSpecularColor()
            #spec_rolloff_color = (spec_rollof[0], spec_rollof[1], spec_rollof[2])
            #mat_dict['spec_rolloff_color'] = spec_rolloff_color
            mat_dict['spec_rolloff_color'] = spec_rollof[0]

    return ret_dict
    


pm.openFile('/Users/johan/Developement/maya/convert_mat_maya_to_vray/convert_scene.mb', force=True)

all_mat = pm.ls(materials=True)
md = convert_maya_to_vray_material(all_mat)
pprint.pprint(md)

createVrayMat(md)