# Requirement
Linux environment with GPU 24GB + VRAM)

# Create environment
conda create -n drone-vla python=3.10 -y
conda activate drone-vla

# Install OpenVLA and core dependencies
git clone https://github.com/openvla/openvla.git
cd openvla
pip install -e .
pip install "flash-attn==2.5.5" --no-build-isolation
