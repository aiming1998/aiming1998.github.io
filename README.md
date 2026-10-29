# 个人主页

毛一鸣 / Aiming（论文署名 Yiming Mao）的轻量双语个人主页。参考 Qiayuan Liao 主页的信息结构，代码为独立实现。没有外部字体、统计脚本或运行时依赖。

目标网址：https://aiming1998.github.io/ 。GitHub 仓库：`aiming1998/aiming1998.github.io`。

## 本地查看

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
```

打开 `http://127.0.0.1:8765`。中文页面为 `/zh.html`。离线时也可以直接打开 `site/index.html`。

## 更新内容

修改 `content.json` 后重新运行 `python3 build.py`。文字字段支持 `en` / `zh`。姓名、当前身份、简介和方向放在 `profile`；项目放在 `projects`；教育背景放在 `education`；开源软件与经历分别放在 `software` 和 `experience`。

个人照片位于 `assets/portrait.jpg`。原始照片保持原样，通过页面 CSS 逆时针旋转 90 度并裁切为头像区。替换正向照片时，删除 `profile.photo_rotation` 或设为 `0`。项目图片和简历也放在 `assets/`。不要把 GitHub fork 当作原创贡献。

公开资料已由用户提供或从论文来源核实。`publish_ready: true` 会生成允许索引的页面和 sitemap。开发草稿时可临时设为 `false`。`--publish` 检查会阻止残留的示例项目发布。

## GitHub Pages

用户已确认使用 `aiming1998`。本机 `gh` 登录该账号；GitHub 连接器登录的是另一个账号，不能用于本项目的发布。

仅提交本目录内的主页源码，不能把上级论文目录一起上传。`.github/workflows/pages.yml` 会构建 `site/` 并发布；仓库 Settings → Pages 的 Source 使用 GitHub Actions。现有 ARM 项目仓库和发布源保持独立。

执行 `python3 build.py --publish` 可检查基本发布条件。也可以只把构建后的 `site/` 内容提交到单独仓库，并使用分支根目录作为 Pages 发布源。

## 已实现

- 中英文独立 HTML 页面，页面主要内容不依赖 JavaScript 渲染。
- 可用方向键切换的页签，切换语言保留当前栏目。
- 移动端布局、键盘焦点、跳过导航、打印样式。
- 只展示已填写的联系方式，不生成虚假的论文、指标和履历。

版式参考：[Qiayuan Liao](https://qiayuanl.github.io/)。代码为独立实现，未复制参考站的照片、项目图或履历。

## 内容与素材来源

- 姓名、英文名、Pokebot 算法专家身份、具身智能数据与全链路模型训练方向、个人照片：用户在当前对话提供。
- ARM 论文与第一作者身份：https://arxiv.org/abs/2604.03037 。CVF 官方记录为 CVPR 2026 Workshops（GigaBrain Challenge），Poster 形式由用户提供。
- ARM 官方条目：https://openaccess.thecvf.com/content/CVPR2026W/GigaBrainChallenge/html/Mao_ARM_Advantage_Reward_Modeling_for_Long-Horizon_Manipulation_CVPRW_2026_paper.html 。
- ARM 99.4% 指标限定为项目页报告的 GR00T N1.5 + ARM（AW-BC）长时程叠毛巾实验：https://aiming1998.github.io/ARM/ 。
- ARM 缩略图：https://aiming1998.github.io/ARM/video/0109-poster.jpg 。
- CTRL 论文与作者顺序：https://arxiv.org/abs/2304.12315 。Oral 标记由官方会议手册和第一作者主页交叉核实。
- CTRL 官方代码：https://github.com/tusen-ai/SST 。缩略图：https://lue.fan/images/ctrl_teaser.png 。
- 主页仅标注论文作者身份，未推断个人负责模块、学历、任职起始时间或未提供的联系方式。
- 工作与指导关系按用户本人自述整理：小米汽车和图森未来实习、地平线与逐际动力经历，以及在破壳的数据负责人和预训练职责；不补写任职年份。
- 教育背景按用户补充更新为：湖南大学自动驾驶方向硕士研究生；同时在清华大学智能网联汽车课题组、李克强团队下由高铭老师联合指导。页面分别标注研究生身份和联合培养关系，不推断入学或毕业年份。
- 清华大学校徽来源：https://vi.tsinghua.edu.cn/gk/xxbz/xh/bzjbzsy.htm 。原图保存为 `assets/tsinghua.jpg`，仅使用 CSS 隐藏四周留白，不改动徽章。
- 湖南大学校徽来源：https://100.hnu.edu.cn/bsxz1/bsxz.htm 的官方素材包 https://100.hnu.edu.cn/xiaohuixiaoming.zip ，使用其中 `bsxz/8cdd90f3c7a47e7a7fc6e27975a9935f.jpg` 的独立校徽，原样保存为 `assets/hunan.jpg`。
- FluxVLA Engine：https://arxiv.org/html/2609.17210v1 ，论文署名含 Yiming Mao（第 10 作者）；公开状态为 arXiv 技术报告。主页作者列表用省略号缩写，论文入口指向最新摘要页。
- FluxVLA 官方代码与框架图：https://github.com/FluxVLA/FluxVLA 、https://raw.githubusercontent.com/FluxVLA/FluxVLA/main/assets/framework.png 。
