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
- ARM 代码已在 FluxVLA 开源：https://github.com/FluxVLA/FluxVLA ，使用说明：https://github.com/FluxVLA/FluxVLA/blob/main/docs/arm.md 。
- CTRL 论文与作者顺序：https://arxiv.org/abs/2304.12315 。Oral 标记由官方会议手册和第一作者主页交叉核实。
- CTRL 官方代码：https://github.com/tusen-ai/SST 。缩略图：https://lue.fan/images/ctrl_teaser.png 。
- CTRL 的 Waymo 检测与跟踪双任务 SOTA 为 2023 年论文报告结果，采用离线设置；依据 CVF 官方补充材料表 2（跟踪）与表 3（检测）：https://openaccess.thecvf.com/content/ICCV2023/supplemental/Fan_Once_Detected_Never_ICCV_2023_supplemental.pdf 。表 3 注明检测榜单结果截至 2023 年 3 月 8 日，跟踪表未单独标注截止日期；不表示当前榜单排名。
- 个人介绍中的许华哲 / Huazhe Xu 链接由本人提供：http://hxu.rocks/ 。
- 主页仅标注论文作者身份，未推断个人负责模块、学历、任职起始时间或未提供的联系方式。
- 工作与指导关系按用户本人自述整理：小米汽车和图森未来实习、地平线与逐际动力经历，以及在破壳的数据负责人和预训练职责；不补写任职年份。
- 教育背景按用户补充更新为：湖南大学自动驾驶方向硕士研究生；同时在清华大学智能网联汽车课题组、李克强团队下由高铭老师联合指导。页面分别标注研究生身份和联合培养关系，不推断入学或毕业年份。
- 团队归属按用户进一步补充：湖南大学钟志华院士、丁荣军院士团队；清华大学李克强院士团队。团队归属单独突出展示，高铭老师联合指导单独说明；不把团队归属扩写为三位院士直接指导。湖南大学两位院士称谓可参考 https://mve.hnu.edu.cn/hdjxyyzgcxy/szdw/jslb.htm 。
- 清华大学校徽来源：https://vi.tsinghua.edu.cn/gk/xxbz/xh/bzjbzsy.htm 。原图保存为 `assets/tsinghua.jpg`，仅使用 CSS 隐藏四周留白，不改动徽章。
- 湖南大学校徽来源：https://100.hnu.edu.cn/bsxz1/bsxz.htm 的官方素材包 https://100.hnu.edu.cn/xiaohuixiaoming.zip ，使用其中 `bsxz/8cdd90f3c7a47e7a7fc6e27975a9935f.jpg` 的独立校徽，原样保存为 `assets/hunan.jpg`。
- FluxVLA Engine：https://arxiv.org/html/2609.17210v1 ，论文署名含 Yiming Mao（第 10 作者）；公开状态为 arXiv 技术报告。主页作者列表用省略号缩写，论文入口指向最新摘要页。
- FluxVLA 官方代码与框架图：https://github.com/FluxVLA/FluxVLA 、https://raw.githubusercontent.com/FluxVLA/FluxVLA/main/assets/framework.png 。

## 职业经历与公司标识

五家公司分别展示；破壳标为当前，小米汽车与图森未来标为实习。研究方向不作为未确认的正式职级，不补写任职年份。根据用户确认，闫岩、王峰、王乃岩的指导关系写入图森未来实习经历。

用户确认在逐际动力为 COSA 0.5 提供数据、模型与部分算法支持；Highlights 将其作为产业项目展示，职业经历同步说明个人贡献，附官方技术报告 https://www.limxdynamics.com/cosa05v3/#zh 。该说明不推断具体模块负责人或论文作者身份。配图为报告中的官方架构图 https://limx-video.oss-cn-beijing.aliyuncs.com/cosa05v3/limx-vla-architecture.svg ，原样保存为 `assets/cosa05-architecture.svg`。

标识作为经历识别使用，素材保留原样：

- PokeBot：从 https://pokebot.com/ 导航中的第一枚 `viewBox="0 0 141 84"` 内联 SVG 提取为 `assets/pokebot.svg`。
- 逐际动力：使用官网原始红色标识 https://www.limxdynamics.com/favicon.ico?favicon.41f4bc48.ico ，原样保存为 `assets/limx-red.ico`。
- 地平线：https://www.horizon.auto/favicon.png 实际为 ICO，原样提取其中的 256×256 PNG 字节，保存为 `assets/horizon.png`。
- 小米汽车：https://www.xiaomiauto.com/global 官方橙色标识 https://g-s1.xiaomiauto.com/xiaomiauto-com-global-assets/images/0815/home/logo-mi.png ，原样保存为 `assets/xiaomi-orange.png`。
- 图森未来：采用历史 TuSimple 标识，来源为 Goodyear 与 TuSimple 的官方合作公告 https://www.prnewswire.com/news-releases/goodyear-and-tusimple-collaborate-on-autonomous-vehicle-freight-operations-301175138.html ，原图 https://mma.prnewswire.com/media/1335812/TuSimple.jpg?p=original ，保存为 `assets/tusimple.jpg`。
