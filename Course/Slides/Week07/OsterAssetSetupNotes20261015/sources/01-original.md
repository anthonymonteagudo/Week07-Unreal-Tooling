![[Pasted image 20261015024355.png]]

![[Pasted image 20261015024020.png]]

![[Pasted image 20261015024041.png]]

![[Pasted image 20261015024243.png]]

![[Pasted image 20261015024308.png]]

![[Pasted image 20261015024421.png]]

![[Pasted image 20261015024434.png]]

![[Pasted image 20261015024450.png]]

![[Pasted image 20261015024615.png]]

![[Pasted image 20261015024630.png]]

![[Pasted image 20261015024928.png]]

![[Pasted image 20261015025030.png]]

![[Pasted image 20261015025201.png]]

![[Pasted image 20261015025301.png]]

![[Pasted image 20261015025337.png]]

![[Pasted image 20261015025347.png]]

![[Pasted image 20261015025315.png]]

![[Pasted image 20261015025523.png]]

![[Pasted image 20261015025817.png]]

![[Pasted image 20261015025912.png]]

![[Pasted image 20261015030201.png]]

![[Pasted image 20261015030212.png]]

hi there my name is Isaac Oster and in

this video we're going to talk about how

to import these assets piece of geometry

and some textures into an unreal project

and then create a material instance that

uses this as its parent and then plugs

these Textures in and applies it to the

material slot so this is going to be

based on or extending the previous two

videos the first one covers exporting a

selection that you have in the content

browser and then the second video covers

importing an asset from a file path or

in this case several assets so I've

added a few lines to both of these the

first line that I added is setting an

attribute to replace existing to true

for our asset import data so that it'll

just override anything that happens to

be in the project already and then the

other thing that I added is a little

section here that will handle selected

textures now probably the better way to

do this would be to detect the textures

that are associated with static mesh and

then just run them through this is like

a separate process but anyway this is

how you would do that if you wanted to

just handle a selection other than

geometry all right so the first thing

I'm going to do is create a new function

called build selected assets

and I am going to create a reference to

this object this material

and then I just need to get the path so

I'm going to right click over here and

copy file path probably okay

paste it in and then I'm just going to

clean this up a little bit so

we basically want to go to content and

replace that with game

and it needs a forward slash

and then we want to just take off that

you asset at the end

that'll give us a reference to the

material parent so the next thing we

need to do is get a reference to our

imported objects and I'm going to go

ahead and just run this

we don't have to call this yet but

everything else should work just fine as

is

looking for asset importer

all right so here's our new objects

ultimately we're going to delete this

this is the material that comes in by

default with the fbx

but we can hold off on that for just a

moment first we have to identify it

so we have some information here that's

very useful which is the import file

paths so what we can actually do is go

through everything in the folder that we

just imported our assets into and track

down you can see at the bottom there of

that source file if we double click it

and then scroll down a bit

see file path so this is right now it's

it's giving a relative path but it has

access to the full thing and so we can

actually compare this data for every

single asset in our folder here to our

paths to say like yes this is something

that I just imported or know this is

something that was here before because

we don't really want to mess with

whatever assets might already be in this

folder I'm going to be using another

method here on editor asset Library

called list assets we feed it a

directory path and it'll give us the

asset paths for everything that is in

the directory

and because I'm going to be using the

editor asset Library a few times I'm

just going to create a single instance

of it

so I'm going to need a directory path

and I have it right here

so I'm going to go ahead and just set up

a function call inside import assets

and we'll just add an argument here

called folder path

so now when this function is called

it'll be passed whatever this happens to

be which is something you would probably

want to get user data from via you know

UI or something

so now we've got the asset paths that

are associated with every asset in the

folder

and now we need to load the asset

but it might actually complain there's a

there's a change to how the asset paths

are handled I'll go and print the asset

path real quick so we can take a look at

it

right so these are the asset paths for

everything in there and it does this

little thing here which didn't used to

be a problem but now is a problem if you

were to try to load this asset it'll

complain I'll go ahead and do that

really you just gotta trim everything

past that dot and it'll work just fine

but we can go ahead and run through the

regular process using load asset

to show you the issue

and I'll set this

equal to asset

right so this is the issue here try

convert file name to Long package name

was passed blah blah blah so if you if

you're getting this error the the

problem is you've got to remove that

last little bit from the path there so

we'll just try this

right and now it's happy

so now that we've got the assets we can

get the import file path assuming it has

one

we can take a look here at the

documentation for static mesh it has an

editor property called asset import data

which will return the asset import data

object associated with static mesh and

on the asset import data object we have

a method get first file name which will

return the import file path for the

asset

anything that's been imported will have

an asset import data object but any

native unreal objects such as a material

will not so we need to have a little

check in here that will add momentarily

so we'll grab the asset import data

editor property

and from the asset import data

we'll use get first file name

and we'll just print the import file

path

now this is going to yield an error

because not everything in here has an

asset import data object but let's take

a look at what that error looks like

so you can see there's an attribute

error none type object has no attribute

get first file name

so what we've done here is we've asked

for the asset import data object

associated with the asset and then we

are calling this method here but if this

returns as none obviously this method

doesn't exist on none so that's what the

issue is so we can do a tricceptor

and let's run it again

and here you can see all of our import

file paths for the textures and then

here is the geometry as well so now that

I've got the import file paths for all

the Assets in the directory at least the

assets that have import file paths I can

compare them against the files that I

just imported and identify the new

Assets in here that need to be set up

so I'm going to need to pass in my list

of file names

so I'll just add another argument

and rather than printing this we're

going to do a little comparison

and then we need to identify whether or

not it is a texture or a piece of

geometry

so I'm just going to create a list up

here

all right so

if I can find the import file path

associated with the asset in my list of

recently imported assets

then I'm going to do a text see if it's

either a static mesh or a texture and

then put it into the appropriate list

in the next video we'll take a look at

how to identify and delete the default

material created when we imported the

geometry how to create a new material

instance and assign the material parent

how to assign the textures and then how

to take that new material instance and

assign it to our geometry