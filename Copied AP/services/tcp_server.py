import argparse
import numpy as np
import pickle
import shutil
import socket
import threading
import time


class EMGTCPServer:
    def __init__(self, host='localhost', port=12345, pkl_file='recording.pkl'):
        self.host = host
        self.port = port
        self.pkl_file = pkl_file
        self.server_socket = None
        self.clients = []
        self.running = False
        self.data = None
        self.sampling_rate = None
        self.CHANNELS = 32
        self.SAMPLES_PER_PACKET = 18
        self.load_data()

    def load_data(self):
        """Load the EMG data from the PKL file"""
        try:
            with open(self.pkl_file, 'rb') as f:
                self.data = pickle.load(f)
            self.emg_signal = self.data['biosignal'][:32, :, :]
            self.sampling_rate = self.data['device_information']['sampling_frequency']
            print(f"Data loaded successfully. Shape: {self.emg_signal.shape}")
            print(f"Sampling rate: {self.sampling_rate} Hz")
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def print_data(self, data, window_index):
        # skip, if printing disabled
        if args.ndp:
            return

        # set terminalbreite, um vorzeitiges umbrechen zu verhindern
        terminal_width = shutil.get_terminal_size((100, 20)).columns  # fallback: 100 Zeichen
        np.set_printoptions(linewidth=terminal_width)

        """Print the current chunk of data"""
        print(f"\x1b[HSending window {window_index}:" + (" " * 30))
        print(f"Shape: {data.shape}" + (" " * 30))
        print("Data values:" + (" " * 30))
        for i in range(data.shape[0]):
            line = f"Channel {i+1}: {data[i, :]}"
            padded_line = line.ljust(terminal_width)  # mit Leerzeichen auffüllen
            print(padded_line)
        print(" ".ljust(terminal_width))
        print(" ".ljust(terminal_width))
        #print("-" * 50)

    def start(self):
        """Start the TCP server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"Server started on {self.host}:{self.port}")

        # Start accepting connections in a separate thread
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()

    def accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"New connection from {address}")
                self.clients.append(client_socket)
                # Start a new thread to handle this client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")

    def handle_client(self, client_socket):
        """Handle a single client connection"""
        try:
            # Get the total number of windows
            num_windows = self.emg_signal.shape[2]
            window_index = 0

            while self.running and window_index < num_windows:
                # Get the current window of data
                current_window = self.emg_signal[..., window_index]
                
                # Print the data before sending
                self.print_data(current_window, window_index)
                
                # Convert the data to bytes and send
                data_bytes = current_window.tobytes()
                client_socket.sendall(data_bytes)
                
                # Calculate sleep time based on original sampling rate
                # Since we're sending 18 samples at a time, we need to adjust the sleep time
                sleep_time = self.SAMPLES_PER_PACKET / self.sampling_rate
                time.sleep(sleep_time)
                
                window_index += 1

                # loop around if we reach the end of the data
                if window_index >= num_windows:
                    window_index = 0
                    print("Restarting data transmission from the beginning.")

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()

    def stop(self):
        """Stop the TCP server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for client in self.clients:
            client.close()
        self.clients.clear()
        print("Server stopped")

if __name__ == "__main__":
    # disable debug output if has "--ndp" (short for no data print)
    parser = argparse.ArgumentParser()
    parser.add_argument('--ndp', action='store_true', help='Does not print the sent data')
    args = parser.parse_args()

    # Create and start the server
    server = EMGTCPServer()
    try:
        server.start()
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop() 