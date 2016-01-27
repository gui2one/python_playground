import bpy
from bpy.app.handlers import persistent


for i, func in enumerate(bpy.app.handlers.frame_change_pre):
    if func.__name__ == 'my_func':
        bpy.app.handlers.frame_change_pre.pop(i)
        
         
@persistent
def my_func(scene):


    C = bpy.context
    D = bpy.data

    dominos = C.scene.objects['dominos']

    objs = [C.scene.objects['dominos'],C.scene.objects['bonne_annee'],C.scene.objects['dominos_logo'],C.scene.objects['typos_2016']]
    
    for dominos in objs:
        
        try:
            dominos.modifiers.remove(dominos.modifiers['Bevel'])
        except:
            pass
        
        # --- get a mesh from the object ---
        apply_modifiers = True
        settings = 'PREVIEW'
        mesh = dominos.to_mesh(C.scene, apply_modifiers, settings)
    #    print(mesh)
        # ... do something with the mesh ...
        numPolys = len(mesh.polygons)
        for i in range(int(numPolys/6.0)):
            hasFallen = mesh.polygons[i*6 + 5].normal[1] < 0.999
            #print (hasFallen)
            ### 6 polygons
            ### 24 vertices
            
            for j in range(6): # 6 faces
                indexRange = dominos.data.polygons[i*6 + j].loop_indices ## loop_indices returns a type "range"
                for k in indexRange:

                    if hasFallen :
                    
                        dominos.data.vertex_colors[1].data[k].color = [0.0,0.0,0.0]
                    else:
                        dominos.data.vertex_colors[1].data[k].color = [1.0,1.0,1.0]                

        # optionally remove it
        bpy.data.meshes.remove(mesh)
        
        bevelMod = dominos.modifiers.new("Bevel","BEVEL")
        bevelMod.width = 0.003
        bevelMod.segments = 2
        
 
bpy.app.handlers.frame_change_pre.append(my_func)