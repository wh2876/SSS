# echo_server.py
import socket

host = '172.22.251.148'        # Symbolic name meaning all available interfaces
port = 12347     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
readingsfile = open("sensor_readings.txt","a")
while True:
  data = conn.recv(1024)
  if not data: break
  temperature,pressure,humidity = str(data).split('\'')[1].split(',')
  
  if float(temperature) < 22:
    conn.sendall(b'B')
  elif float(temperature) < 23:
    conn.sendall(b'G')
  elif float(temperature) < 24:
    conn.sendall(b'Y')
  else:
    conn.sendall(b'R')
  
  readingsfile.write( ("Temperature : " + str(temperature) + "C | Pressure : " + str(pressure) + "hPa | Humidity : " + str(humidity) + "%\n") )  
  print ("Temperature : ", float(temperature), "C")
  print ("Pressure : ", float(pressure), "hPa")
  print ("Humidity : ", float(humidity), "%")
  
conn.close()
readingsfile.close()

