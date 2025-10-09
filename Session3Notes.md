# Task 01 - Security Groups

- Created a security group as per lab sheet, then created a rule. The lab sheet is confusing, it tells you how to get to the add
rule bit and then tells you to repeat the previous step and then tells you to delete some of the security groups. Why?

Anyway I just deleted the security group I made so all I have is the default one. 
I believe the security groups - at least the Custom TCP one - is for limiting which devices can connect based on their IP.

# Task 02 - Creating Instances


### Cinder Volume (CONT.)
I do not know what a cinder volume is or why it is used exactly. I think it is a type of architecture that provides the volumes for instances that makes them easy to manage and modify.

## Creating an Instance
Instances make up much of the data and processing power parts of the system. They can be found by going to Compute->Instances, and have many customisation options, such as:
### Sources
Image, Instance Snapshot, Volume, Volume Snapshot are the options.
- Image is a basically a new computer - an OS, Storage, RAM, etc. combo
- Instance Snapshot I believe is a copy of an existing instance.
- Volume is *just* storage I believe
- Volume Snapshot is a copy of an existing Volume.

Then you choose the size of it, the minimum value is based on the size of the OS and available Flavours (next section), 
so will get automatically adjusted depending on which OS template you choose for your instance if you choose an Image (i.e. Ubuntu, Windows, etc.)

### Flavour
Flavour is the hardware specification like RAM, (Virtual) CPU count, and storage size. You are presented with set options with names like 
base.m1, base.m2, huge.m1, etc. which have set combinations of RAM, SSD size, and VCPUs

### Network
Then you may select networks this instance is connected to, the first customisation option so far to allow multiple selections.

### Ports
Then you get to select ports, which you can use instead of - or alongside - networks. 
I'll admit I'm not sure exactly why you'd want this but I think it makes it so it has a consistent exact address on a network.

### Security Groups
You can select which security groups apply to this instance in order to set a limit on which devices can connect to it (among other things probably. Requires further investigation of security groups).

### Key Pair
Allows you to set key pairs related to this instance to quickly get in without having to re-type username and password n stuff.
You can create and import them here.

### Configuration / User Data
If you want to set up the instance quickly (like custom programs and stuff) you can provide a setup script to do it all automatically

### Server Groups
This allows you to instantly connect the instance to existing servers. We haven't done anything with servers yet so I can't write anything specific about this.

### Metadata and Scheduler Hints
No idea what these do/are

# Task 03 - Using the Instance
Compute -> Insatance
