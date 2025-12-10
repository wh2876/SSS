# Step 1: Create Network

## Network:

In Openstack, on the left, click on Network -> Networks. Then "Create Network" in the top right. Under each subheading use these settings:

### Network
    Network Name: "AgriSenseNetwork" 
    [x] - Enable Admin State
    [x] - Create Subnet
    Availability Zone Hints: []

__Name__

Name can be whatever you want, I'm using AgriSenseNetwork for if ever I refer back to this network we've created.

__Admin State__

Not sure if this is needed, but I left it ticked because it was ticked by default

__Create Subnet__

At least 1 subnet is **required** in order to properly connect the network to the other components of our system. The details of them get set in the next tab, and if you accidentally untick this option and finish creating the network early it doesn't matter too much because you can add new subnets to a network whenever you want.

__Availability Zone Hints__

This is stuff beyond our scope, so we just don't touch it since we don't need to. "nova" was the only thing in the box for me which I believe is relevant but isn't something we concern ourselves with too much.

### Subnet

    Name: AgriSenseSubnetA
    IP: 192.168.50.0/24

TBD on ACTUAL specifics, I can't access openstack atm to see what the settings were. I've filled in what I think there was to set

__Name__

Same situation as as every other time we pick a name

__IP__

Doesn't matter too much, must follow A.B.C.D/E pattern though, I described how the bitmask stuff works in one of SessionNotes files, but the basic gist is devices on this network should have the IP A.B.C.X, where the X is replaced by a number that no other device on the network is using?

### Subnet Details

Don't think I touched this at all so leave it alone

## Router:

On the left, click on Network -> Routers. Then Create Router in the top right and use these settings:

    Router Name: AgriSenseRouter 
    [x] Enable Admin State
    External Network: production 
    Availability Zone Hints: []

__Router Name__

Again, just a name

__Enable Admin State__

Again, not sure if this is needed but I left it ticked because it was ticked by default

__External Network__

Make sure to pick the one NOT marked "old production".
This is important to set now because as far as I can tell you have to create a new router if you forget to set this here Also make sure to pick the one NOT marked "old production".

The external network in this case allows our router to connect to the internet (through the production network) and therefore the outside world, including our raspberry pi.

__Availability Zone Hints__

As with the network, leave it.

## Router Continued:
Once created, click on the newly added to inspect it. Click on the Interfaces tab inside it and Add Interface:
    Subnet: AgriSenseSubnetA
    IP Address: //leave empty to let it auto assign
__Subnet__
Connecting the router to this subnet means that we now have a route from the outside world to our private network (AgriSenseNetwork) and subnet (AgriSenseSubnet). Now, devices connected to that private network are able to access the outside world.
Some of the later steps are needed to be taken in order to let the outside world access our private network devices though.

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
