import matplotlib.pyplot as plt
import torch
from PIL import Image
from SSIM_PIL import compare_ssim
from torchvision.transforms import transforms
from tqdm import tqdm

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
HISTORY = "images/history.png"


def weights_init(m):
    if hasattr(m, "weight"):
        m.weight.data.uniform_(-0.5, 0.5)
    if hasattr(m, "bias"):
        m.bias.data.uniform_(-0.5, 0.5)


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        act = torch.nn.Sigmoid
        self.body = torch.nn.Sequential(
            torch.nn.Conv2d(3, 12, kernel_size=5, padding=5 // 2, stride=2),
            act(),
            torch.nn.Conv2d(12, 12, kernel_size=5, padding=5 // 2, stride=2),
            act(),
            torch.nn.Conv2d(12, 12, kernel_size=5, padding=5 // 2, stride=1),
            act(),
        )
        self.fc = torch.nn.Sequential(torch.nn.Linear(768, 100))

    def forward(self, x):
        out = self.body(x)
        out = out.view(out.size(0), -1)
        # print(out.size())
        out = self.fc(out)
        return out


def dataProcess(model, gradient, tech, method, iteration=50):

    gradient = torch.load(gradient)
    net = Net().to(DEVICE)
    net.apply(weights_init)
    net.load_state_dict(torch.load(model))

    labelSize = torch.empty(1, 100).size()
    imgSize = torch.empty(1, 3, 32, 32).size()

    dummy_data = torch.randn(imgSize).to(DEVICE).requires_grad_(True)
    dummy_label = torch.randn(labelSize).to(DEVICE).requires_grad_(True)

    optimizer = torch.optim.LBFGS([dummy_data, dummy_label])

    original_dy_dx = list((_.detach().clone() for _ in gradient))
    history = []

    print("recover image...")
    for iters in tqdm(range(iteration)):

        def closure():
            optimizer.zero_grad()
            criterion = torch.nn.CrossEntropyLoss()
            dummy_pred = net(dummy_data)
            dummy_onehot_label = torch.nn.functional.softmax(
                dummy_label, dim=-1
            )

            dummy_loss = criterion(dummy_pred, dummy_onehot_label)
            dummy_dy_dx = torch.autograd.grad(
                dummy_loss, net.parameters(), create_graph=True
            )

            grad_diff = 0
            for gx, gy in zip(dummy_dy_dx, original_dy_dx):
                grad_diff += ((gx - gy) ** 2).sum()
            grad_diff.backward()

            return grad_diff

        optimizer.step(closure)

        if iters % 10 == 0:
            current_loss = closure()
            loss = "%.4f" % current_loss.item()
            tqdm.write(f"iter: {iters}, loss: {loss}")
            history.append(transforms.ToPILImage()(dummy_data[0].cpu()))

    plt.figure(3, figsize=(12, 8))
    for i in range(int(iteration / 10)):
        plt.subplot(3, 10, i + 1)
        plt.imshow(history[i])
        plt.title("iter=%d" % (i * 10))
        plt.axis("off")

    plt.savefig(HISTORY)

    return history[-1]


def PETValidation(recover, origin, tech):

    if tech == "FL":
        origin = Image.open(origin)
        similarity = compare_ssim(recover, origin, GPU=False)

        return {"recover": recover, "origin": origin, "similarity": similarity}
