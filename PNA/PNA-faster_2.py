from datetime import datetime
from typing import List
import psutil
import threading
import time
import os


class SystemMonitor:
    """Monitor system resources in real-time during computation."""

    def __init__(self, interval: float = 0.5):
        self.interval = interval
        self.monitoring = False
        self.monitor_thread = None
        self.process = psutil.Process(os.getpid())
        self.max_memory_mb = 0
        self.max_cpu_percent = 0
        self.memory_readings = []
        self.cpu_readings = []

    def start_monitoring(self):
        """Start monitoring system resources."""
        self.monitoring = True
        self.max_memory_mb = 0
        self.max_cpu_percent = 0
        self.memory_readings = []
        self.cpu_readings = []
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("🔍 System monitoring started...")

    def stop_monitoring(self):
        """Stop monitoring system resources."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("⏹️  System monitoring stopped.\n")

    def _monitor_loop(self):
        """Main monitoring loop running in separate thread."""
        while self.monitoring:
            try:
                # Get memory usage in MB
                memory_info = self.process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024

                # Get CPU usage percentage
                cpu_percent = self.process.cpu_percent()

                # Update maximums
                self.max_memory_mb = max(self.max_memory_mb, memory_mb)
                self.max_cpu_percent = max(self.max_cpu_percent, cpu_percent)

                # Store readings for average calculation
                self.memory_readings.append(memory_mb)
                self.cpu_readings.append(cpu_percent)

                # Print real-time stats (overwrite previous line)
                print(f"\r📊 Memory: {memory_mb:.1f} MB | CPU: {cpu_percent:.1f}% | "
                      f"Peak Memory: {self.max_memory_mb:.1f} MB | Peak CPU: {self.max_cpu_percent:.1f}%",
                      end="", flush=True)

                time.sleep(self.interval)

            except Exception as e:
                print(f"\nMonitoring error: {e}")
                break

    def get_stats(self):
        """Get monitoring statistics."""
        avg_memory = sum(self.memory_readings) / len(self.memory_readings) if self.memory_readings else 0
        avg_cpu = sum(self.cpu_readings) / len(self.cpu_readings) if self.cpu_readings else 0

        return {
            'max_memory_mb': self.max_memory_mb,
            'max_cpu_percent': self.max_cpu_percent,
            'avg_memory_mb': avg_memory,
            'avg_cpu_percent': avg_cpu,
            'readings_count': len(self.memory_readings)
        }


def generate_primes(limit: int, monitor: SystemMonitor = None) -> List[int]:
    """Generate a list of prime numbers up to a given limit using an optimized Sieve of Eratosthenes."""
    if limit < 2:
        return []

    # Initialize a list to track prime status, only for odd numbers
    primes = [True] * ((limit // 2) + 1)
    primes[0] = False  # 1 is not a prime number

    # Handle the number 2 separately
    prime_list = [2]

    # Iterate over odd numbers only
    for i in range(3, limit + 1, 2):
        if primes[i // 2]:
            prime_list.append(i)
            for j in range(i * i, limit + 1, 2 * i):
                primes[j // 2] = False

    return prime_list


def display_time_taken(key: str, start: datetime, stop: datetime) -> None:
    """Print the time duration for a specific process."""
    duration = stop - start
    print(f"{key} started at: {start}")
    print(f"{key} ended at: {stop}")
    print(f"{key} duration: {duration}")


def display_system_stats(stats: dict, phase_name: str) -> None:
    """Display system resource statistics."""
    print(f"\n📈 {phase_name} Resource Usage:")
    print(f"   Peak Memory: {stats['max_memory_mb']:.1f} MB")
    print(f"   Average Memory: {stats['avg_memory_mb']:.1f} MB")
    print(f"   Peak CPU: {stats['max_cpu_percent']:.1f}%")
    print(f"   Average CPU: {stats['avg_cpu_percent']:.1f}%")
    print(f"   Monitoring samples: {stats['readings_count']}")


def get_system_info():
    """Display initial system information."""
    print("💻 System Information:")
    print(f"   CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")

    memory = psutil.virtual_memory()
    print(f"   Total RAM: {memory.total / 1024 / 1024 / 1024:.1f} GB")
    print(f"   Available RAM: {memory.available / 1024 / 1024 / 1024:.1f} GB")
    print(f"   RAM Usage: {memory.percent}%")

    print(f"   Python Process PID: {os.getpid()}\n")


def main():
    # Display system information
    get_system_info()

    # Set limit value directly (no user interaction)
    limit = 1000000000  # Change this value as needed

    # Validate the limit
    if limit < 2:
        print("The range must be at least 2.")
        return

    # Format Range Value
    formatted_limit = f"{limit:,}"
    print(f"🎯 Prime number range: {formatted_limit}")

    # Initialize system monitor
    monitor = SystemMonitor(interval=0.1)  # Monitor every 100ms

    # Start Overall Timing
    overall_start = datetime.now()
    monitor.start_monitoring()

    try:
        # Step 1: Prime Number Calculation
        print("\n🔢 Starting prime number generation...")
        step_start = datetime.now()
        primes = generate_primes(limit, monitor)
        prime_count = len(primes)
        step_end = datetime.now()

        print()  # New line after monitoring output
        display_time_taken("Prime number generation", step_start, step_end)

        # Get stats for prime generation
        prime_gen_stats = monitor.get_stats()
        display_system_stats(prime_gen_stats, "Prime Generation")

        # Step 2: Highest Prime Calculation
        print("\n🔍 Determining highest prime...")
        step_start = datetime.now()
        highest_prime = primes[-1] if primes else None
        step_end = datetime.now()
        display_time_taken("Highest prime determination", step_start, step_end)

        # Print Results
        print(f"\n✅ Results:")
        print(f"   Total primes in the range 2 to {formatted_limit}: {prime_count:,}")
        if highest_prime:
            print(f"   The highest prime in the range is: {highest_prime:,}")
        else:
            print("   No primes found in this range.")

    finally:
        # Stop monitoring and show overall stats
        monitor.stop_monitoring()
        overall_end = datetime.now()

        # Overall Timing and Stats
        display_time_taken("Overall computation", overall_start, overall_end)

        # Final system stats
        final_stats = monitor.get_stats()
        display_system_stats(final_stats, "Overall")

        # Memory efficiency info
        if prime_count > 0:
            memory_per_prime = final_stats['max_memory_mb'] / prime_count * 1024  # KB per prime
            print(f"\n📊 Efficiency Metrics:")
            print(f"   Memory per prime: {memory_per_prime:.3f} KB")
            print(f"   Primes per second: {prime_count / (overall_end - overall_start).total_seconds():.0f}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")