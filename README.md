# 队式16 - Deep Blue

欢迎来到队式16的开发仓库~

本仓库目前包括了逻辑组和平台组，未来…会不会有界面组和3D组呢(⊙_⊙?)

目前入驻的暂时只有：

**逻辑组**：郭一隆 (@Vone), 王殷豪 (@yale59888), 孙胜扬 (@ssydasheng)

**平台组**：李思涵 (@ThomasLee), 阮磊 (@tristoner), 刘家硕 (@liudd13)

好像人马上就要齐了，逻辑组好像还有一个人(⊙_⊙?)


## 公告公告，大家看这里看这里~

还没有学会git的，现在赶快去现学现卖~

[Git教程](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000) by 廖雪峰

[Git简明指南](http://rogerdudler.github.io/git-guide/index.zh.html) by rogerdudler（据说是雨泽学长推荐）

然后去学习一下一种[正确的分支姿势](http://www.ruanyifeng.com/blog/2012/07/git.html)，这次的开发的分支策略就是基于这个的。 ***真的很重要！！！***


## 当前任务
图例：

***紧急的任务***

一般的任务

*关系不大的任务*

### 逻辑组
* ***确定 逻辑/平台 接口***
* 编出能跑的游戏
* *更新文档，使得其与basic.h保持一致*

### 平台组
* ***确定 逻辑/平台 接口***
* 写出对战流程
* 完成和选手程序方面的通信
* 完成能黑箱运行的对战程序

## 已完成
√ 提供 Markdown/LaTex 格式的选手文档 (@ThomasLee)

## 关于Git
请大家 ***不要*** 使用中文文件名或目录名 = =

请大家 ***不要*** 直接对 **master** 分支进行修改，而是将 **develop** 分支作为主要开发分支。（为了保险起见我还是把 **master** 设为protected了…Orz）

请大家 ***不要commit写到一半的代码***，对每次commit ***附上清晰简明的概要***，并且 ***在本地测试没有问题之后再push***

请大家在merge时 ***使用*** `--no-ff` ***参数***，以保持branch层次的清晰

鉴于惨痛的经验…为了保持分支图的清晰，如果在push时发现远程仓库下的对应分支已被修改，并且预期不会有太多的conflict， ***请不要直接使用*** `git pull`， ***而是使用*** `git pull --rebase`，以避免不必要的merge

---------------------------------------------------------------------

大家加油~🙏
