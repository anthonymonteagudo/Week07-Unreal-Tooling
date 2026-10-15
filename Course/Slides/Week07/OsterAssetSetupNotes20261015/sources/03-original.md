in the last video we covered deleting

the default material that comes in with

the import of the fbx and creating a new

empty material instance here that is

named according to the slot name here

so I'm going to go ahead and create a

new variable here

so now we can refer to this object

we'll take a look at the documentation

so we want to go ahead and set the

parent

let's read and write in the editor

property

and read only as a property so we're

going to want to use the editor property

and then over here we have our material

parent which is going to be this

we're loading in the asset at this path

and now we can see our material instance

now is using the parent material here as

its parent

## Set Material

so now we want to come over and assign

the material instance to this slot

on the static mesh

to do that we will take a look at the

documentation for static mesh

it has a method called set material

it's going to need the material index

and the new material

so the easy way to get the index is to

grab it here

so this is our list

you get the index

of the static material that we are

iterating over

here's our static mesh

dot set

material

so now we have our index

so that just means

what slot this case there's only one but

that could be a lot

and then the material which will be

our new material instance

and here we can see into our first slot

our new material instance is assigned

and now we take a look at adding the

textures as parameters

to this material instance

## Set Material Instance

so this part of the process has some

minor technical complexity normally with

the material instance we'd be able to

access the texture parameter values and

then easily set the textures

using the the parameter value property

here but in the case of a newly created

material instance

the texture parameter values are going

to be disabled so essentially if these

things are not checked we don't have a

texture parameter value for this texture

so we need another method to access this

information here

there is a class called the material

editing library and on that class there

is a method called set material instance

texture parameter value

takes three arguments the material

instance the parameter name and the

value which in this case is going to be

the texture so getting the instance is

going to be pretty easy and getting the

textures will be pretty easy but the

parameter name is going to be the part

that we need to think about

so when I set up this material parent

I created these texture inputs these

texture parameters here and I gave them

specific names so there's BC for base

color and for normal map and then orm

for occlusion roughness and metalness

the textures all have those same names

BC underscore n and underscore orm so I

can easily use the suffix here at the

end of the of the texture to correctly

identify what the parameter needs to be

## Assigning Textures

so let's go ahead and iterate over all

the textures and here is my populated

textures list

first thing I need to do is get the

suffix

it also call it parameter name that

might be better

so we'll get the the name of the texture

we'll do a split operation

we'll split it

the underscore and we'll grab

the last item in the list that's

returned by that process

now I'm going to go ahead and grab the

unreal

material editing Library

and then

our method

this is going to have a few arguments so

I'm going to space it out a little bit

first thing is the material instance

the next thing is going to be the

parameter name

and then

the final argument will be the texture

all right

so as we can see all of the textures are

assigned to the appropriate slot on this

material instance the material instance

has the correct parent and the material

instance is assigned here to the static

mesh now there's one significant error

## Saving Assets

in the logic that we need to resolve and

that is

currently we're iterating over the

entire list of imported assets

and taking all of the textures and

putting them in this one list and then

we're iterating over that list and just

assigning them as we go so if we have

more than one asset with more than one

set of textures we're just going to end

up with whatever the last three textures

were in that list so we need to just do

a quick check here and look for the

asset name which in this case is going

to be air conditioning and then if the

texture also has air conditioning in it

then we'll go ahead and assign it but

otherwise we'll skip it

first thing we need to do is get the

asset name

so this will give us air conditioning

here and if we needed this version this

is zero one probably get rid of that

that underscore there so that it

wouldn't it wouldn't fail this test

and then down here in our list of

textures

so this would save us if we had a lot of

textures we would make sure that we're

only assigning the appropriate texture

based on the naming convention the other

thing that would be cool is if we could

save these assets

we'll use editor asset library has a

method called save assets but I need to

create another list up here

because again we don't know how many

material instances we're going to be

making

and then we can throw all the new stuff

into a list here

and this would be looking for a path

and there you go

there are probably a lot more things we

could do with this in terms of features

and bulletproofing but this covers most

of the moving parts

these kinds of quality of life tools can

make a big difference in your project

and I highly recommend looking for

opportunities to automate processes that

are repetitive or tedious or prone to

human error I hope you've enjoyed these

videos I'd appreciate you taking time to

watch them I'll be posting the commented

code on my unreal developer Network page

please feel free to post questions there

or in the comment section below thanks

CODE:
def buildSelectedAssets(folderPath,fileNames):
    """
    Sets up static mesh, material instances, and textures.  Args passed in by import script.
    """
    # lists to hold new assets
    textures = []
    geo = []
    materialInstances = []
    # create asset tools instance
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    EAL = unreal.EditorAssetLibrary()
    # hard coded path to parent material
    materialParent = EAL.load_asset('/Game/Meshes/ImportTest/M_parent')
    # get all assets in folder path
    for assetPath in EAL.list_assets(folderPath):
        # clean up asset path
        assetPath = assetPath.split('.')[0]
        # identify newly import assets
        # load assets, located file import path, and compare to file import paths passed in from import script.
        asset = EAL.load_asset(assetPath)
        try:
            assetImportData = asset.get_editor_property('asset_import_data')
            importfilePath = assetImportData.get_first_filename()
            if importfilePath in fileNames:
                if isinstance(asset, unreal.StaticMesh):
                    geo.append(asset)
                if isinstance(asset, unreal.Texture):
                    textures.append(asset)
        except AttributeError: # not all assets have asset import data
            pass
    for staticMesh in geo:
        # get asset name from static mesh to find textures later
        assetName = staticMesh.get_name().split('_')[1]
        # iterate over all static materials associated with mesh
        for staticMaterial in staticMesh.static_materials:
            # get the index of the current static material for later
            index = staticMesh.static_materials.index(staticMaterial)
            # locate and delete the default material created on import
            matPath = staticMaterial.material_interface.get_path_name()
            unreal.EditorAssetLibrary.delete_asset(matPath)
            # create new material instance
            materialInstance = assetTools.create_asset(
                staticMaterial.material_slot_name,
                folderPath,
                unreal.MaterialInstanceConstant,
                unreal.MaterialInstanceConstantFactoryNew(),
            )
            materialInstances.append(materialInstance)
            # set parent material
            materialInstance.set_editor_property('parent', materialParent)
            # assign new material instance to correct material slot
            staticMesh.set_material(index, materialInstance)
            # iterate over textures
            for texture in textures:
                # identify textures associated with asset by naming convention
                if assetName in texture.get_name():
                    # get parameter name from texture name - i.e. T_Airconditioner_BC -> BC
                    parameterName = texture.get_name().split('_')[-1]
                    # set up material instance parameter
                    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                        materialInstance,
                        parameterName,
                        texture
                )
    # save all new assets
    newAssets = [geo,textures,materialInstances]
    for list in newAssets:
        for asset in list:
            unreal.EditorAssetLibrary.save_asset(asset.get_path_name())