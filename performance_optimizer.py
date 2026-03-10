import time
import threading
import functools
import hashlib
import json
import streamlit as st
from collections import OrderedDict

class PerformanceOptimizer:
    """
    Class to optimize the performance of the TalentScout chatbot application.
    Provides caching, request batching, and performance monitoring.
    """
    
    def __init__(self, cache_size=100):
        """
        Initialize the performance optimizer
        
        Args:
            cache_size (int): Maximum number of entries to keep in the cache
        """
        # Initialize cache for API responses
        self.cache = OrderedDict()
        self.cache_size = cache_size
        self.cache_hits = 0
        self.cache_misses = 0
        
        # tracking performance
        self.response_times = []
        self.max_response_times = 20  
        
        self.batch_queue = []
        self.batch_lock = threading.Lock()
        
        # Initialize stats in session state if they don't exist
        if 'performance_stats' not in st.session_state:
            st.session_state.performance_stats = {
                'api_calls': 0,
                'avg_response_time': 0,
                'cache_hits': 0, 
                'cache_misses': 0
            }
    
    def cache_api_response(self, func):
        """
        Decorator for caching API responses based on input parameters
        
        Args:
            func: Function to decorate
            
        Returns:
            wrapper: Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_args = args[1:]  
            key_parts = [str(arg) for arg in cache_args]
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}:{v}")
            
            cache_key = hashlib.md5(str(key_parts).encode()).hexdigest()
            
            # Check if result is in cache
            if cache_key in self.cache:
                self.cache_hits += 1
                st.session_state.performance_stats['cache_hits'] += 1
                
                # Move the entry to the end (most recently used)
                self.cache.move_to_end(cache_key)
                
                return self.cache[cache_key]
            
            # Not in cache, call the function
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            # Record performance statistics
            self.record_response_time(elapsed_time)
            self.cache_misses += 1
            st.session_state.performance_stats['cache_misses'] += 1
            st.session_state.performance_stats['api_calls'] += 1
            
            self.cache[cache_key] = result
            self.cache.move_to_end(cache_key)
            
            # Remove oldest entry if cache is full
            if len(self.cache) > self.cache_size:
                self.cache.popitem(last=False)
            
            return result
        
        return wrapper
    
    def record_response_time(self, elapsed_time):
        """
        Record API response time for monitoring
        
        Args:
            elapsed_time (float): Response time in seconds
        """
        self.response_times.append(elapsed_time)
        
        # Keep only the recent history
        if len(self.response_times) > self.max_response_times:
            self.response_times.pop(0)
        
        # Update average response time in session state
        if self.response_times:
            st.session_state.performance_stats['avg_response_time'] = sum(self.response_times) / len(self.response_times)
    
    def get_average_response_time(self):
        """
        Get the average response time from recorded response times
        
        Returns:
            float: Average response time in seconds
        """
        if not self.response_times:
            return 0.0
        
        return sum(self.response_times) / len(self.response_times)
    
    def preprocess_prompt(self, prompt):
        """
        Optimize prompts before sending to API
        
        Args:
            prompt (str): The original prompt
            
        Returns:
            str: The optimized prompt
        """
        # Remove redundant whitespace
        optimized = " ".join(prompt.split())
        
        max_chars = 10000
        if len(optimized) > max_chars:
            cutoff_points = [
                optimized.rfind("\n\n", 0, max_chars),
                optimized.rfind(". ", 0, max_chars),
                optimized.rfind("? ", 0, max_chars),
                optimized.rfind("! ", 0, max_chars),
                max_chars
            ]
            
            cutoff = next((p for p in cutoff_points if p > 0), max_chars)
            optimized = optimized[:cutoff+1]
        
        return optimized
    
    def batch_requests(self, requests, process_func):
        """
        Batch multiple requests together to reduce overhead
        
        Args:
            requests (list): List of request parameters
            process_func (function): Function to process batched requests
            
        Returns:
            list: Results for each request
        """
        with self.batch_lock:
            batch_id = time.time()
            for req in requests:
                self.batch_queue.append((batch_id, req))
        
        # Process the entire batch
        results = process_func(self.batch_queue)
        
        with self.batch_lock:
            self.batch_queue = []
        
        return results
    
    def display_performance_stats(self):
        """Display performance statistics in the Streamlit UI"""
        stats = st.session_state.performance_stats
        
        st.sidebar.markdown("### Performance Metrics")
        st.sidebar.text(f"API Calls: {stats['api_calls']}")
        st.sidebar.text(f"Avg Response Time: {stats['avg_response_time']:.2f}s")
        
        # Cache efficiency
        cache_total = stats['cache_hits'] + stats['cache_misses']
        if cache_total > 0:
            cache_efficiency = (stats['cache_hits'] / cache_total) * 100
            st.sidebar.text(f"Cache Efficiency: {cache_efficiency:.1f}%")
            
            hits_bar = "■" * int(cache_efficiency / 5)
            misses_bar = "□" * (20 - int(cache_efficiency / 5))
            st.sidebar.text(f"Cache Hits/Misses: {hits_bar}{misses_bar}")
        
        if self.response_times:
            st.sidebar.text("Recent Response Times (s):")

            for t in self.response_times[-5:]:
                bar = "■" * int(t * 10)
                st.sidebar.text(f"{t:.2f}s {bar}")
    
    def optimize_json_parse(self, json_str):
        """
        Safely parse JSON with fallback options
        
        Args:
            json_str (str): JSON string to parse
            
        Returns:
            dict: Parsed JSON or error dict
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            try:
                fixed_json = self._fix_json_string(json_str)
                return json.loads(fixed_json)
            except:
                return {
                    "error": "Failed to parse JSON response",
                    "original": json_str,
                    "exception": str(e)
                }
    
    def _fix_json_string(self, json_str):
        """
        Attempt to fix common JSON formatting issues
        
        Args:
            json_str (str): Potentially malformed JSON string
            
        Returns:
            str: Attempted fix of the JSON string
        """
        
        if "```json" in json_str:
            json_str = json_str.replace("```json", "")
        if "```" in json_str:
            json_str = json_str.replace("```", "")
            
        
        import re
        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1"\2":', json_str)
        
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
            
        return json_str
    
    def rate_limit(func):
        """
        Decorator to implement rate limiting for API calls
        
        Args:
            func: Function to decorate
            
        Returns:
            wrapper: Decorated function
        """
        last_call_time = {}
        min_interval = 0.1  
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            func_name = func.__name__
            
            # Check if we need to wait
            if func_name in last_call_time:
                elapsed = current_time - last_call_time[func_name]
                if elapsed < min_interval:
                    time.sleep(min_interval - elapsed)
            
            last_call_time[func_name] = time.time()
            
            
            return func(*args, **kwargs)
        
        return wrapper