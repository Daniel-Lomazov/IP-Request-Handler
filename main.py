from __future__ import annotations
import secrets, ipaddress
from typing import Any
import random
import time


class IPv4:
    @staticmethod
    def generate() -> str:
        """Generates a random valid IPv4 address."""
        _ip = secrets.randbits(32)
        _ip = ipaddress.IPv4Address(_ip)
        _ip = str(_ip)
        return _ip

    @staticmethod
    def validate(_ip: str) -> str | None:
        """Validates if the given string is a valid IPv4 address."""
        try:
            _ = ipaddress.IPv4Address(_ip)
            return _ip
        except ipaddress.AddressValueError:
            return None
    
    def invalid(self) -> bool:
        """Returns True if the IPv4 address is invalid."""
        return IPv4.validate(self.address) is None
    
    def __init__(self, address: str):
        """Initializes the IPv4 generator."""
        self.address = address

    def __call__(self) -> str:
        """Returns the generated IPv4 address."""
        return self.address
    
    def __repr__(self) -> str:
        return f"IPv4('{self()}')"
    
    def __hash__(self) -> int:
        return hash(self.address)

    def __eq__(self, other: object) -> bool:  # type: ignore[override]
        """Value equality based on the textual IPv4 address.

        Accepts any object (object signature) to remain compatible with the
        base `object.__eq__` contract. Returns False for non-IPv4 instances.
        """
        if isinstance(other, IPv4):
            return self.address == other.address
        return False


class Device:
    def __init__(self, ip_address: IPv4):
        """Initializes a device."""
        self.ip_address = ip_address

    def reset(self, new_ip_address: IPv4) -> None:
        """Resets the device."""
        self.ip_address = new_ip_address

    def __repr__(self) -> str:
        return f"Device('{self.ip_address()}')"

    def __hash__(self) -> int:
        """Returns a hash of the device based on its IP address."""
        return hash(self.ip_address)
    
    def make_request(self, network: Network) -> None:
        """Simulates a request from the device."""
        _timestamp = time.perf_counter()
        network.process_request(self, _timestamp)

class Network:
    request_monitoring_time_window = 10.0  # seconds
    request_rate_limit = 2.0  # requests per second
    request_monitoring_threshold = request_rate_limit * request_monitoring_time_window

    def __init__(self):
        """Initializes a network with a specified size."""
        self._init_time = time.perf_counter()
        self.request_log: dict[Device, list[float] | str] = {}
    
    @property
    def init_time(self):
        return self._init_time
    
    def list_devices(self):
        return list(self.request_log.keys())

    @property
    def size(self) -> int:
        return len(self.list_devices())

    def __repr__(self) -> str:
        """Returns a string representation of the network."""
        # Well parsed representation of the network
        _formated_data = f"\nNetwork(size={self.size})\n" 
        _formated_data += f"Running for {(time.perf_counter() - self.init_time):.2f} seconds\n"
        _formated_data += "Log History:\n"
        for device, timestamps in self.request_log.items():
            if timestamps == "BLOCKED":
                _formated_data += f"  {device}: BLOCKED\n"
                continue
            if not isinstance(timestamps, list):  # Defensive: unknown state
                _formated_data += f"  {device}: <unexpected-state>\n"
                continue

            timestamps_copy = list(timestamps)
            for i in range(len(timestamps_copy)):
                timestamps_copy[i] = timestamps_copy[i] - self.init_time
                timestamps_copy[i] = round(timestamps_copy[i], 2)  # Round to 2 decimal places

            # For each device show number of requests
            _formated_data += f"  {device}: {len(timestamps_copy)}\n"

        return _formated_data
    
    def is_suspicious(self, device: Device, timestamp: float) -> bool:
        """Checks if the device has made too many requests in a short time."""
        if device not in self.request_log:
            return False

        timestamps_union = self.request_log[device]
        if isinstance(timestamps_union, str):
            if timestamps_union == "BLOCKED":
                return True
            raise NotImplementedError("Unexpected state in request log.")
        timestamps: list[float] = timestamps_union  # Narrow type
        
        # Filter timestamps within the monitoring time window
        filtered_timestamps = []
        for i in range(len(timestamps)):
            _temp = timestamp - timestamps[i]
            if _temp <= self.request_monitoring_time_window:
                filtered_timestamps.append(timestamps[i])

        filtered_timestamps.append(timestamp)

        # Check if the number of recent requests exceeds a threshold
        return len(filtered_timestamps) > self.request_monitoring_threshold

    def block(self, device: Device) -> None:
        """Blocks a device from making requests."""
        # print(f"Blocking {device}...\n")
        self.request_log[device] = "BLOCKED"
        # print(f"Blocked {device}.\n")

    def unblock(self, device: Device) -> None:
        """Unblocks a device, allowing it to make requests again."""
        self.request_log[device] = []

    def is_blocked(self, device: Device) -> bool:
        """Checks if a device is blocked."""
        return self.request_log.get(device) == "BLOCKED"

    def process_request(self, device: Device, timestamp: float) -> None:
        """Simulates a request from a device."""
        print(f"Processing request from {device} at {timestamp - self.init_time:.2f} seconds.")
        
        if self.is_blocked(device):
            print(f"Blocked request from {device} at {timestamp - self.init_time:.2f} seconds.")
            return

        if self.is_suspicious(device, timestamp):
            print(f"Suspicious activity detected from {device} at {timestamp - self.init_time:.2f} seconds.")
            print(self)
            _ = input("Press Enter to continue...\n")
            self.block(device)
            return
        
        if device not in self.request_log:
            self.request_log[device] = []

        if device in self.request_log:
            entry = self.request_log[device]
            if isinstance(entry, list):
                entry.append(timestamp)
            else:
                raise ValueError(f"Unexpected state for device {device}. Request log should be a list.")
        # print(f"Request from {device} successfully processed at {timestamp - self.init_time:.2f} seconds.\n")

             
# Main execution
net = Network()
max_size = 1
devices = [Device(IPv4(IPv4.generate())) for _ in range(max_size)]
runs = 100

for i in range(runs):
    random_device = secrets.choice(devices)
    random_device.make_request(net)
    random_number_of_seconds = abs(random.normalvariate() * 0.2 + 0.1)
    time.sleep(random_number_of_seconds)

# TODOs
# - Refactor into a small CLI tool with argparse
# - Integrate protocol-based routing (collect handlers, registry)
# - Add tests for demo flows
# - Replace sleep-based simulation with event-driven testing