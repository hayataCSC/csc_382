#!/usr/bin/env python3
import sys
from urllib.parse import urlparse
from socket import *

# Helper func for forming a request HTTP request message
def createHttpRequest(path, host):
  return f'GET {path} HTTP/1.1\r\nHOST: {host}\r\nConnection: close\r\n\r\n'

# Helper func for getting contenet length from the response header
def getContentLengthFrom(header):
  return header.split('Content-Length: ')[1].split('\r\n')[0] 

# Helper func for getting status code from the response header
def getStatusCodeFrom(header):
  return header.split(' ')[1]

# Helper func for writing content to a file
def saveContent(filePath, content):
  with open(filePath, 'w') as f:
    f.write(content)

# Helper func for getting header and content from the socket connection
def getHeaderAndContent(socket):
  buffer = ''
  header = ''

  while True:
    # Get response and decode it
    response = socket.recv(1024)
    buffer += response.decode()
    # Get the index of the blank line if any
    index = buffer.find('\r\n\r\n')
    # If there is a blank line in buffer...
    if (index != -1):
      # Get the header from the buffer string
      header = buffer[0:index]
      # Save the leftover (beginning of content) to buffer
      buffer = buffer[index+4:]
      # End the while loop
      break;

  # Get the content length from the response header
  contentLength = int(getContentLengthFrom(header))

  # While the buffer string is less then the content length...
  while (len(buffer) < contentLength):
    # Get response and decode it
    response = socket.recv(1024)
    buffer += response.decode()

  return header, buffer
          

# Get the url and file path from the CL arguments
url = sys.argv[1]
filePath = sys.argv[2]

# Parse the url
urlInfo = urlparse(url)
# Get the hostname and path
host, path = urlInfo.hostname, urlInfo.path
# Get
path = path if path != '' else '/'
# Get the port number (use 80 if port number is not specified)
port = int(urlInfo.port) if urlInfo.port else 80

# Compose HTTP request message
httpMsg = createHttpRequest(path, host)
print('--- request header ---\n', httpMsg)

# Connect to the web server through TCP and send HTTP request
socket = socket(AF_INET, SOCK_STREAM)
socket.connect((host, port))
socket.send(httpMsg.encode())

# Get header and content from the response
header, content = getHeaderAndContent(socket)

print('--- response header ---\n', header)

# Get the status code from the response header
statusCode = getStatusCodeFrom(header)

statusCode = 200

# If status code is 200, save the content to the file
statusCode == 200 and saveContent(filePath, content)
