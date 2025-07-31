# 开发指南

欢迎有兴趣的开发者为 Qalgo 贡献代码！本指南将帮助您搭建本地开发环境。

## 环境搭建

1.  **克隆项目**

    首先，从 GitHub 克隆最新的项目代码到您的本地机器：

        git clone https://github.com/QuantumAlgorithm/QuantumAlgorithm.git
        cd QuantumAlgorithm


2.  **安装 Qalgo**

    我们推荐使用可编辑模式（`-e`）安装。这样做的好处是，您对源代码的任何修改都会立刻生效，无需重新安装。

        pip install -e .


3.  **安装开发依赖**

    `requirements.txt` 文件中包含了测试、文档生成等开发过程中所需要的额外工具。

        pip install -r requirements.txt

## 测试
我们使用 `pytest` 作为测试框架。在完成代码修改后，请运行完整的测试套件以确保没有引入新的问题。

    pytest


## 提交规范
本项目使用 `commitizen` 来规范化提交信息（commit message）。这有助于生成清晰的变更日志（CHANGELOG.md）。请使用以下命令进行提交：

    cz commit

它将引导您完成提交信息的填写。

## 文档
本项目使用 `mkdocs` 生成文档。您可以在本地启动一个实时预览服务器来查看您的文档修改效果。

    mkdocs serve

启动后，在浏览器中访问 `http://127.0.0.1:8000` 即可。

## 贡献流程
1.  Fork 本项目到您的 GitHub 账户。
2.  基于 `main` 分支创建一个新的分支。
3.  在新的分支上进行开发和修改。
4.  确保所有测试通过。
5.  提交您的修改，并推送到您的 Fork 仓库。
6.  在原始仓库发起一个 Pull Request，并详细描述您的修改内容。

## 发布
本项目配置了 GitHub Actions，当新的 tag 被推送到仓库时，会自动构建并发布新版本到 PyPI。

