import time
import secrets, ipaddress
# from dataclasses import dataclass
# from abc import ABC, abstractmethod


# class Shape(object):
#     @abstractmethod
#     def draw(self):
#         pass

# def shape_factory(shape_type: str) -> Shape:
#     if shape_type == "circle":
#         return Circle()
#     elif shape_type == "square":
#         return Square()
#     else:
#         raise ValueError("Unknown shape type")




# A basic Factory pattern to generate a valid IPv4 address

class IPv4:
    @staticmethod
    def generate() -> str:
        """Generates a random valid IPv4 address."""
        return str(ipaddress.IPv4Address(secrets.randbits(32)))
    
    def __init__(self):
        """Initializes the IPv4 generator."""
        self.address = IPv4.generate()

    def __call__(self) -> str:
        """Returns the generated IPv4 address."""
        return self.address
    
    def __eq__(self, value) -> bool:
        """Checks equality with another IPv4 instance."""
        if not isinstance(value, IPv4):
            return NotImplemented
        return self.address == value.address
    
class Network:
    request_monitoring_time_window = 60.0  # seconds
    request_monitoring_threshold = 10  # requests per minute

    class Request:
        def __init__(self, ip: str, timestamp: float):
            self.info = {
                "ip": ip,
                "timestamp": timestamp
            }

        @property
        def ip(self) -> str:
            return self.info["ip"]
        
        @property
        def timestamp(self) -> float:
            return self.info["timestamp"]   
        
        def within_time_window(self, global_time: float) -> bool:
            return 0 <= abs((global_time - self.timestamp) / Network.request_monitoring_time_window) <= 1
        

    def __init__(self, size: int = 10):
        """Initializes a network with a specified size."""
        self.init_time = time.perf_counter()
        self.size = size
        self.ips = [IPv4() for _ in range(self.size)]
        self.request_log = {}

    def __repr__(self) -> str:
        """Returns a string representation of the network."""
        # Well parsed representation of the network
        _formated_data = f"\nNetwork(size={self.size})\n" 
        _formated_data += f"Running for {(time.perf_counter() - self.init_time):.2f} seconds\n"
        _formated_data += "Log History:\n"
        for ip, timestamps in self.request_log.items():
            timestamps_copy = timestamps.copy()
            for i in range(len(timestamps_copy)):
                timestamps_copy[i] = timestamps_copy[i] - self.init_time
                timestamps_copy[i] = round(timestamps_copy[i], 2)  # Round to 2 decimal places

            # For each ip show number of requests
            _formated_data += f"  {ip}: {len(timestamps_copy)} requests at {timestamps_copy}\n"
        return _formated_data
    
    def is_suspicious(self, ip: str) -> bool:
        """Checks if the IP address has made too many requests in a short time."""
        if ip not in self.request_log:
            return False
        
        timestamps = self.request_log[ip]
        current_time = time.perf_counter()
        
        # Filter timestamps within the monitoring time window
        filtered_timestamps = []
        for i in range(len(timestamps)):
            _temp = current_time - timestamps[i]
            if _temp <= self.request_monitoring_time_window:
                filtered_timestamps.append(timestamps[i])
        
        # Check if the number of recent requests exceeds a threshold
        return len(filtered_timestamps) > self.request_monitoring_threshold

    def make_request(self) -> None:
        """Simulates a request from a random IP address."""
        _time = time.perf_counter()
        _ip = secrets.choice(self.ips)
        _request = Network.Request(_ip(), _time)

        if _request.ip not in self.request_log:
            self.request_log[_request.ip] = []
        self.request_log[_request.ip].append(_request.timestamp)
        
        if self.is_suspicious(_request.ip):
            print(self)

            print(f"Suspicious activity detected from IP: {_request.ip} at {(_time - self.init_time):.2f} seconds")
            # try catch exit-with-keyboard otherwise upon any key press continue upon input
            try:
                # Clear the log for the suspicious IP    
                self.request_log[_request.ip] = []
                print(f"Cleared log for IP: {_request.ip}")
                print(f"(NotImplemented) Block IP: {_request.ip}")
                input("Press Enter to continue or Ctrl+C to exit...")
            except KeyboardInterrupt:
                print("Exiting due to keyboard interrupt.")
                exit(0)
             
        
# Main execution
net = Network(size=5)
runs = 100
for _run in range(runs):
    randomness = 5
    random_seconds = secrets.randbelow(10 ** randomness + 1)  # Random seconds between 0 and 10^randomness
    random_seconds /= 10 ** randomness  # Random seconds between 0 and 1
    random_seconds += 0.1  # Ensure at least
    time.sleep(random_seconds)  # Simulate a delay before the next request
    net.make_request()