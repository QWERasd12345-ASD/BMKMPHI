# preparing for the constrastive learning

import torch
from torch import nn
from einops import rearrange

class ContrastiveLoss(torch.nn.Module):
    def __init__(self, margin=1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, x0, x1, y):
        diff = x0 - x1
        dist_sq = torch.sum(torch.pow(diff, 2), 1)
        dist = torch.sqrt(dist_sq)

        mdist = self.margin - dist
        dist = torch.clamp(mdist, min=0.0)
        loss = y * dist_sq + (1 - y) * torch.pow(dist, 2)
        loss = torch.sum(loss) / 2.0 / x0.size()[0]

        return loss

def distance(x1, x2, dist_type="euc"):
    if dist_type == "euc":
        dist = torch.cdist(x1, x2) ** 2

    elif dist_type == "cos":
        cos = nn.CosineSimilarity(dim=1, eps=1e-6)
        dist = cos(x1, x2)

    return dist

class Mamba2(nn.Module):
    def __init__(self, d_model, n_layer=24, d_state=128, d_conv=4, expand=2, headdim=64, chunk_size=64, vocab_size=50277, pad_vocab_size_multiple=16):
        super().__init__()
        self.fc = nn.Linear(d_model, d_model)  # 示例线性层，替换为实际逻辑
        self.hidden_state = nn.Parameter(torch.zeros(1, d_model))  # 示例隐藏状态

    def forward(self, u, h=None):
        """
        Arguments:
            u: Input tensor of shape (batch, sequence_length, d_model)
            h: Hidden state for inference (optional)

        Returns:
            y: Output tensor of shape (batch, sequence_length, d_model)
            h: Updated hidden state
        """
        # Example forward logic
        y = self.fc(u)  # Perform a transformation
        h = self.hidden_state if h is None else h  # Update hidden state
        return y, h

class NdMamba2_2d(nn.Module):
    def __init__(self, cin, mamba_dim, cout, **mamba2_args):
        super().__init__()
        self.fc_in = nn.Linear(cin, mamba_dim, bias=False)
        self.mamba2_for = Mamba2(mamba_dim, **mamba2_args)
        self.mamba2_back = Mamba2(mamba_dim, **mamba2_args)
        self.fc_out = nn.Linear(mamba_dim, cout, bias=False)

    def forward(self, x):
        h, w = x.shape[2:]
        # Padding to ensure compatibility with Mamba2
        x = nn.functional.pad(x, (0, (8 - x.shape[3] % 8) % 8,
                                   0, (8 - x.shape[2] % 8) % 8))
        h8, w8 = x.shape[2:]
        x = rearrange(x, 'b c h w -> b (h w) c')  # Flatten spatial dimensions
        x = self.fc_in(x)  # Adjust channels

        # Forward through Mamba2 layers
        x1, h1 = self.mamba2_for(x)
        x2, h2 = self.mamba2_back(x.flip(1))
        x2 = x2.flip(1)  # Reverse back to original order

        x = x1 + x2  # Combine forward and backward passes
        x = self.fc_out(x)  # Adjust channels back
        x = rearrange(x, 'b (h w) c -> b c h w', h=h8)  # Reshape back to 2D
        x = x[:, :, :h, :w]  # Remove padding
        return x

class cnn_module(nn.Module):
    def __init__(self, kernel_size=7, dr=0):
        super(cnn_module, self).__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=kernel_size, stride=2)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=kernel_size, stride=2)
        self.bn2 = nn.BatchNorm2d(128)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(2)
        self.dropout = nn.Dropout(dr)

        # Adding NdMamba2_2d layer
        self.ndmamba2_2d = NdMamba2_2d(128, 128, 128)

        self.fc1 = nn.Linear(4608, 512)

    def forward(self, x):
        x = self.bn1(self.relu(self.conv1(x)))
        x = self.bn2(self.relu(self.conv2(x)))
        x = self.maxpool(x)

        # Passing through NdMamba2_2d
        x = self.ndmamba2_2d(x)

        x = self.fc1(torch.flatten(x, 1))  # Flatten and pass through FC
        return x

