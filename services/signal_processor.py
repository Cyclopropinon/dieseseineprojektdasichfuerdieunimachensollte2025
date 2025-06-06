import socket
import time
import numpy as np


class Signal_Receiver_TCP:
    def __init__(self, host='abcde', port=80):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.no_of_channels = 32
        self.samples_per_channel = 18
        self.total_samples = self.no_of_channels * self.samples_per_channel

    def connect(self):
        ## This method is used to connect to the TCP server.
        ## Returns: Boolean value:
        ## 1). True - when it is connected successfully
        ## 2). False - when connection fails.

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## creates a socket using IPv4 addresses

            self.socket.connect((self.host, self.port)) ## connects to da TCP server
            self.is_connected = True ## sets value to True if connection succesful
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False ## returns false if connection has epic fail

    def receive_data(self):
        ## This method receives the data from the TCP server only if the connection is successful
        ## The "data" is of type bytes. We decode it to string using utf-8 and then strip of any leading spaces/tabs, etc.
        ## We then convert the string in to list of strings of floats
        ## The list contains samples and timestamps
        ## Then the strings are converted into floats
        ## We then convert this into a 2D array.
        ## Returns "channel_data" which is a 2D array in shape (no_of_channels, samples_per_channel)
        if not self.is_connected:
            print("Not connected to the server")
            return None

        try:
            # Receive data
            # Each value is a float (4 bytes)
            buffer_size = self.total_samples * 4
            data = self.socket.recv(buffer_size)

            if not data:
                print("Connection closed by server")
                self.is_connected = False
                return None

            # Decode and parse the received data
            # Format: t1,ch1_sample1,ch2_sample1,...,ch32_sample18
            decoded_data = data.decode('utf-8').strip()
            values = decoded_data.split(',')

            if len(values) != self.total_samples:
                print(f"Invalid data size. Expected {self.total_samples} values, got {len(values)}")
                return None

            # Convert values to float and reshape into channels × samples
            data_values = [float(x) for x in values]
            channel_data = np.array(data_values).reshape(self.samples_per_channel, self.no_of_channels+1) ## +1 cuz of timestamp


            return {
                'data': channel_data
            }

        except Exception as e:
            print(f"Error receiving data: {e}")
            self.is_connected = False
            return None

    def close(self):
        ## This method is used to disconnect to the TCP server
        if self.socket:
            self.socket.close()
            self.is_connected = False
            print("Connection closed")

'''
# Example usage:
if __name__ == "__main__":
    ##receiver = Signal_Receiver_TCP()

    if receiver.connect():
        try:
            while receiver.is_connected:
                data = receiver.receive_data()
                if data:
                    print(f"\nReceived data chunk:")
                    print(f"Shape of data: {data['data'].shape}")
                    print(f"Channel 0 first 3 samples: {data['data'][0, :3]}")
                    print(f"Channel 31 last 3 samples: {data['data'][31, -3:]}")
                time.sleep(0.1)  # Small delay to prevent CPU overuse
        except KeyboardInterrupt:
            print("\nStopping receiver...")
        finally:
            receiver.close()

'''