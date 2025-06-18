import numpy as np
import qalgo as qa
from qalgo import qda
from matplotlib import pyplot as plt


def plot_nonzero_distribution(A: np.ndarray):
    """
    绘制大型矩阵的非零元素分布图。

    参数:
        A (numpy.ndarray): 输入的 NumPy 矩阵。
    """
    # 检查输入是否为 NumPy 数组
    if not isinstance(A, np.ndarray):
        raise ValueError("Input must be a numpy.ndarray")

    # 获取非零元素的坐标
    nonzero_rows, nonzero_cols = np.nonzero(A)

    # 创建图形
    plt.figure()
    plt.scatter(nonzero_cols, nonzero_rows, s=1, color="blue", alpha=0.6)
    plt.gca().invert_yaxis()  # 矩阵可视化通常从左上角开始显示
    plt.title("Non-Zero Element Distribution")
    plt.xlabel("Column Index")
    plt.ylabel("Row Index")
    plt.grid(False)
    plt.show()


def loadtxt(A_filename: str, b_filename: str) -> tuple[np.ndarray, np.ndarray]:
    A = np.loadtxt("A1.txt")
    if A.shape != (1798, 1798):
        raise ValueError(
            "Matrix A in A.txt does not have the correct shape (1798, 1798)."
        )
    plot_nonzero_distribution(A)
    print(qa.condest(A))

    b_raw = np.loadtxt("output1.txt")
    if b_raw.shape != (29, 62):
        raise ValueError(
            "Matrix b in output.txt does not have the correct shape (29, 62)."
        )
    b = b_raw.flatten(order="C")  # 行主序展开
    if b.size != 1798:
        raise ValueError("Flattened vector b does not have the correct size (1798).")

    return A, b


def generate() -> tuple[np.ndarray, np.ndarray]:
    A = np.array([[1, 2, 3, 4], [2, 1, 4, 5], [3, 4, 1, 6], [4, 5, 6, 1.]])
    b = np.array([3, 4.5, 11.8, 0.2])

    return A, b


def main():
    A, b = loadtxt("A1.txt", "output1.txt")
    # A, b = generate()

    A_q, b_q, recover_x = qda.classical2quantum(A, b)
    print(b_q.shape)
    x_q = qda.solve(A_q, b_q)
    print(x_q.shape)
    # x_hat = recover_x(x_q)

    # # 最小化 || b - norm A x_hat ||，得到 x 的模长 norm
    # y = np.dot(A, x_hat)
    # norm = np.dot(b, y) / np.dot(y, y)
    # print(norm)
    # x = norm * x_hat

    # print(len(x))


if __name__ == "__main__":
    main()
