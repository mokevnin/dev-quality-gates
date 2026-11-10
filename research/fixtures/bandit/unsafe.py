import torch
from huggingface_hub import hf_hub_download

torch.load("model.pt", weights_only=False)
hf_hub_download(repo_id="example/model", filename="weights.bin", revision="main")
