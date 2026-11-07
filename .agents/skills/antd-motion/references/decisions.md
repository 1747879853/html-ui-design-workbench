# 动效参数与场景参考

## 判断动效是否值得做

Ant Motion 将动效的作用概括为：改善认知舒适度、突出重点、描述层级关系、提供反馈；同时要求目的明确且播放流畅。Ant Design 将原则概括为**自然、高效、克制**。用于业务界面时，先检查用户是否更快理解“发生了什么、从哪里来、去了哪里”。

原始 [「动效」页面](https://motion.ant.design/language/basic-cn)的正文只有两个章节，逐项对应如下：

| 原页内容 | 在本 Skill 中的应用 |
| --- | --- |
| 动效价值：增加体验舒适度，让认知自然 | `SKILL.md` 中维持视觉连续性的判断 |
| 动效价值：增加界面活力，吸引注意、突出重点 | `SKILL.md` 中引导注意的判断，且仅用于需要强调的内容 |
| 动效价值：描述层级关系与空间关系 | `SKILL.md` 中方向、起终点与界面结构一致；下表的浮层和页面转换 |
| 动效价值：提供反馈、明确意向 | `SKILL.md` 中交互状态与反馈目标；下表的按钮、选择、输入反馈 |
| 衡量意义：目的明确、没有多余动效 | `SKILL.md` 第 2 步的保留条件 |
| 衡量意义：不明显丢帧或卡顿，不影响产品性能 | `SKILL.md` 第 4、5 步的实现与真实浏览器检查 |

| 场景 | 动效选择 | 避免 |
| --- | --- | --- |
| 按钮、选择、输入反馈 | 用短促的状态过渡确认操作已经生效。 | 用装饰性循环动画代替真实反馈。 |
| Popover、Drawer、Modal 等浮层 | 方向和遮挡关系要解释层级；进场能被识别，离场可更快。 | 与触发点无关的位移、大幅缩放。 |
| 列表添加、删除、展开 | 尽可能保留对象连续性，让相邻内容变化可理解。 | 整页闪烁、所有行同时长距离移动。 |
| 批量入场 | 有明确阅读顺序时才使用轻微错峰；退出通常整块快速完成。 | 为每一项设置长延迟，阻碍下一步操作。 |
| 页面/复杂场景转换 | 根据空间关系和主要任务选择层级、方向与时长。 | 套用宣传页效果到高频业务操作。 |

## 时间与缓动

- [Ant Motion「速度」](https://motion.ant.design/language/speed-cn) 的历史设计语言示例：组件约 100/200/300 ms（小型/常规/较大）；页面转换以 150 ms 为步进，可能到 300/450/600 ms。这是设计参考，不是所有页面的硬性标准。
- 进入视口常用 ease-out，离开常用 ease-in，视口内点到点移动常用 ease-in-out；环状或机械运动可用线性。具体缓动应与对象和场景相称。
- Ant Design React 的主题文档列出 `motionDurationFast`、`motionDurationMid`、`motionDurationSlow` 和多个 `motionEase*` Token，默认分别为 0.1/0.2/0.3 秒。这些是设计参照；本项目要核对 Ant Design Vue 4.x 的实际组件样式和 API，不把 React 版 Token 或旧文档的 `450ms/easeInOutQuad` 动画库默认值当作本项目配置。
- 组件内置动效通常由组件库控制。React 文档中的 `ConfigProvider theme.token.motion = false` 是 React 版示例，不可直接套用到此 Vue 项目；若需关闭动效，先确认本项目的组件库和资源支持什么方式，再评估应用级影响。

## 官方来源

- [Ant Motion「动效」](https://motion.ant.design/language/basic-cn)：动效价值与意义。
- [Ant Design「动效」](https://ant-design.antgroup.com/docs/spec/motion-cn)：自然、高效、克制。
- [Ant Motion「速度」](https://motion.ant.design/language/speed-cn)：时间单位、缓动与进出场。
- [Ant Motion「空间」](https://motion.ant.design/language/space-cn)：层级、视差与远近关系。
- [Ant Motion「组合动效」](https://motion.ant.design/language/combined)：多元素队列与聚散的适用场景。
- [Ant Design React「定制主题」](https://ant-design.antgroup.com/docs/react/customize-theme-cn)：React 版动效 Token 与关闭动效配置，仅作设计参照。
