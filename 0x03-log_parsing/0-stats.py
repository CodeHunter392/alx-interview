#!/usr/bin/python3
import sys
import signal
import re

total_file_size = 0
status_code_counts = {
    "200": 0,
    "301": 0,
    "400": 0,
    "401": 0,
    "403": 0,
    "404": 0,
    "405": 0,
    "500": 0
}

line_count = 0

# Regex pattern to match the log line format
log_pattern = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - \[.+\] "GET /projects/260 HTTP/1\.1" (?P<status>\d{3}) (?P<size>\d+)'
)

def print_stats():
    """Prints the accumulated statistics."""
    print(f"File size: {total_file_size}")
    for status_code in sorted(status_code_counts.keys()):
        if status_code_counts[status_code] > 0:
            print(f"{status_code}: {status_code_counts[status_code]}")

def signal_handler(sig, frame):
    """Handles the keyboard interruption signal (CTRL + C)."""
    print_stats()
    sys.exit(0)

# Set up the signal handler for keyboard interruption
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        match = log_pattern.match(line)
        if match:
            status_code = match.group("status")
            file_size = int(match.group("size"))
            total_file_size += file_size
            if status_code in status_code_counts:
                status_code_counts[status_code] += 1
        line_count += 1

        if line_count % 10 == 0:
            print_stats()
except KeyboardInterrupt:
    print_stats()
    raise

