# Step 1: Create Network

## Network:

In Openstack, on the left, click on Network -> Networks. Then "Create Network" in the top right. Under each subheading use these settings:
### Network
- Network Name: AgriSenseNetwork //You can put whatever you want as long as it's memorable, I'll be using this for whenever I refer back to this network we created.
- [x] Enable Admin State
- [x] Create Subnet
- Availability Zone Hints: //Don't bother touching this one
### Subnet
TBD, Can't access openstack atm to see what the options were.
Name: AgriSenseSubnetA //the A is for theoretically if we needed more (B, C, etc.). In actuality we only need this one.
### Subnet Details
Don't think I touched this at all so leave it alone

## Router:

On the left, click on Network -> Routers. Then Create Router in the top right and use these settings:
- Router Name: AgriSenseRouter //just like with network it doesn't matter too much, this is just the example name
- [x] Enable Admin State
- External Network: production //this is important to do now because as far as I can tell you have to create a new router if you forget to set this here // Also make sure to pick the one NOT marked "old production"
- Availability Zone Hints: //Again don't bother
Submit.

Once created, click on the newly added to inspect it. Click on the Interfaces tab inside it and Add Interface:
- Subnet: AgriSenseSubnetA
- IP Address: //leave empty to let it auto assign
Submit.

## Instance:

On the left, click on Compute -> Instances. Then Launch Instance in the top of right

### Details
- Instance Name: AgriSenseServer //again, just an example name to keep referring to
- Description: //Completely up to you what you put here
- Availability Zone: nova
- Count: 1
### Source
- Select Boot Source: Image
- Create new Volume: Yes
- Delete Volume on Instance Delete: No //We won't be deleting it, but this makes sure the data we save to the server from the raspberry pi doesn't get deleted if we delete the server instance 
- Volume Size: //leave this one alone, it will get automatically changed by our upcoming choices.
Then further down the page click on the Up arrow next to Ubuntu 22.04 Server Template to use it as our Operating System for this image
### Flavour
Find base.m5 and click the Up arrow next to it to choose it. Realistically we would be fine using an alternative flavour with lower storage/speed, but this closely matches the RaspberryPi's specifications.
### Networks
TBD, again I can't access openstack at the moment.
Connect to AgriSenseSubnet is all I'm aware of.


## Connecting them up

- Create server instance
- Connect them all up

Step 2: Open the port

The device added is given a Port in the Network overview. It can be recognised by it's IP!
To allow this device to receive incoming connections in a client-server model, an incoming TCP connection must be allowed through at least 1 port. To do this you must set a security group to assign to this Network Port that allows connection to a specific port on that device.
- Create a new security group and add a Custom TCP Rule and set the port to the one you will use for the incoming/outgoing connection. This can be changed to a range of ports or all ports.
- Go back to the Network -> Ports and Edit Port on the desired device, click on security groups, and assign the newly created security group with the TCP rule. now if you use the allowed ports the client-server will work.

Step 2: Set up pi

Step 3: Connect the 2

- On Openstack, go to router and make note of the IP under the "External Gateway" "External Fixed IPs" key
- Then go to the subnet of the network you have connected to both the router and the server instance and make note of the CIDR under the 

Step 4: ping

ping to the router IP not the instance IP
