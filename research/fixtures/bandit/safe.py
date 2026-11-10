import torch
from huggingface_hub import hf_hub_download

torch.load("model.pt", weights_only=True)
hf_hub_download(
    repo_id="example/model",
    filename="weights.bin",
    revision="0123456789abcdef0123456789abcdef01234567",
)
