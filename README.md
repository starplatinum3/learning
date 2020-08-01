# learning

#### 介绍
背单词，背公式

#### 软件架构
软件架构说明


#### 安装教程

1.  `pip install pyqt5`
2.  下载文件，直接运行
3.  xxxx

#### 使用说明

1.  在输入问题的文本框输入问题，在输入答案的文本跨输入答案，点击“从文本框录入答案”按钮
可以把答案录入，点show ans按钮可以显示当前在输入问题文本框里面的问题的答案
2.  录入答案也可以是从剪贴板录入图片答案，先把问题输入到文本框，再把答案截图，
然后点从 ”剪贴板输入答案“ 按钮
3.  点save是保存问题和答案，关闭软件的时候也会保存

4. 点modify ans 可以更改某个问题的答案，操作和1，2一样，只是点modify之后会直接
 覆盖原来的答案
5. 点show list 展示已有问题的列表，点列表里的文字可以直接显示答案
6. 点 unshow answer， 隐藏答案
7. 点 upgrade table 把已有的问题更新到列表
8.添加了DataBase() 类 ，专门管理数据。因为修饰他为@singleton ，所以他只有一个实例，每次new一个database其实就是调用了那个实例，就可以管理数据了。
9. 添加了Direction(QWidget),点dir按钮可以打开目录，点目录里的某个文件夹，可以跳出那个文件夹里有的问题，问题就可以分类了。点那个问题，会跳出问题的答案，列问题的框的最下面有个unshow ans 按钮，可以隐藏问题的答案，然后这个按钮会变成show ans，点了就会展示答案。
右键问题，可以把问题放在某个文件夹，或者创建一个新的文件夹放这个问题。请不要在问题以外的地方点右键进行菜单操作，那会出问题

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 码云特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5.  码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
