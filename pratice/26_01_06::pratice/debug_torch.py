import torch
import sys

print(f"Python execution: {sys.executable}")
print(f"Torch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    try:
        print(f"CUDA Device Count: {torch.cuda.device_count()}")
        print(f"CUDA Device Name: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        print(f"Error getting CUDA info: {e}")
else:
    print("CUDA not detected.")

try:
    x = torch.rand(5, 3)
    print("Basic Tensor Operation (rand): Success")
except Exception as e:
    print(f"Basic Tensor Operation Failed: {e}")
