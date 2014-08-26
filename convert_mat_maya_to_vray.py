import pymel.core as pm
import pprint

def createVrayMat(mat_dict):
 
    for mat_name, info_dict in mat_dict.iteritems():
        
        # get the maps
        color_file = info_dict.get('color_file')
        spec_color_file = info_dict.get('spec_color_file')
        bump_file = info_dict.get('bump_file')
        bump_depth = info_dict.get('bump_depth')
        diffuse_amount_file = info_dict.get('diffuse_amount_file')
        reflect_gloss_file = info_dict.get('reflect_gloss_file')
        spec_rolloff_file = info_dict.get('spec_rolloff_file')
        mesh = info_dict.get('mesh')

        # create the vray mat
        vrayMat = pm.shadingNode('VRayMtl',asShader=True, name='vray_{0}'.format(mat_name))
        
        vrayMat.useFresnel.set(True)
        vrayMat.reflectionSubdivs.set(64)
        
        if color_file:
            pm.connectAttr('{0}.outColor'.format(color_file), '{0}.color'.format(vrayMat))
        else:
            color = info_dict.get('color')
            print('found no color_file', color)
            vrayMat.color.set(color)
    
       
        if spec_color_file:
            pm.connectAttr('{0}.outColor'.format(spec_color_file), '{0}.reflectionColor'.format(vrayMat))
        else:
            spec_color = info_dict.get('spec_color')
            print('found no spec_file', spec_color)
            vrayMat.reflectionColor.set(spec_color)
                 
            
        if bump_file:
            pm.connectAttr('{0}.outColor'.format(bump_file), '{0}.bumpMap'.format(vrayMat))
            vrayMat.bumpMult.set(bump_depth)
            
        else:
            print('found no bump_file')
                
        
        if diffuse_amount_file:
            pm.connectAttr('{0}.outAlpha'.format(diffuse_amount_file), '{0}.diffuseColorAmount'.format(vrayMat))
        else:
            diffuse_amount = info_dict.get('diffuse_amount')
            print('found no diffuse_amount_file', diffuse_amount)
            vrayMat.diffuseColorAmount.set(diffuse_amount)
       
        
        if reflect_gloss_file:
            pm.connectAttr('{0}.outAlpha'.format(reflect_gloss_file), '{0}.reflectionGlossiness'.format(vrayMat))
        else:
            reflect_gloss = info_dict.get('reflect_gloss')
            print('found no reflect_gloss_file', reflect_gloss)
            vrayMat.reflectionGlossiness.set(reflect_gloss)
            
            
            
        if spec_rolloff_file:
            pm.connectAttr('{0}.outAlpha'.format(spec_rolloff_file), '{0}.reflectionColorAmount'.format(vrayMat))
        else:
            spec_rolloff = info_dict.get('spec_rolloff')
            print('found no spec_rolloff_color_file', spec_rolloff)
            vrayMat.reflectionColorAmount.set(spec_rolloff)
            #vrayMat.reflectionColorAmount.set(.5)
            
    
        # create the shading grp
        vraySG = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name='vray_{0}SG'.format(mat_name))
        # connect the mat and SG
        pm.connectAttr('{0}.outColor'.format(vrayMat), '{0}.surfaceShader'.format(vraySG), force=True)
        
        if mesh:
            pm.sets(vraySG, forceElement=mesh)

    
def convert_maya_to_vray_material(mat_list):
    
    ret_dict = {}
    
    for mat in mat_list:
        
        mat_dict = {}
        ret_dict[mat] = mat_dict
        
        #if (mat == 'lambert1' or mat == 'particleCloud1'): continue
        
        # only do blinn materials
        if type(mat) is not pm.nodetypes.Blinn:
            continue           
                
        sg = mat.listConnections(type='shadingEngine')[0]
        mesh = sg.listConnections(type='mesh')
        
        
        mat_dict['mesh'] = mesh
        
        
        # get the file textures
        spec_color_file = mat.specularColor.inputs()
        
        color_file = mat.color.inputs()
        
        bump_file = []
        bump_node = mat.normalCamera.inputs()
        
        if(bump_node):
            bump_file = bump_node[0].listConnections(type="file")
            bump_depth = bump_node[0].getAttr('bumpDepth')
         
           
        diffuse_amount_file = mat.diffuse.inputs()
        
        reflect_gloss_file = mat.eccentricity.inputs()
        
        spec_rolloff_file = mat.specularRollOff.inputs()
           
        
        # if we did not get a file, check for a value
        if len(spec_color_file) > 0:
            mat_dict['spec_color_file'] = spec_color_file[0]
            
        else:
             spec_color = mat.getSpecularColor()
             mat_dict['spec_color'] = spec_color
            
        
        if len(color_file) > 0:
            mat_dict['color_file'] = color_file[0]
        
        else:
            color = mat.getColor()
            mat_dict['color'] = color
        
        
        if len(bump_file) > 0:
            mat_dict['bump_file'] = bump_file[0]
            mat_dict['bump_depth'] = bump_depth
            
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

        if len(spec_rolloff_file) > 0:
            mat_dict['spec_rolloff_file'] = spec_rolloff_file[0]
            
        else:
            spec_rolloff = mat.getSpecularRollOff()
            mat_dict['spec_rolloff'] = spec_rolloff

    return ret_dict
    
#pm.openFile('/Users/johan/Developement/maya/convert_mat_maya_to_vray/convert_scene.mb', force=True)
#pm.openFile('/Users/johan/Developement/maya/convert_mat_maya_to_vray/convert_scene_multi_maps.mb', force=True)
#pm.openFile('/Users/johan/Developement/maya/convert_mat_maya_to_vray/convert_scene_no_maps.mb', force=True)

all_mat = [mat for mat in pm.ls(materials=True) if type(mat) is pm.nodetypes.Blinn]
md = convert_maya_to_vray_material(all_mat)
pprint.pprint(md)

createVrayMat(md)

# select the old materials
pm.select(md.keys())
