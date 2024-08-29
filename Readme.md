
# XJ_Python

在开发过程中写下的一些有用的类，主要与PyQt5相关。

- 可运行``ModuleTest.py``查看XJ包中每个模块的测试样例的效果。
- 直接下载整个项目然后运行``buildWheel.bat``脚本直接生成并安装轮子，
- 实际上安装轮子太过于费事，通常都是将项目代码拉到另一个需要的项目下面使用，或者设置一下Python环境路径``PYTHONPATH``然后将项目代码丢到这个环境路径中；

![ModuleTest](./Preview/Preview-ModuleTest.png)


<br>

# 部分Widgets模块展示：

##### 弹窗，功能与``QMenu``出现一定程度的重合(同是可以将窗口弹出至鼠标附近)
![XJQ_HintBox](./Preview/Preview-XJQ_HintBox.gif)

<br>

##### 跑马灯容器，可以装载任意控件，滚动方向速度等均可调整
![XJQ_MarqueeBox](./Preview/Preview-XJQ_MarqueeBox.gif)

<br>

##### 遮罩类，往其中加入动画控件便可实现加载动画效果
![XJQ_Mask](./Preview/Preview-XJQ_Mask.gif)

<br>

##### 鼠标触发器，可以设定范围，进入、离开、范围内悬停均会触发信号
![XJQ_MouseTriggerBox](./Preview/Preview-XJQ_MouseTriggerBox.gif)

<br>

##### 图片列表，可打开大量图片并且有加载动画以及资源超时自动释放(避免占用过多内存)，鼠标悬浮时可查看预览图
![XJQ_PictListView](./Preview/Preview-XJQ_PictListView.gif)

<br>

##### 冒泡/消息提示弹窗，方位顺序可调整，例如优先显示在某块区域左侧或下方
![XJQ_PopupBox](./Preview/Preview-XJQ_PopupBox.gif)

<br>



