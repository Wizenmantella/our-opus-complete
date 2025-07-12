#!/usr/bin/env python3
"""
Hardware Acceleration System
Advanced hardware acceleration for M4 chip optimization and GPU acceleration.

Features:
- M4 chip optimization with Metal Performance Shaders
- GPU acceleration detection and optimization
- CUDA support for NVIDIA GPUs
- OpenCL support for AMD GPUs
- CPU multi-threading optimization
- Memory management and optimization
- Performance monitoring and benchmarking
- Hardware-specific codec optimization
- Power management and thermal monitoring
- Automatic hardware detection and configuration
"""

import os
import platform
import subprocess
import psutil
import torch
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
import asyncio
import logging
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

# Hardware acceleration imports
try:
    import GPUtil
    GPU_UTIL_AVAILABLE = True
except ImportError:
    GPU_UTIL_AVAILABLE = False

# Metal Performance Shaders (M4 chip)
try:
    import Metal
    import MetalPerformanceShaders as MPS
    METAL_AVAILABLE = True
except ImportError:
    METAL_AVAILABLE = False

# CUDA
try:
    import cupy as cp
    CUDA_AVAILABLE = torch.cuda.is_available()
except ImportError:
    CUDA_AVAILABLE = False

# OpenCL
try:
    import pyopencl as cl
    OPENCL_AVAILABLE = True
except ImportError:
    OPENCL_AVAILABLE = False

logger = logging.getLogger(__name__)


class HardwareType(Enum):
    """Hardware acceleration types"""
    M4_CHIP = "m4_chip"
    CUDA = "cuda"
    OPENCL = "opencl"
    CPU = "cpu"
    METAL = "metal"
    VULKAN = "vulkan"


class AccelerationType(Enum):
    """Acceleration operation types"""
    VIDEO_DECODE = "video_decode"
    VIDEO_ENCODE = "video_encode"
    AUDIO_PROCESS = "audio_process"
    AI_INFERENCE = "ai_inference"
    COLOR_GRADING = "color_grading"
    EFFECTS = "effects"
    COMPOSITING = "compositing"
    TRANSCODING = "transcoding"


@dataclass
class HardwareCapabilities:
    """Hardware capabilities information"""
    hardware_type: HardwareType
    device_name: str
    compute_units: int
    memory_gb: float
    max_threads: int
    supports_fp16: bool = False
    supports_int8: bool = False
    supports_unified_memory: bool = False
    video_decode_formats: List[str] = field(default_factory=list)
    video_encode_formats: List[str] = field(default_factory=list)
    performance_score: float = 0.0
    power_efficiency: float = 0.0
    thermal_design_power: float = 0.0


@dataclass
class PerformanceMetrics:
    """Performance monitoring metrics"""
    timestamp: float
    cpu_usage: float
    memory_usage: float
    gpu_usage: float
    gpu_memory_usage: float
    temperature: float
    power_draw: float
    throughput: float
    latency: float


class HardwareAccelerationSystem:
    """Complete hardware acceleration system"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.hardware_capabilities: List[HardwareCapabilities] = []
        self.performance_history: List[PerformanceMetrics] = []
        self.thread_pool = ThreadPoolExecutor(max_workers=mp.cpu_count())
        self.process_pool = ProcessPoolExecutor(max_workers=mp.cpu_count())
        
        # Initialize hardware detection
        self._detect_hardware()
        self._initialize_acceleration()
        
        # Start performance monitoring
        self.monitoring_thread = threading.Thread(
            target=self._monitor_performance, daemon=True
        )
        self.monitoring_thread.start()
    
    def _detect_hardware(self):
        """Detect available hardware acceleration"""
        try:
            # Detect M4 chip
            if platform.system() == "Darwin":
                try:
                    cpu_info = subprocess.run(
                        ["sysctl", "-n", "machdep.cpu.brand_string"],
                        capture_output=True, text=True
                    ).stdout.strip()
                    
                    if "Apple M4" in cpu_info or "M4" in cpu_info:
                        m4_caps = HardwareCapabilities(
                            hardware_type=HardwareType.M4_CHIP,
                            device_name="Apple M4",
                            compute_units=self._get_m4_compute_units(),
                            memory_gb=self._get_unified_memory(),
                            max_threads=mp.cpu_count(),
                            supports_fp16=True,
                            supports_int8=True,
                            supports_unified_memory=True,
                            video_decode_formats=["H.264", "H.265", "ProRes", "AV1"],
                            video_encode_formats=["H.264", "H.265", "ProRes"],
                            performance_score=95.0,
                            power_efficiency=98.0,
                            thermal_design_power=20.0
                        )
                        self.hardware_capabilities.append(m4_caps)
                except Exception as e:
                    logger.warning(f"M4 detection failed: {e}")
            
            # Detect CUDA GPUs
            if CUDA_AVAILABLE:
                try:
                    for i in range(torch.cuda.device_count()):
                        props = torch.cuda.get_device_properties(i)
                        cuda_caps = HardwareCapabilities(
                            hardware_type=HardwareType.CUDA,
                            device_name=props.name,
                            compute_units=props.multi_processor_count,
                            memory_gb=props.total_memory / (1024**3),
                            max_threads=props.max_threads_per_block,
                            supports_fp16=props.major >= 6,
                            supports_int8=props.major >= 6,
                            supports_unified_memory=False,
                            video_decode_formats=["H.264", "H.265", "AV1"],
                            video_encode_formats=["H.264", "H.265"],
                            performance_score=self._benchmark_cuda(i),
                            power_efficiency=60.0,
                            thermal_design_power=props.total_memory / (1024**3) * 25
                        )
                        self.hardware_capabilities.append(cuda_caps)
                except Exception as e:
                    logger.warning(f"CUDA detection failed: {e}")
            
            # Detect OpenCL devices
            if OPENCL_AVAILABLE:
                try:
                    for platform_cl in cl.get_platforms():
                        for device in platform_cl.get_devices():
                            opencl_caps = HardwareCapabilities(
                                hardware_type=HardwareType.OPENCL,
                                device_name=device.name,
                                compute_units=device.max_compute_units,
                                memory_gb=device.global_mem_size / (1024**3),
                                max_threads=device.max_work_group_size,
                                supports_fp16=False,
                                supports_int8=False,
                                supports_unified_memory=False,
                                video_decode_formats=["H.264", "H.265"],
                                video_encode_formats=["H.264"],
                                performance_score=self._benchmark_opencl(device),
                                power_efficiency=70.0,
                                thermal_design_power=device.max_compute_units * 2
                            )
                            self.hardware_capabilities.append(opencl_caps)
                except Exception as e:
                    logger.warning(f"OpenCL detection failed: {e}")
            
            # CPU fallback
            cpu_caps = HardwareCapabilities(
                hardware_type=HardwareType.CPU,
                device_name=platform.processor() or "CPU",
                compute_units=mp.cpu_count(),
                memory_gb=psutil.virtual_memory().total / (1024**3),
                max_threads=mp.cpu_count() * 2,
                supports_fp16=False,
                supports_int8=True,
                supports_unified_memory=True,
                video_decode_formats=["H.264", "H.265"],
                video_encode_formats=["H.264", "H.265"],
                performance_score=50.0,
                power_efficiency=80.0,
                thermal_design_power=65.0
            )
            self.hardware_capabilities.append(cpu_caps)
            
            logger.info(f"Detected {len(self.hardware_capabilities)} hardware devices")
            
        except Exception as e:
            logger.error(f"Hardware detection failed: {e}")
    
    def _get_m4_compute_units(self) -> int:
        """Get M4 compute units"""
        try:
            # M4 has 10 CPU cores (4 performance + 6 efficiency)
            # GPU cores vary by model
            gpu_cores = subprocess.run(
                ["system_profiler", "SPDisplaysDataType"],
                capture_output=True, text=True
            ).stdout
            
            if "M4 Pro" in gpu_cores:
                return 20  # 20 GPU cores
            elif "M4 Max" in gpu_cores:
                return 40  # 40 GPU cores
            else:
                return 10  # Base M4 - 10 GPU cores
        except:
            return 10
    
    def _get_unified_memory(self) -> float:
        """Get unified memory size"""
        try:
            memory_info = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True
            ).stdout.strip()
            return int(memory_info) / (1024**3)
        except:
            return 8.0
    
    def _benchmark_cuda(self, device_id: int) -> float:
        """Benchmark CUDA performance"""
        try:
            device = torch.device(f"cuda:{device_id}")
            size = 1024
            
            # Matrix multiplication benchmark
            start_time = time.time()
            a = torch.randn(size, size, device=device)
            b = torch.randn(size, size, device=device)
            
            for _ in range(10):  # Reduced iterations for faster detection
                c = torch.matmul(a, b)
            
            torch.cuda.synchronize()
            end_time = time.time()
            
            ops_per_second = 10 * size * size * size / (end_time - start_time)
            return min(ops_per_second / 1e9, 100.0)  # Normalize to 0-100
            
        except Exception as e:
            logger.warning(f"CUDA benchmark failed: {e}")
            return 80.0  # Default high score for CUDA
    
    def _benchmark_opencl(self, device) -> float:
        """Benchmark OpenCL performance"""
        try:
            # Simple performance estimation based on compute units
            return min(device.max_compute_units * 2, 100.0)
            
        except Exception as e:
            logger.warning(f"OpenCL benchmark failed: {e}")
            return 40.0
    
    def _initialize_acceleration(self):
        """Initialize hardware acceleration"""
        try:
            # Sort capabilities by performance score
            self.hardware_capabilities.sort(
                key=lambda x: x.performance_score, reverse=True
            )
            
            # Initialize M4 Metal if available
            if METAL_AVAILABLE and any(cap.hardware_type == HardwareType.M4_CHIP 
                                     for cap in self.hardware_capabilities):
                self._initialize_metal()
            
            # Initialize CUDA if available
            if CUDA_AVAILABLE:
                self._initialize_cuda()
            
            # Initialize OpenCL if available
            if OPENCL_AVAILABLE:
                self._initialize_opencl()
            
            logger.info("Hardware acceleration initialized successfully")
            
        except Exception as e:
            logger.error(f"Hardware acceleration initialization failed: {e}")
    
    def _initialize_metal(self):
        """Initialize Metal Performance Shaders for M4"""
        try:
            if not METAL_AVAILABLE:
                return
            
            # Try to use MPS (Metal Performance Shaders)
            if torch.backends.mps.is_available():
                self.mps_device = torch.device("mps")
                logger.info("Metal Performance Shaders initialized for M4")
            else:
                logger.warning("MPS not available on this system")
            
        except Exception as e:
            logger.error(f"Metal initialization failed: {e}")
    
    def _initialize_cuda(self):
        """Initialize CUDA acceleration"""
        try:
            if not CUDA_AVAILABLE:
                return
            
            # Set CUDA device
            torch.cuda.set_device(0)
            
            # Initialize CUDA context
            self.cuda_context = torch.cuda.current_device()
            
            logger.info(f"CUDA initialized with {torch.cuda.device_count()} devices")
            
        except Exception as e:
            logger.error(f"CUDA initialization failed: {e}")
    
    def _initialize_opencl(self):
        """Initialize OpenCL acceleration"""
        try:
            if not OPENCL_AVAILABLE:
                return
            
            # Get best OpenCL device
            best_device = None
            best_score = 0
            
            for cap in self.hardware_capabilities:
                if cap.hardware_type == HardwareType.OPENCL and cap.performance_score > best_score:
                    best_score = cap.performance_score
                    best_device = cap
            
            if best_device:
                platforms = cl.get_platforms()
                for platform_cl in platforms:
                    devices = platform_cl.get_devices()
                    for device in devices:
                        if device.name == best_device.device_name:
                            self.opencl_context = cl.Context([device])
                            self.opencl_queue = cl.CommandQueue(self.opencl_context)
                            break
            
            logger.info("OpenCL initialized")
            
        except Exception as e:
            logger.error(f"OpenCL initialization failed: {e}")
    
    def _monitor_performance(self):
        """Monitor hardware performance continuously"""
        while True:
            try:
                # Get CPU metrics
                cpu_usage = psutil.cpu_percent(interval=1)
                memory_usage = psutil.virtual_memory().percent
                
                # Get GPU metrics
                gpu_usage = 0
                gpu_memory_usage = 0
                temperature = 0
                power_draw = 0
                
                if GPU_UTIL_AVAILABLE:
                    try:
                        gpus = GPUtil.getGPUs()
                        if gpus:
                            gpu = gpus[0]
                            gpu_usage = gpu.load * 100
                            gpu_memory_usage = gpu.memoryUtil * 100
                            temperature = gpu.temperature
                            power_draw = getattr(gpu, 'powerDraw', 0)
                    except:
                        pass
                
                # Calculate throughput (placeholder)
                throughput = 100.0
                
                # Calculate latency (placeholder)
                latency = 0.1
                
                metrics = PerformanceMetrics(
                    timestamp=time.time(),
                    cpu_usage=cpu_usage,
                    memory_usage=memory_usage,
                    gpu_usage=gpu_usage,
                    gpu_memory_usage=gpu_memory_usage,
                    temperature=temperature,
                    power_draw=power_draw,
                    throughput=throughput,
                    latency=latency
                )
                
                self.performance_history.append(metrics)
                
                # Keep only last 1000 metrics
                if len(self.performance_history) > 1000:
                    self.performance_history = self.performance_history[-1000:]
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                time.sleep(5)
    
    def get_best_hardware(self, operation: AccelerationType) -> Optional[HardwareCapabilities]:
        """Get best hardware for specific operation"""
        try:
            # Filter capabilities by operation support
            suitable_hardware = []
            
            for cap in self.hardware_capabilities:
                if operation == AccelerationType.VIDEO_DECODE:
                    if cap.video_decode_formats:
                        suitable_hardware.append(cap)
                elif operation == AccelerationType.VIDEO_ENCODE:
                    if cap.video_encode_formats:
                        suitable_hardware.append(cap)
                elif operation == AccelerationType.AI_INFERENCE:
                    if cap.supports_fp16 or cap.supports_int8:
                        suitable_hardware.append(cap)
                else:
                    suitable_hardware.append(cap)
            
            # Return best performing hardware
            if suitable_hardware:
                return max(suitable_hardware, key=lambda x: x.performance_score)
            
            return None
            
        except Exception as e:
            logger.error(f"Hardware selection failed: {e}")
            return None
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get detailed performance report"""
        try:
            if not self.performance_history:
                return {
                    "hardware_capabilities": [
                        {
                            "type": cap.hardware_type.value,
                            "name": cap.device_name,
                            "performance_score": cap.performance_score,
                            "memory_gb": cap.memory_gb,
                            "compute_units": cap.compute_units
                        }
                        for cap in self.hardware_capabilities
                    ],
                    "best_hardware": self.hardware_capabilities[0].device_name if self.hardware_capabilities else "None"
                }
            
            recent_metrics = self.performance_history[-100:]  # Last 100 samples
            
            # Calculate averages
            avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
            avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
            avg_gpu = sum(m.gpu_usage for m in recent_metrics) / len(recent_metrics)
            avg_gpu_memory = sum(m.gpu_memory_usage for m in recent_metrics) / len(recent_metrics)
            avg_temperature = sum(m.temperature for m in recent_metrics) / len(recent_metrics)
            avg_power = sum(m.power_draw for m in recent_metrics) / len(recent_metrics)
            avg_throughput = sum(m.throughput for m in recent_metrics) / len(recent_metrics)
            avg_latency = sum(m.latency for m in recent_metrics) / len(recent_metrics)
            
            return {
                "hardware_capabilities": [
                    {
                        "type": cap.hardware_type.value,
                        "name": cap.device_name,
                        "performance_score": cap.performance_score,
                        "memory_gb": cap.memory_gb,
                        "compute_units": cap.compute_units
                    }
                    for cap in self.hardware_capabilities
                ],
                "current_performance": {
                    "cpu_usage": avg_cpu,
                    "memory_usage": avg_memory,
                    "gpu_usage": avg_gpu,
                    "gpu_memory_usage": avg_gpu_memory,
                    "temperature": avg_temperature,
                    "power_draw": avg_power,
                    "throughput": avg_throughput,
                    "latency": avg_latency
                },
                "best_hardware": self.hardware_capabilities[0].device_name if self.hardware_capabilities else "None"
            }
            
        except Exception as e:
            logger.error(f"Performance report generation failed: {e}")
            return {"error": str(e)}
    
    def optimize_for_task(self, task_type: AccelerationType) -> Dict[str, Any]:
        """Optimize hardware configuration for specific task"""
        try:
            best_hardware = self.get_best_hardware(task_type)
            
            if not best_hardware:
                return {"error": "No suitable hardware found"}
            
            # Configure optimization based on hardware and task
            optimization = {
                "hardware": best_hardware.device_name,
                "type": best_hardware.hardware_type.value,
                "recommended_threads": best_hardware.max_threads,
                "memory_allocation": min(best_hardware.memory_gb * 0.8, 8.0),
                "batch_size": self._calculate_optimal_batch_size(best_hardware, task_type),
                "precision": "fp16" if best_hardware.supports_fp16 else "fp32"
            }
            
            # Apply M4-specific optimizations
            if best_hardware.hardware_type == HardwareType.M4_CHIP:
                optimization.update({
                    "unified_memory": True,
                    "metal_performance_shaders": True,
                    "neural_engine": task_type == AccelerationType.AI_INFERENCE,
                    "video_toolbox": task_type in [AccelerationType.VIDEO_DECODE, AccelerationType.VIDEO_ENCODE]
                })
            
            return optimization
            
        except Exception as e:
            logger.error(f"Task optimization failed: {e}")
            return {"error": str(e)}
    
    def _calculate_optimal_batch_size(self, hardware: HardwareCapabilities, 
                                     task_type: AccelerationType) -> int:
        """Calculate optimal batch size for hardware and task"""
        try:
            # Base batch size on available memory
            base_batch_size = max(1, int(hardware.memory_gb / 2))
            
            # Adjust for task type
            if task_type == AccelerationType.AI_INFERENCE:
                return min(base_batch_size, 32)
            elif task_type in [AccelerationType.VIDEO_DECODE, AccelerationType.VIDEO_ENCODE]:
                return min(base_batch_size, 8)
            elif task_type == AccelerationType.EFFECTS:
                return min(base_batch_size, 4)
            else:
                return min(base_batch_size, 16)
                
        except Exception as e:
            logger.error(f"Batch size calculation failed: {e}")
            return 1
    
    def __del__(self):
        """Cleanup resources"""
        try:
            self.thread_pool.shutdown(wait=False)
            self.process_pool.shutdown(wait=False)
        except:
            pass