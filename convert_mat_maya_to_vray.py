import pymel.core as pm

def create_vray_material(mat):

    '''
    reflectionColor = (1, 1, 1)
    reflectionAmount = 0.8
    reflectionGloss = 0.8
    color = mat.color.get()

    # create the vray mat
    vrayMat = pm.shadingNode('VRayMtl',asShader=True, name='vray_'+mat)
    vrayMat.useFresnel.set(True)
    vrayMat.reflectionGlossiness.set(reflectionGloss)
    vrayMat.reflectionColorAmount.set(reflectionAmount)
    vrayMat.reflectionColor.set(reflectionColor)
    vrayMat.color.set(color)
    
    # create the shading grp
    vraySG = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name='vray_'+mat+'_SG')
    # connect the mat and SG
    pm.connectAttr(vrayMat+'.outColor', vraySG+'.surfaceShader', force=True)
    
    return vraySG
    '''

def convert_maya_to_vray_material(mat_list):
    
    old_mat = []
    
    for mat in mat_list:
        
        if (mat == 'lambert1' or mat == 'particleCloud1'): continue
        
        old_mat.append(mat)
        sg = mat.listConnections(type='shadingEngine')[0]
        mesh = sg.listConnections(type='mesh')
    
        # create the vray material and assign it
        #vraySG = create_vray_material(mat)
        #pm.sets(vraySG, forceElement=mesh)
     
    # select the old material
    pm.select(old_mat)
    


pm.openFile('/Users/johan/Developement/maya/convert_mat_maya_to_vray/convert_scene.mb', force=True)

all_mat = pm.ls(materials=True)
convert_maya_to_vray_material(all_mat)