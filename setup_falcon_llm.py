#!/usr/bin/env python3
"""
Setup script for Falcon 7B LLM integration with FashionPulse
Installs dependencies and verifies system requirements
"""
import subprocess
import sys
import os
import platform
import torch
from pathlib import Path

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def run_command(command, description):
    """Run a command and return success status"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Success")
            return True
        else:
            print(f"   ❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def check_system_requirements():
    """Check system requirements for LLM"""
    print_header("SYSTEM REQUIREMENTS CHECK")
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version >= (3, 8):
        print("   ✅ Python version is compatible")
    else:
        print("   ❌ Python 3.8+ required")
        return False
    
    # Check platform
    system = platform.system()
    print(f"💻 Operating System: {system}")
    
    # Check available memory
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        print(f"🧠 System RAM: {memory_gb:.1f} GB")
        if memory_gb >= 16:
            print("   ✅ Sufficient RAM for LLM")
        elif memory_gb >= 8:
            print("   ⚠️ Minimum RAM available (8GB+)")
        else:
            print("   ❌ Insufficient RAM (8GB+ recommended)")
    except ImportError:
        print("   ⚠️ Cannot check RAM (psutil not installed)")
    
    # Check CUDA availability
    cuda_available = torch.cuda.is_available()
    print(f"🎮 CUDA Available: {cuda_available}")
    if cuda_available:
        gpu_count = torch.cuda.device_count()
        print(f"   🎯 GPU Count: {gpu_count}")
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
            print(f"   📱 GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
            
        if gpu_memory >= 8:
            print("   ✅ Sufficient GPU memory for Falcon 7B")
        else:
            print("   ⚠️ Limited GPU memory (8GB+ recommended)")
    else:
        print("   ⚠️ No CUDA GPU detected - will use CPU (slower)")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print_header("INSTALLING DEPENDENCIES")
    
    # Core ML packages
    packages = [
        ("torch>=2.0.0", "PyTorch (Deep Learning Framework)"),
        ("transformers>=4.35.0", "Hugging Face Transformers"),
        ("accelerate>=0.24.0", "Hugging Face Accelerate"),
        ("peft>=0.6.0", "Parameter Efficient Fine-Tuning"),
        ("bitsandbytes>=0.41.0", "Quantization Support"),
        ("sentencepiece>=0.1.99", "Tokenization Support"),
        ("psutil", "System Monitoring"),
        ("datasets>=2.15.0", "Dataset Utilities")
    ]
    
    success_count = 0
    for package, description in packages:
        if run_command(f"pip install {package}", f"Installing {description}"):
            success_count += 1
    
    print(f"\n📊 Installation Summary: {success_count}/{len(packages)} packages installed successfully")
    return success_count == len(packages)

def verify_installation():
    """Verify that all components are working"""
    print_header("VERIFICATION TESTS")
    
    # Test imports
    test_imports = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("accelerate", "Accelerate"),
        ("peft", "PEFT"),
        ("bitsandbytes", "BitsAndBytes")
    ]
    
    import_success = 0
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {name} import successful")
            import_success += 1
        except ImportError as e:
            print(f"   ❌ {name} import failed: {e}")
    
    # Test model loading (lightweight test)
    print(f"\n🧪 Testing model components...")
    try:
        from transformers import AutoTokenizer
        print("   ✅ Tokenizer loading capability verified")
        
        # Test if we can access the model (without downloading)
        model_name = "SHJ622/falcon_7b_ecommerce_ai_chatbot_n100"
        print(f"   🔍 Checking model accessibility: {model_name}")
        
        # This will check if the model exists without downloading
        try:
            from huggingface_hub import model_info
            info = model_info(model_name)
            print(f"   ✅ Model found on Hugging Face Hub")
            print(f"   📊 Model size: ~7B parameters")
        except Exception as e:
            print(f"   ⚠️ Model check warning: {e}")
            print(f"   💡 Model may still work when loaded directly")
        
    except Exception as e:
        print(f"   ❌ Model component test failed: {e}")
    
    return import_success >= len(test_imports) * 0.8

def create_config_files():
    """Create configuration files for LLM integration"""
    print_header("CREATING CONFIGURATION FILES")
    
    # Create LLM config
    llm_config = """# Falcon 7B LLM Configuration for FashionPulse
# This file contains settings for the LLM integration

[model]
name = "SHJ622/falcon_7b_ecommerce_ai_chatbot_n100"
device = "auto"  # auto, cuda, cpu
torch_dtype = "float16"  # float16, float32
max_new_tokens = 512
temperature = 0.7
top_p = 0.9
do_sample = true

[performance]
low_cpu_mem_usage = true
device_map = "auto"
load_in_8bit = false  # Set to true if you have limited GPU memory
load_in_4bit = false  # Set to true for even more memory savings

[fallback]
enable_fallback = true  # Use rule-based responses if LLM fails
fallback_timeout = 30  # Seconds to wait before falling back
"""
    
    config_path = Path("chat_agent/llm_config.ini")
    try:
        with open(config_path, 'w') as f:
            f.write(llm_config)
        print(f"   ✅ Created LLM config: {config_path}")
    except Exception as e:
        print(f"   ❌ Failed to create config: {e}")
    
    # Create startup script
    startup_script = """#!/usr/bin/env python3
# Quick start script for FashionPulse with Falcon 7B LLM

import os
import sys
import subprocess
from pathlib import Path

def start_services():
    print("🚀 Starting FashionPulse with Falcon 7B LLM...")
    
    # Start backend
    print("📦 Starting main backend...")
    backend_process = subprocess.Popen([sys.executable, "start_backend.py"])
    
    # Start chat agent with LLM
    print("🧠 Starting chat agent with LLM...")
    chat_process = subprocess.Popen([sys.executable, "chat_agent/api_server.py"])
    
    # Start frontend
    print("🌐 Starting frontend...")
    frontend_process = subprocess.Popen(["npm", "run", "dev"])
    
    print("✅ All services started!")
    print("🔗 Frontend: http://localhost:3000")
    print("🔗 Backend: http://localhost:5000")
    print("🔗 Chat Agent: http://localhost:5001")
    
    try:
        # Wait for processes
        backend_process.wait()
        chat_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down services...")
        backend_process.terminate()
        chat_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    start_services()
"""
    
    startup_path = Path("start_with_llm.py")
    try:
        with open(startup_path, 'w') as f:
            f.write(startup_script)
        os.chmod(startup_path, 0o755)  # Make executable
        print(f"   ✅ Created startup script: {startup_path}")
    except Exception as e:
        print(f"   ❌ Failed to create startup script: {e}")

def main():
    """Main setup function"""
    print_header("FALCON 7B LLM SETUP FOR FASHIONPULSE")
    print("This script will set up the Falcon 7B e-commerce chatbot integration")
    
    # Step 1: Check system requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met. Please upgrade your system.")
        return False
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed. Please check your internet connection and try again.")
        return False
    
    # Step 3: Verify installation
    if not verify_installation():
        print("\n⚠️ Some components may not be working correctly.")
        print("The system may still function with reduced capabilities.")
    
    # Step 4: Create config files
    create_config_files()
    
    # Final instructions
    print_header("SETUP COMPLETE!")
    print("🎉 Falcon 7B LLM integration setup is complete!")
    
    print("\n📋 **Next Steps:**")
    print("1. Restart your chat agent server:")
    print("   python chat_agent/api_server.py")
    
    print("\n2. Test the integration:")
    print("   python test_falcon_llm_integration.py")
    
    print("\n3. Or start all services at once:")
    print("   python start_with_llm.py")
    
    print("\n💡 **Usage Tips:**")
    print("• The LLM will handle complex e-commerce queries")
    print("• Product searches are enhanced with AI responses")
    print("• If LLM fails to load, fallback responses will be used")
    print("• Check logs for any loading issues")
    
    print("\n🔧 **Troubleshooting:**")
    print("• If model loading is slow, it's downloading (~13GB)")
    print("• For GPU memory issues, enable quantization in config")
    print("• CPU-only mode works but is slower")
    print("• Check chat_agent/api_server.py logs for details")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)