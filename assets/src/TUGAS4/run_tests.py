#!/usr/bin/env python3
"""
Script to run comprehensive file server tests
This script will help you run different server configurations and stress tests
"""

import subprocess
import time
import os
import signal
import sys
import argparse
from datetime import datetime

class TestRunner:
    def __init__(self):
        self.server_process = None
        
    def start_server(self, port=46666, workers=5, use_multiprocessing=False):
        """Start the server with specified configuration"""
        cmd = [
            sys.executable, 'thread_pool.py',
            '--port', str(port),
            '--workers', str(workers)
        ]
        
        if use_multiprocessing:
            cmd.append('--multiprocessing')
        
        print(f"Starting server: {' '.join(cmd)}")
        
        try:
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(2)  # Give server time to start
            
            if self.server_process.poll() is None:
                print(f"Server started successfully (PID: {self.server_process.pid})")
                return True
            else:
                print("Server failed to start")
                return False
                
        except Exception as e:
            print(f"Error starting server: {e}")
            return False
    
    def stop_server(self):
        """Stop the running server"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("Server stopped successfully")
            except subprocess.TimeoutExpired:
                print("Server didn't stop gracefully, killing...")
                self.server_process.kill()
                self.server_process.wait()
            except Exception as e:
                print(f"Error stopping server: {e}")
        
        self.server_process = None
    
    def run_stress_test(self, server_workers, client_multiprocessing=False, output_prefix=""):
        """Run stress test with specified configuration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_prefix}stress_test_results_{timestamp}.csv"
        
        cmd = [
            sys.executable, 'file_client_stress_test.py',
            '--server-host', '172.16.16.101',
            '--server-port', '46666',
            '--server-workers'
        ] + [str(w) for w in server_workers] + [
            '--output', output_file
        ]
        
        if client_multiprocessing:
            cmd.append('--multiprocessing-client')
        
        print(f"Running stress test: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
            
            if result.returncode == 0:
                print("Stress test completed successfully")
                print(f"Results saved to: {output_file}")
                return True
            else:
                print("Stress test failed")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("Stress test timed out")
            return False
        except Exception as e:
            print(f"Error running stress test: {e}")
            return False
    
    def run_comprehensive_tests(self):
        """Run comprehensive tests with different server configurations"""
        test_configs = [
            # (server_workers, use_multiprocessing, description)
            (1, False, "threading_1worker"),
            (5, False, "threading_5workers"),
            (50, False, "threading_50workers"),
            (1, True, "multiprocessing_1worker"),
            (5, True, "multiprocessing_5workers"),
            (50, True, "multiprocessing_50workers"),
        ]
        
        print("="*80)
        print("COMPREHENSIVE FILE SERVER STRESS TEST")
        print("="*80)
        print(f"Total configurations to test: {len(test_configs)}")
        print("Each configuration will test:")
        print("- Operations: upload, download")
        print("- File sizes: 10MB, 50MB, 100MB")
        print("- Client workers: 1, 5, 50")
        print("- Total combinations per config: 18")
        print(f"- Grand total tests: {len(test_configs) * 18}")
        print("="*80)
        
        successful_configs = 0
        
        for i, (workers, use_mp, description) in enumerate(test_configs, 1):
            print(f"\n[{i}/{len(test_configs)}] Testing configuration: {description}")
            print(f"Server workers: {workers}, Multiprocessing: {use_mp}")
            print("-" * 60)
            
            # Start server with current configuration
            if self.start_server(workers=workers, use_multiprocessing=use_mp):
                # Run stress test
                server_workers_list = [workers]  # Test with current server worker count
                
                if self.run_stress_test(
                    server_workers=server_workers_list,
                    client_multiprocessing=False,  # Test with threading clients
                    output_prefix=f"{description}_"
                ):
                    successful_configs += 1
                    print(f"✓ Configuration {description} completed successfully")
                else:
                    print(f"✗ Configuration {description} failed")
                
                # Stop server
                self.stop_server()
                time.sleep(2)  # Brief pause between configurations
            else:
                print(f"✗ Failed to start server for configuration {description}")
        
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*80)
        print(f"Successful configurations: {successful_configs}/{len(test_configs)}")
        print(f"Failed configurations: {len(test_configs) - successful_configs}/{len(test_configs)}")
        
        if successful_configs == len(test_configs):
            print("🎉 All tests completed successfully!")
        else:
            print("⚠️  Some tests failed. Check the logs above for details.")
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_server()

def main():
    parser = argparse.ArgumentParser(description='File Server Test Runner')
    parser.add_argument('--mode', choices=['single', 'comprehensive'], default='comprehensive',
                       help='Test mode: single configuration or comprehensive test')
    parser.add_argument('--server-workers', type=int, default=5,
                       help='Number of server workers (single mode only)')
    parser.add_argument('--server-multiprocessing', action='store_true',
                       help='Use multiprocessing for server (single mode only)')
    parser.add_argument('--client-multiprocessing', action='store_true',
                       help='Use multiprocessing for client workers (single mode only)')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    try:
        if args.mode == 'single':
            print("Running single configuration test...")
            print(f"Server: {args.server_workers} workers, "
                  f"{'multiprocessing' if args.server_multiprocessing else 'threading'}")
            print(f"Client: {'multiprocessing' if args.client_multiprocessing else 'threading'}")
            
            if runner.start_server(
                workers=args.server_workers,
                use_multiprocessing=args.server_multiprocessing
            ):
                runner.run_stress_test(
                    server_workers=[args.server_workers],
                    client_multiprocessing=args.client_multiprocessing,
                    output_prefix="single_test_"
                )
            else:
                print("Failed to start server")
                
        else:  # comprehensive
            runner.run_comprehensive_tests()
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        runner.cleanup()

if __name__ == "__main__":
    main()