This is a step-by-step instruction manual to recreate our AgriSense system, including Openstack network setup, raspberry pi setup, sensor setup, and the connection of the whole system.


# Step 1: Create Our Openstack Cloud System

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

I only had the nova availabilty zone available, and leaving nothing chosen for this is equivalent to choosing all zones, so it didn't matter what I did here. If you've got other zones, use the one I imagine you've made solely for this system.

### Subnet

    Subnet Name: AgriSenseSubnetA
    Network Address: 192.168.50.0/24 
    IP Version: IPv4
    Gateway IP: 

__Subnet Name__

Same situation as as every other time we pick a name

__Network Address__

Doesn't matter too much, must follow A.B.C.D/E pattern though, I described how the bitmask stuff works in one of my SessionNotes files, but the basic gist is devices on this network should have the IP A.B.C.X, where the X is replaced by a preferably unique number.

__IP Version__

IPv6 is becoming the new standard but IPv4 works fine for us and its the default so just leave it

__Gateway IP__

Leave blank, this will get auto-assigned and it doesn't matter too much to us what it gets set to.

### Subnet Details

I didn't touch this at all so leave it alone. It's advanced configuration and unnecessary for us to fiddle with.

## Network continued

Now that the network has been created, go to Subnets (if you aren't already there) and make note of the Network Address for the subnet you created. This is the [Network Address] and we will need it later.

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

This is important to set now because as far as I can tell you have to create a new router if you forget to set this here.

The external network allows our router to connect to the internet (through the production network) and therefore the outside world, including our raspberry pi.

__Availability Zone Hints__

Same as before

## Router Continued:

Once created, click on the newly added to inspect it. Click on the Interfaces tab inside it and Add Interface:
    
    Subnet: AgriSenseSubnetA
    IP Address: 

Finally, since we set an External network when we created the router, if you go to Overview, under External Gateway you will see External Fixed IPs.
Make note of the IP Address that has been assigned, this is our [Router IP] that will we use later.
__Subnet__

Connecting the router to this subnet means that we now have a route from the outside world to our private network (AgriSenseNetwork) and subnet (AgriSenseSubnet). Now devices connected to that private network are able to access the outside world.
To allow the outside world to access our devices, we will need to configure security groups for these devices to use.

__IP Address__ 

Leave empty. it'll auto-assign and it doesn't matter too much exactly what it gets

## Instance:

On the left, click on Compute -> Instances. Then Launch Instance in the top of right

### Details

    Instance Name: AgriSenseServer
    Description: 
    Availability Zone: nova
    Count: 1

__Instance Name__

Again, just an example name to keep referring to

__Description__

Completely up to you what you put here, I'm leaving it empty because I don't believe a description is *needed* unless we have a more complicated system and we need to make sure it's clear what's what.

__Availability Zone__

Leave it as it was by default.

__Count__

We only need 1 instance of the server, so only create 1 

### Source
    
    Select Boot Source: Image
    Create new Volume: Yes
    Delete Volume on Instance Delete: No 
    Volume Size: 

Then further down the page click on the Up arrow next to Ubuntu 22.04 Server Template to use it as our Operating System for this image

__Select Boot Source__

An image is an Operating System with RAM and all that, i.e. a computer.

__Create new Volume__

This yes choice just makes it easier. If you have some storage you already have and want to use that, select No and select that storage volume.

__Delete Volume on Instance Delete__

We won't be deleting the instance anyway, but this makes sure the data we save to the server from the raspberry pi doesn't get deleted if we delete the server instance by accident or some other reason

__Volume Size__

Leave this one alone, it will automatically get changed according to our other choices, we don't currently need to manually set it to anything higher.

### Flavour

Find base.m5 and click the Up arrow next to it to choose it. Realistically we would be fine using an alternative flavour with lower storage/speed, but this closely matches the RaspberryPi's specifications.

### Networks

Press the up arrow next to AgriSenseNetwork to connect this device to that network.

## Instance continued

Go to the instance you created and go to Overview, below, under IP Addresses you should see AgriSenseNetwork and an IP Address next to it, make note of this [Server IP] for later.

## Security Groups

When we attempt to connect the raspberry pi to our server, if we use the default security group setup then our router will block certain network signals from reaching our devices on the private network. To fix this issue and confirm our raspberry pi has connected to our devices, we need to allow certain requests.

Go to Network -> Security Groups and Create Security Group, again name it whatever as long as it's recognisable. I'm not an expert on security so there's probably a few security risk with these, but create these two rules by pressing Add rule to add each one:

### Rule 1

    Rule: All ICMP
    Description: 
    Direction: Ingress
    Open Port: Port Range
    From Port: 12000
    To Port: 13000
    Remote: CIDR
    CIDR: 0.0.0.0/0

__Rule__

ICMP requests, for all I care, are ping requests used to test connection speed. This rule allows outside devices to ping our devices to test connection

__Description__

Up to you

__Direction__
Ingress is **incoming** to our devices from external sources
Egress is **outgoing** from our devices to external sources
We want ingress here because it will allow our raspberry pi to ping our server to make sure it can access it.

__Open Port / From Port / To Port__

Port Range is chosen so we have a few ports to choose from. As far as I'm aware it doesn't matter which ports we open, but I chose these ones because 1000 is a nice number and one of the examples from our lab uses port 12345 by default, which is contained within this range.

__Remote / CIDR__

CIDR is chosen to base our incoming connection filters by IP Address, I think using security group would only allow connections from our instances using that group.
I think here leaving them as 0s allows for ANY IP to get through via this rule. Our Raspberry Pi uses 172.22.250.0/24 (maybe) so if we wanted to filter it we'd set it to that - but I might be wrong on how that works, all I know is that leaving it as 0s allows the pi to ping.

### Rule 2

    Rule: Custom TCP Rule
    Description: 
    Direction: Ingress
    Open Port: Port Range
    From Port: 12000
    To Port: 13000
    Remote: CIDR
    CIDR: 0.0.0.0/0

This is mostly the same as the other one, but allows for TCP connections instead of ICMP, which we use to transmit data to our devices from the raspberry pi.
I'm not sure, but All TCP would probably be fine too, I think it just auto-allows ALL ports to be used.

## Security Groups continued

Go to Network -> Networks and click on AgriSenseNetwork then on Ports. We are now going to apply these new rules to our server so that the raspberry pi can communicate with it.

Click on Edit Port on the row with the [Server IP] from earlier, then click on Security Groups. I'm not sure if having the default group in addition will cause conflicts (it's probably fine), but I removed them all and then assigned only the one we created with the ICMP and TCP rules.

## Finished!

I think now everything on the Openstack end is sorted, now we move on to the Raspberry Pi!

# Step 2: Raspberry Pi Connection
I don't have access to the raspberry atm so I can't verify these steps, but:

Our raspberry pi was already set up with the basics, so these instructions will be used to confirm a solid connection between the pi and our openstack server.

Open a terminal on the Raspbery Pi and type 

    sudo route add -net [Network Address] gw [Router IP] dev wlan0

where the bits in square brackets you will have hopefully made note of before (otherwise you can go back and re-obtain this information by logging to openstack and checking again).
If it doesn't work it might be fixed if you 

    sudo apt install net-tools

After this, make note of the IP of the device, gotten by typing "ifconfig" and pressing enter in the terminal. If it doesn't work try the command above if you hadn't already. If there are still errors here then give up, its so over (not really, I just don't know what to do since we didn't get these problems).
I believe the ip will be next to "inet" and ours was X.X.X.141 

Then on Openstack, go to Computer -> Instances -> AgriSenseServer -> Console and open it in fullscreen with the hyperlink it shows.

In this, type "ping [RaspberryPiIP]". Hopefully it will work and you will see it repeatedly send a signal to the Pi and time how long it takes for the signal to get back.

Then, on the raspberry pi, type "ping [Router IP]" to ensure the Pi can reach the network, and then try "ping [Server IP]" to test server connection. If the router ping goes through but the server ping fails you may have made an error in the Security Groups configuration.

## Important Notes

Every time you restart the raspberry pi, you will need to re-run 

        sudo route add -net [Network Address] gw [Router IP] dev wlan0



# Raspberry Pi to ESP32

//to connect and transfer/erase/whatever else data to/from it, tap the RST button once when "Connecting..." shows up on whatever youre doing (e.g. esptool erase-flash, upload on arduino IDE)
// this puts the esp32 into download mode and makes sure not to prevent serial data being transferred

//on my home pc
used this https://www.youtube.com/watch?v=4ZEPPQLY5o4

