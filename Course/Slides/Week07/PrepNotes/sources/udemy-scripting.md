Minimal Valuable Python Scripting Knowledge (for Tech Artist)
	1. Data Types
	2. Conditions and Loops
	3. Functions
	4. Imports
	5. Files Scrapping

Basic Data Types
	Integers, Floats
		my_int = 1
		my_float = 2.5
	Strings
		my_string = "Victory"
	Lists
		my_list = ["Slava", "Olya", "Andrii"]
	Dictionaries
		my_dictionary = {"player": "vmakhynko", "score": 15}

Conditions and Loops
	If-Elif-Else
		temperature = 25
		if temperature > 30:
			weather_condition = "Hot day!"
		elif temperature > 20:
			weather_condition = "Nice weather."
		else:
			weather_condition = "Cool day."
	For Loops
		fruits = ["apple", "banana", "orange"]
		for fruit in fruits:
			print("I have a ", fruit)
	While Loops
		counter = 1
		while counter <= 5:
			print("counting", counter)
			counter += 1

Functions
	Overview: The building blocks of structured code wherein you can reuse those blocks in various places and needs.
	Parameters
		Information the function accepts. They are like settings that help your function do the job the way you want.
		def greet(name):
			print("Hello, " + name + "!")
	Arguments
		When you use or call a function, you provide it with some information. The actual values or data that the function will work with based on the parameters you set.
		greet("Alice")
	Return
		Functions also give back information after doing their job. It is like getting the results from the function to use it in your script further on.
		def multiply(a, b)
			result = a * b
			return result
	Scopes
		Two types of scopes: global and local. To understand them, understand them you can think of your program like a big house... Global scope is like stuff everyone in the house can use; Local scope is like stuff that only belongs to a specific room and cannot be used by other rooms.
		
		global_variable = 10
		def update_global():
			global global_variable
			global_variable += 5
			local_variable = 15
			print("Inside the function - Global variable:", global_variable)
			print("Inside the function - Local variable:", local_variable)
	
	Calling the Function
		update_global()

Importing
	Think of importing as adding special tools to your script, making it more powerful and versatile. 
		You can import an entire module - like bringing a complete toolbox.
		You can use importing with an alias - which is like giving a nickname to your toolbox for easier use
		You can import just specific functions from the module - like grabbing just the tools you need for the particular job from the whole toolbox.
		
	// Importing the entire os module
	import os
	
	// Using function from the os module
	current_directory = os.getcwd()
	print("Current Directory: ", current_directory)
	
	// Importing the os module with an alias
	import os as operating_system
	
	// Using the alias to call functions
	home_directory = operating_system.path.expanduser("~")
	print("Home Directory:", home_directory)
	
	// Importing specific functions from the os module
	from os import listdir
	
	// Using the imported functions directly
	files_in_directory = listdir(current_directory)
	print("Files in Current Directory Directory:", files_in_directory)

Working with Files
	Synopsis: Core aspect of automation in this area
	1. OS lib
		Super useful pack of functions to work with files. 
			For example, to check if a file exists before trying to access it, or to build a dynamic path which is required for handling diverse data sets or files located in different folders.
	2. Read/Write file
		Mastering file input and output operations allows you to handle tasks like configuration management, logging, and data manipulations.
	3. .xml / .json parsing
	
	import os
	import json
	import xml.etree.ElementTree as ET
	
	// Working with the os module
	file_path = "example.txt"
	
	// Check if a file exists
	if os.path.exists(file_path):
		print(f"The file {file_path} exists.")
	else:
		print(f"The file {file_path} does not exist.")
		
	// List all files in the directory
	files_in_directory = os.listdir(os.getcwd())
	print("Files in Current Directory:", files_in_directory)
	
	// Reading and writing to a file
	// Writing to a file
	with open("example.txt", "r") as file:
		content = file.read()
		print("File Content:", content)
		
	// Reading from a file
	with open("example.txt", "r") as file:
		content = file.read()
		print("File Content:", content)
	// Parsing JSON
	json_data = '{"name": "John", "age": 30, "city": "New York"}'
	parsed_json = json.loads(json_data)
	print("Parsed JSON:")
	for key, value in parsed_json.items():
		print(f"{key}: {value}")
	// Parsing XML
	xml_data = '<person><name>Anna</name><age>25</age><city>San Francisco</city></person>'
	root = ET.fromstring(xml_data)
	print("Parsed XML:")
	for child in root:
		print(f"{child.tag}: {child.text}")

Tool Should Work
	Do not optimize unless needed!
		Tech Artists don't usually need to worry too much about how fast their code runs.
		The main thing is making sure code works WELL and gives the right results every time. Since those scripts are like handy tools to do specific jobs, not game code. Just focus on making sure code works well!

Things to Learn Further
	Learn mentioned basics of Python
		Don't necessarily need to dive too deeply. Could stop after classes. Most important: APPLY knowledge and PRACTICE.

Understanding Max Script
	Max Script: In-house 3DS Max Scripting solution. Empowers technical artists to automate repetitive tasks to create custom tools and extend overall functionality of 3DS Max.

Capabilities of Max Script
	Automate Tasks
	Build Custom Tools
	Modify Scenes
		Manipulate objects, materials, lights, and more within the 3ds Max scene
	Access and Manage Data
	Interact with UI and many more

Max Script vs Python
	Use Python over MS whenever possible
		Python is often considered more versatile, especially across software. So highly advised to focus on Python as opposed to Maxscript.

Max Script code example

	-- Create a loop to generate a grid of cubes
	for i = 1 to 5 do
	(
		for j = 1 to 5 do
		(
			-- Create a cube
			local cubeObj = box length:10 width:10 height:10 pos:[i*20, j*20, 0]
	
			-- Generate a random color
			local randomColor = [random 1.0, random 1.0, random 1.0]
	
			-- Assign the random color to the cube
			cubeObj.material = standard diffuse:randomColor
		)
	)

How to Run:
	Open 3ds Max
	Go to the Scripting Menu
	Select Max Script
	Write the script into newly opened window
	Click the Run button

Max Script code example
	Equivalent on Python:

		from pymax import runtime as rt
		import random
		
		# Create a loop to generate a grid of cubes
		for i in range(1, 6):
			for j in rnage(1, 6):
				# Create a cube
				cubeObj = rt.box(length=10, width=10, height=10)
				
				# Set the position of the cube
				cubeObj.position = [i *20, j * 20, 0]
				
				# Generate a random color
				randomColor = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
				
				# Create a Standard material
				material = rt.StandardMaterial()
				material.diffuse = randomColor
				
				# Assign the material to the cube
				cubeObj.material = material

List of Things to Learn Further
	Official Autodesk Max Script documentation
	Research more Tech Art solutions achieved with Max Script
	How to convert Max Script to Python

# Maya Embedded Language (MEL) — Lecture Summary

## Overview

This lecture introduces **Maya Embedded Language**, commonly known as **MEL**, which is Autodesk Maya’s native scripting language. The lecture follows a similar structure to the previous lecture on MaxScript, focusing on what MEL is, what it can be used for, how it compares to Python and C++, and why it is still useful for Technical Artists.

## What Is MEL?

**MEL** stands for **Maya Embedded Language**.

It is a scripting language designed specifically for **Autodesk Maya**. MEL allows users to automate Maya workflows, build custom tools, manipulate scene objects, customize the user interface, manage files, and export data.

## What Can Be Done with MEL?

MEL can be used for many common Technical Art and pipeline tasks, including:

- Automating repetitive Maya workflows
    
- Creating custom tools
    
- Manipulating objects in the viewport
    
- Saving and naming files
    
- Exporting data
    
- Building artist-friendly interfaces
    
- Customizing Maya’s UI
    
- Maintaining older Maya tools and scripts
    

## MEL vs. Python

Python is generally more versatile and widely used across the industry, but MEL still has an important place in Maya.

Knowing MEL is useful because:

- Many existing Maya tools and legacy scripts are written in MEL.
    
- Understanding MEL makes it easier to modify, optimize, and maintain older Maya scripts.
    
- Some Maya functionality is more directly accessible through MEL.
    
- MEL is especially useful for UI customization inside Maya.
    
- MEL can help Technical Artists better understand how Maya works internally.
    

For new Technical Artists, the lecture recommends prioritizing **Python first**, then learning MEL once they are more comfortable scripting.

## Code Example Discussed

The lecture presents a simple MEL script that generates a grid of cubes and assigns random colors to each cube.

![[Pasted image 20260620230730.png]]

The example demonstrates:

- Creating objects in Maya
    
- Running scripts from Maya’s Script Editor
    
- Using comments to explain code behavior
    
- Automating scene creation
    
- Assigning randomized materials or colors
    

To run a MEL script in Maya:

1. Open Maya.
    
2. Open the Script Editor.
    
3. Write or paste the MEL code.
    
4. Execute the script.
    
5. The generated objects should appear in the Maya scene.
    

A Python version of the same cube-grid script is also shown, demonstrating that many Maya scripting tasks can be done in either MEL or Python.

## Learning Resources

For deeper study, the lecture recommends:

- Autodesk Maya scripting documentation
    
- Official MEL documentation
    
- Researching MEL optimization examples
    
- Studying existing Maya tools written in MEL
    
- Comparing MEL scripts with equivalent Python scripts
    

## Key Takeaway

MEL and MaxScript are useful specialized scripting languages, but new Technical Artists should focus most of their early learning energy on **Python**.

The lecture compares this to traveling in a country where English is commonly understood: Python is like English because it works broadly, while MEL is like Maya’s native language. You can communicate with Python, but knowing MEL can give you deeper access and better control inside Maya.

## Practical Advice for Technical Artists

- Learn Python first.
    
- Learn MEL later as a Maya-specific enhancement.
    
- Be comfortable reading and modifying existing MEL scripts.
    
- Use MEL when it gives better access to Maya-specific features.
    
- Use Python for broader pipeline, automation, and cross-application workflows.
    

## Summary

MEL is Maya’s native scripting language. It is useful for automation, UI customization, scene manipulation, and maintaining legacy tools. While Python is usually the better first scripting language for Technical Artists, MEL remains valuable for anyone working deeply in Maya pipelines.

# Practical Scripting Examples for Technical Artists — Lecture Summary

## Overview

This lecture showcases five practical examples of how scripting can help Technical Artists streamline workflows, automate repetitive tasks, and improve production efficiency.

The examples are simplified and abstract, but each one could be adapted into a real production tool.

## Main Lecture Goal

The purpose of the lecture is not only to understand what each script does line by line, but also to understand **why the script exists**.

For Technical Artists, scripting is valuable because it solves workflow problems, reduces manual labor, improves consistency, and helps artists move assets through production more efficiently.

## Example 1 — Reading Performance Data from XML

The first example calculates the **average frames per second** from a performance log stored in an XML file.

### Purpose

This type of script could be used to analyze performance data from a game or tool.

### Possible Real-World Uses

- Reading performance logs
    
- Calculating average FPS
    
- Finding performance spikes or drops
    
- Comparing performance across builds
    
- Generating automated reports for artists, engineers, or producers
    

### Technical Art Value

This shows how scripting can be used not just for asset creation, but also for **data analysis** and **performance monitoring**.

## Example 2 — 3ds Max to Substance Painter Bridge

The second example is written in **MaxScript** and creates an automated bridge between **3ds Max** and **Substance Painter**.

### Purpose

The script allows artists to export a mesh from 3ds Max and load it directly into Substance Painter.

### Possible Real-World Uses

- Exporting models from a DCC
    
- Launching another production tool
    
- Reducing repetitive export/import steps
    
- Standardizing the handoff between modeling and texturing
    
- Preventing incorrect export settings
    

### Technical Art Value

This is a classic pipeline automation task. It connects two pieces of production software and removes manual steps from the artist workflow.

## Example 3 — Batch File Renaming with Python

The third example uses **Python** to quickly rename files with a `.png` extension inside a directory.

### Purpose

The script demonstrates how Python can process files in a folder and rename them according to a rule.

### Possible Real-World Uses

- Batch-renaming texture files
    
- Adding suffixes like `_Normal`, `_Roughness`, `_Opacity`, or `_BaseColor`
    
- Standardizing naming conventions
    
- Preparing textures for automatic shader assignment
    
- Cleaning up inconsistent artist file names
    

### Technical Art Value

Good naming conventions allow tools, shaders, and pipelines to understand what each file represents. A script like this can help enforce consistency across a project.

## Example 4 — Substance Painter Texture Set Validator

The fourth example is a custom tool for **Substance Painter** that checks whether a texture set resolution meets project requirements.

### Purpose

The script validates whether a texture set uses the correct resolution.

### Expanded Example

A real project might have different texture budgets for different asset types:

- Melee weapons
    
- Ranged weapons
    
- Shields
    
- Characters
    
- Props
    
- Environment assets
    

A more advanced validator could detect the asset type from the texture set name, then compare its current resolution against the approved budget for that asset category.

### Possible Real-World Uses

- Checking texture resolution budgets
    
- Enforcing asset standards
    
- Preventing oversized textures
    
- Validating before export
    
- Helping artists catch mistakes early
    

### Technical Art Value

Validation tools are extremely useful in production because they prevent problems before assets reach the engine.

## Example 5 — Maya Skeleton Automation with MEL

The fifth example uses **MEL**, Maya’s native scripting language.

### Purpose

The script automates the process of assigning bones to a skeleton in a Maya scene.

### Possible Real-World Uses

- Skeleton setup automation
    
- Rigging support tools
    
- Bone assignment
    
- Character preparation
    
- Reducing repetitive rigging tasks
    

### Technical Art Value

This example shows how DCC-native scripting languages like MEL can still be useful for specific workflows inside Maya, especially for rigging and scene automation.

## Recommended Python Libraries for Technical Artists

The lecture also introduces several useful Python libraries and APIs for Technical Artists.

## PySide / PyQt

**PySide** and **PyQt** provide Python bindings for the Qt framework.

### Uses

- Creating graphical user interfaces
    
- Building artist-facing tools
    
- Creating custom panels inside DCC applications
    
- Making tools for Maya, 3ds Max, Blender, and other software
    

### Technical Art Value

These libraries are useful when building polished tools that artists can interact with visually.

## NumPy

**NumPy** is used for numerical computation.

### Uses

- Working with large arrays
    
- Matrix operations
    
- Vector math
    
- 3D math
    
- Data manipulation
    

### Technical Art Value

NumPy is useful for scripts involving geometry, transforms, simulation data, or large sets of numerical information.

## Matplotlib

**Matplotlib** is used for creating 2D plots and charts.

### Uses

- Visualizing data
    
- Plotting performance metrics
    
- Creating graphs from logs
    
- Showing trends over time
    

### Technical Art Value

Matplotlib is helpful when a Technical Artist needs to communicate data clearly, especially for optimization or performance analysis.

## OpenCV

**OpenCV** is a computer vision and image processing library.

### Uses

- Texture manipulation
    
- Image analysis
    
- Mask generation
    
- Video processing
    
- Computer vision workflows
    

### Technical Art Value

OpenCV can be useful for automating image-based tasks, analyzing textures, or creating tools that process visual data.

## DCC-Specific Scripting APIs

The lecture also mentions several important scripting APIs and languages:

- **MEL** — scripting in Autodesk Maya
    
- **bpy** — Blender’s Python API
    
- **Substance Painter Python API** — custom tools for Substance Painter
    
- **pymxs** — Python wrapper for the 3ds Max MaxScript engine
    

## Key Takeaways

- Scripting allows Technical Artists to automate repetitive tasks.
    
- Small scripts can quickly become useful production tools.
    
- The purpose of a script matters as much as the implementation.
    
- Scripts can connect software, validate assets, process files, analyze data, and improve artist workflows.
    
- Python is especially valuable because it works across many tools and production contexts.
    
- DCC-specific scripting languages and APIs are still useful for deeper software integration.
    

## Practical Advice for Technical Artists

When studying scripts, do not only ask:

> What does each line of code do?

Also ask:

> Why was this script created?

A useful Technical Art script usually solves a real workflow problem. The best scripts are often simple, targeted, and practical.

## Summary

This lecture concludes the scripting section by demonstrating how a Technical Artist can use scripting to solve practical production problems. The examples include performance log analysis, DCC-to-texturing workflow automation, batch file renaming, texture validation, and skeleton automation.

Even a small script with only a dozen lines of code can become a valuable tool in a production pipeline.
CODE EXAMPLES
1. Parsing xml performance log file
![[Pasted image 20260620230913.png]]
2. Bridge between 3ds Max and Painter
![[Pasted image 20260620231012.png]]
3. Renaming Textures
![[Pasted image 20260620231110.png]]
4. Validating Texture Resolution in Substance Painter
![[Pasted image 20260620231232.png]]
5. Assigning Bones to a Skeleton in Maya
![[Pasted image 20260620231359.png]]
