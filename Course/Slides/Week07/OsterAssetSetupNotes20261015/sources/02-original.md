![[Pasted image 20261015030730.png]]

![[Pasted image 20261015030810.png]]

![[Pasted image 20261015030825.png]]

![[Pasted image 20261015030914.png]]

![[Pasted image 20261015030926.png]]

![[Pasted image 20261015031301.png]]

![[Pasted image 20261015031431.png]]

![[Pasted image 20261015031633.png]]

![[Pasted image 20261015031646.png]]

![[Pasted image 20261015031856.png]]

![[Pasted image 20261015031919.png]]

![[Pasted image 20261015031933.png]]

![[Pasted image 20261015032937.png]]

![[Pasted image 20261015032952.png]]

![[Pasted image 20261015033455.png]]

![[Pasted image 20261015033536.png]]

![[Pasted image 20261015033602.png]]

![[Pasted image 20261015033628.png]]

![[Pasted image 20261015033646.png]]

![[Pasted image 20261015033705.png]]

![[Pasted image 20261015033719.png]]

![[Pasted image 20261015033754.png]]

so our next task is going to be to

identify and remove any of the default

materials that got created on import

because we're going to want to create

material instances and then reuse the

names that are associated here with

these materials

so we can get that data from the static

mesh for each material assigned in your

DCC it's going to create a material slot

and give it a material name and a

material slot name and those will

correspond to the materials here that

get created and that comes from the

material name itself so this is Maya

there's the material name and if I were

to modify this and re-import it it would

create a new material with that new name

so I'm going to go ahead and grab this

data off of the static mesh and if we go

to the documentation for static mesh

and we scroll all the way the bottom

you're going to see there's a property

called Static materials

static material is essentially a

dictionary it's human readable

and it has some properties has a

material interface a material slot name

and the UV Channel data I'm not really

ever worried about this but these two

are pretty useful

so the material interface is essentially

a very high level grandparent material

object both material instance and

material inherit from Material interface

so what this property is doing is it's

returning back the material itself so

whatever happens to be assigned to that

slot that's going to be returned by this

property so let's go ahead and get that

also I made a little typo here that

needs to be a lowercase f

so this could arguably be a new function

but I'm going to just kind of keep it

simple here

so I'm going to get all of the static

materials associated with my static mesh

let's take a look at what it's got here

so here is our static material struct

and if we scroll down a bit we can see

we have the path to our material that we

created which is all we need to delete

this asset

deleting assets is going to be pretty

easy

let's go over to the API documentation

and we find this method here on the

editor asset Library utility class and

all it's going to take is the asset path

to delete now the static material is

actually going to return to us the

material itself so we need to get the

path

so I'm just going to print this out to

confirm that I'm actually getting the

path here of the material

so there's our path

and we'll head over try this again

all right it looks like we're getting a

warning here forced Elite object failed

to delete our material this package is

not potentially corrupt so we'll take a

look

and you can see it was removed from the

static mesh this is now using the world

grid

but the material still exists so what

I'm going to do just to make sure I've

got kind of a clean pass I'm going to

delete everything

it may be that because we're importing

assets over things that already exist

that there's some kind of a weird

permissions thing and we'll just try

this again

all right perfect so now we can see the

static mesh is assigned to the world

grid material and that material that was

created by default is now deleted all

right make your progress

now we need to make our material

instance

and to do this we're going to need to

use asset tools

asset tools that's a method on it called

create asset

and in order to create an asset tools

object you need to use the asset tools

helpers class for some reason I don't

know why that is

one of those little gotches

so we don't need to be doing this every

time

we can just create one asset tools

object

and I'm just going to copy this for my

other screen

get a set tools

now that we've got our asset tools

instance

we're going to use create asset

it's going to have a few inputs

the first will be the asset name

then the path we're going to save it

the class and the factory

as a default value for calling context

so we're not going to worry about that

we'll start with the asset name

in this case we can get it from our

static material

and it will be

the slot name

so if we take a look at our static

material documentation here's our

property

so static material dot slot name how to

commit the end there the next thing we

use the path we'll be using our folder

path

after that we're going to need

the asset class

so we can probably use material and

since if this doesn't work

we may need to use material instance

constant

which you can see right here constant

Dynamic are the two likely

Alternatives but we'll try this one

first

and then for the factory

I'm just going to add the word Factory

to my search here

and you can see we have a limited number

of options material instance constant

factoring new

so this is going to throw an error

because one of these needs to be

instantiated and I can never remember

which one

but I real will tell me

I'm going to go ahead and

add some code to delete this stuff

procedurally

try that again

all right datavize object cannot native

ice material instance constant Factory

new as object a loud class can be a

factory so this is the one we need to

instantiate and that just means we need

to add some friends at the end here

delete this stuff

all right new asset wasn't created

because the supply Factory does not

support the supply class

so that's probably this just needs to be

material instance constant

beautiful okay so here's our material

instance constant

static mesh doesn't have anything

assigned yet

this is basically totally blank which is

perfect okay fantastic in the next video

we'll take a look at setting this

material as the parent and then

assigning this material listens to this

geometry and then deciding these

textures to this material instance